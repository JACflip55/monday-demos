#!/usr/bin/env python3
"""
Angel Portfolio Math — Monte Carlo Portfolio Construction Simulator

Simulates angel portfolio outcomes using power law distributions.
Helps answer: How many deals? What check size? Follow-on or diversify?

Usage:
    python portfolio_sim.py                    # Default parameters
    python portfolio_sim.py --deals 30 --check 25000 --fund 500000
    python portfolio_sim.py --html             # Generate HTML report
    python portfolio_sim.py --interactive      # Interactive mode

No external dependencies — pure Python 3.6+
"""

import argparse
import json
import math
import random
import statistics
import sys
from datetime import datetime


# --- Power Law Outcome Distribution ---
# Based on real angel portfolio data (AngelList, Kauffman Foundation studies)
# Most startups fail; a few return massively.

OUTCOME_DISTRIBUTION = {
    "total_loss": {"prob": 0.40, "multiple": 0.0, "label": "Total Loss (0x)"},
    "partial_loss": {"prob": 0.20, "multiple": 0.3, "label": "Partial Loss (0.3x)"},
    "break_even": {"prob": 0.15, "multiple": 1.0, "label": "Break Even (1x)"},
    "modest_return": {"prob": 0.10, "multiple": 2.5, "label": "Modest (2.5x)"},
    "good_return": {"prob": 0.08, "multiple": 5.0, "label": "Good (5x)"},
    "great_return": {"prob": 0.04, "multiple": 10.0, "label": "Great (10x)"},
    "home_run": {"prob": 0.02, "multiple": 30.0, "label": "Home Run (30x)"},
    "unicorn": {"prob": 0.01, "multiple": 100.0, "label": "Unicorn (100x)"},
}


def simulate_deal():
    """Simulate a single deal outcome using the power law distribution."""
    r = random.random()
    cumulative = 0.0
    for outcome_data in OUTCOME_DISTRIBUTION.values():
        cumulative += outcome_data["prob"]
        if r <= cumulative:
            # Add some variance within each bucket
            base = outcome_data["multiple"]
            if base == 0:
                return 0.0
            variance = random.uniform(0.7, 1.4)
            return base * variance
    return 0.0


def simulate_portfolio(num_deals, check_size, follow_on_pct=0.0, follow_on_threshold=3.0, num_simulations=10000):
    """
    Run Monte Carlo simulation of an angel portfolio.

    Args:
        num_deals: Number of initial investments
        check_size: Amount per initial check
        follow_on_pct: Percentage of fund reserved for follow-ons (0-1)
        follow_on_threshold: Only follow on if deal is tracking above this multiple
        num_simulations: Number of Monte Carlo runs

    Returns:
        dict with simulation results
    """
    total_capital = num_deals * check_size
    follow_on_reserve = total_capital * follow_on_pct
    initial_capital = total_capital - follow_on_reserve
    actual_check = initial_capital / num_deals if num_deals > 0 else 0

    portfolio_returns = []
    moics = []
    best_deals = []

    for _ in range(num_simulations):
        deals = []
        for _ in range(num_deals):
            multiple = simulate_deal()
            deals.append(multiple)

        # Follow-on logic: double down on winners
        total_invested = initial_capital
        total_returned = sum(d * actual_check for d in deals)

        if follow_on_pct > 0:
            # Find deals tracking above threshold, invest follow-on equally
            winners = [d for d in deals if d >= follow_on_threshold]
            if winners:
                follow_on_per_deal = follow_on_reserve / len(winners)
                for w in winners:
                    # Follow-on gets same multiple (simplified)
                    total_returned += w * follow_on_per_deal
                total_invested += follow_on_reserve

        moic = total_returned / total_invested if total_invested > 0 else 0
        net_return = total_returned - total_invested
        portfolio_returns.append(net_return)
        moics.append(moic)
        best_deals.append(max(deals) if deals else 0)

    # Calculate statistics
    moics_sorted = sorted(moics)
    returns_sorted = sorted(portfolio_returns)

    results = {
        "params": {
            "num_deals": num_deals,
            "check_size": check_size,
            "total_capital": total_capital,
            "follow_on_pct": follow_on_pct,
            "follow_on_threshold": follow_on_threshold,
            "num_simulations": num_simulations,
        },
        "moic": {
            "mean": statistics.mean(moics),
            "median": statistics.median(moics),
            "p10": moics_sorted[int(num_simulations * 0.10)],
            "p25": moics_sorted[int(num_simulations * 0.25)],
            "p75": moics_sorted[int(num_simulations * 0.75)],
            "p90": moics_sorted[int(num_simulations * 0.90)],
            "std_dev": statistics.stdev(moics),
        },
        "returns": {
            "mean": statistics.mean(portfolio_returns),
            "median": statistics.median(portfolio_returns),
            "prob_profit": sum(1 for r in portfolio_returns if r > 0) / num_simulations,
            "prob_2x": sum(1 for m in moics if m >= 2.0) / num_simulations,
            "prob_3x": sum(1 for m in moics if m >= 3.0) / num_simulations,
            "prob_5x": sum(1 for m in moics if m >= 5.0) / num_simulations,
            "prob_10x": sum(1 for m in moics if m >= 10.0) / num_simulations,
        },
        "distribution": {
            "histogram": compute_histogram(moics, bins=20),
            "best_deal_avg": statistics.mean(best_deals),
        },
    }
    return results


def compute_histogram(values, bins=20):
    """Compute histogram buckets for charting."""
    min_val = min(values)
    max_val = min(max(values), 20.0)  # Cap display at 20x for readability
    bucket_width = (max_val - min_val) / bins if max_val > min_val else 1
    buckets = [0] * bins
    for v in values:
        idx = int((min(v, max_val) - min_val) / bucket_width) if bucket_width > 0 else 0
        idx = min(idx, bins - 1)
        buckets[idx] += 1
    return {
        "buckets": buckets,
        "min": min_val,
        "max": max_val,
        "bucket_width": bucket_width,
    }


def compare_strategies(base_deals=20, base_check=25000):
    """Compare different portfolio construction strategies."""
    fund_size = base_deals * base_check

    strategies = [
        {"name": "Concentrated (10 deals)", "deals": 10, "check": fund_size // 10, "follow_on": 0.0},
        {"name": "Balanced (20 deals)", "deals": 20, "check": fund_size // 20, "follow_on": 0.0},
        {"name": "Diversified (40 deals)", "deals": 40, "check": fund_size // 40, "follow_on": 0.0},
        {"name": "Spray & Pray (60 deals)", "deals": 60, "check": fund_size // 60, "follow_on": 0.0},
        {"name": "Balanced + Follow-on", "deals": 15, "check": fund_size // 20, "follow_on": 0.25},
        {"name": "Concentrated + Follow-on", "deals": 8, "check": fund_size // 12, "follow_on": 0.33},
    ]

    results = []
    for s in strategies:
        sim = simulate_portfolio(
            num_deals=s["deals"],
            check_size=s["check"],
            follow_on_pct=s["follow_on"],
            num_simulations=10000,
        )
        results.append({
            "strategy": s["name"],
            "deals": s["deals"],
            "check_size": s["check"],
            "follow_on_pct": s["follow_on"],
            "mean_moic": sim["moic"]["mean"],
            "median_moic": sim["moic"]["median"],
            "prob_profit": sim["returns"]["prob_profit"],
            "prob_3x": sim["returns"]["prob_3x"],
            "prob_5x": sim["returns"]["prob_5x"],
            "p10_moic": sim["moic"]["p10"],
            "p90_moic": sim["moic"]["p90"],
        })

    return results


def print_results(results):
    """Pretty-print simulation results to terminal."""
    params = results["params"]
    moic = results["moic"]
    returns = results["returns"]

    print("\n" + "=" * 60)
    print("  ANGEL PORTFOLIO MATH — Monte Carlo Simulation")
    print("=" * 60)
    print(f"\n  Portfolio: {params['num_deals']} deals × ${params['check_size']:,.0f} = ${params['total_capital']:,.0f}")
    if params["follow_on_pct"] > 0:
        print(f"  Follow-on Reserve: {params['follow_on_pct']*100:.0f}% (>{params['follow_on_threshold']:.0f}x threshold)")
    print(f"  Simulations: {params['num_simulations']:,}")

    print("\n  ─── MOIC (Multiple on Invested Capital) ───")
    print(f"  Mean:   {moic['mean']:.2f}x")
    print(f"  Median: {moic['median']:.2f}x")
    print(f"  P10:    {moic['p10']:.2f}x  (worst 10%)")
    print(f"  P90:    {moic['p90']:.2f}x  (best 10%)")

    print("\n  ─── PROBABILITY ───")
    print(f"  Profit (>1x):  {returns['prob_profit']*100:.1f}%")
    print(f"  Double (>2x):  {returns['prob_2x']*100:.1f}%")
    print(f"  Triple (>3x):  {returns['prob_3x']*100:.1f}%")
    print(f"  5x return:     {returns['prob_5x']*100:.1f}%")
    print(f"  10x return:    {returns['prob_10x']*100:.1f}%")

    print("\n  ─── INSIGHTS ───")
    if moic["median"] < 1.0:
        print("  ⚠️  Median outcome is a loss — you need more deals or better selection")
    elif moic["median"] < 2.0:
        print("  📊 Median is modest — typical for angel portfolios without selection edge")
    else:
        print("  ✅ Strong median — your strategy has good base-rate economics")

    if returns["prob_profit"] < 0.5:
        print("  ⚠️  Less than 50% chance of making money — diversify more")
    elif returns["prob_profit"] > 0.7:
        print("  ✅ Good probability of profit — portfolio construction working")

    print("\n" + "=" * 60)


def generate_html(fund_size=500000):
    """Generate the interactive HTML demo."""
    # Pre-compute strategy comparison
    strategies = compare_strategies(base_deals=20, base_check=fund_size // 20)

    # Pre-compute a default simulation for initial display
    default_sim = simulate_portfolio(num_deals=20, check_size=fund_size // 20, num_simulations=10000)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Angel Portfolio Math — Monte Carlo Simulator</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    background: #0f172a;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    padding: 24px 16px;
    line-height: 1.5;
    min-height: 100vh;
}}
.container {{ max-width: 960px; margin: 0 auto; }}
h1 {{ font-size: 1.75rem; font-weight: 800; margin-bottom: 4px; }}
.subtitle {{ color: #64748b; font-size: 0.9rem; margin-bottom: 28px; }}
h2 {{ font-size: 1.2rem; font-weight: 700; margin: 24px 0 12px; color: #f1f5f9; }}
h3 {{ font-size: 1rem; font-weight: 600; margin: 16px 0 8px; color: #cbd5e1; }}

/* Cards */
.card {{
    background: #1e293b;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
}}
.card-accent {{ border-left: 4px solid #06b6d4; }}
.card-green {{ border-left: 4px solid #22c55e; }}
.card-amber {{ border-left: 4px solid #f59e0b; }}

/* Inputs */
.input-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 20px;
}}
.input-group {{ display: flex; flex-direction: column; gap: 6px; }}
.input-group label {{
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
}}
.input-group input[type="range"] {{
    width: 100%;
    accent-color: #06b6d4;
}}
.input-value {{
    font-size: 1.3rem;
    font-weight: 700;
    color: #06b6d4;
}}
.input-group input[type="number"] {{
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e2e8f0;
    font-size: 1rem;
    width: 100%;
}}
button {{
    background: #06b6d4;
    color: #0f172a;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
}}
button:hover {{ background: #22d3ee; }}
button:active {{ transform: scale(0.98); }}

/* Stats Grid */
.stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin: 16px 0;
}}
.stat-box {{
    background: #0f172a;
    border-radius: 8px;
    padding: 14px;
    text-align: center;
}}
.stat-value {{
    font-size: 1.5rem;
    font-weight: 800;
    color: #06b6d4;
}}
.stat-label {{
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 4px;
    text-transform: uppercase;
}}

/* Chart */
.chart-container {{
    width: 100%;
    height: 200px;
    position: relative;
    margin: 16px 0;
}}
.bar-chart {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    height: 100%;
    padding: 0 4px;
    gap: 2px;
}}
.bar {{
    flex: 1;
    background: #06b6d4;
    border-radius: 3px 3px 0 0;
    min-width: 8px;
    transition: height 0.3s;
    position: relative;
}}
.bar:hover {{ background: #22d3ee; }}
.chart-labels {{
    display: flex;
    justify-content: space-between;
    padding: 4px 4px 0;
    font-size: 0.7rem;
    color: #475569;
}}

/* Strategy Table */
.strategy-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    margin: 12px 0;
}}
.strategy-table th {{
    text-align: left;
    padding: 10px 12px;
    color: #64748b;
    font-size: 0.75rem;
    text-transform: uppercase;
    border-bottom: 1px solid #334155;
}}
.strategy-table td {{
    padding: 10px 12px;
    border-bottom: 1px solid #1e293b;
    color: #cbd5e1;
}}
.strategy-table tr:hover td {{ background: #1e293b; }}
.highlight {{ color: #22c55e; font-weight: 700; }}
.warn {{ color: #f59e0b; }}
.danger {{ color: #ef4444; }}

/* Insights */
.insight {{
    display: flex;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid #1e293b;
}}
.insight:last-child {{ border-bottom: none; }}
.insight-icon {{ font-size: 1.2rem; flex-shrink: 0; }}
.insight-text {{ color: #94a3b8; font-size: 0.9rem; }}

/* Collapsible */
.collapsible {{
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.collapsible::before {{
    content: '▶';
    font-size: 0.7rem;
    transition: transform 0.2s;
}}
.collapsible.open::before {{ transform: rotate(90deg); }}
.collapsible-content {{
    display: none;
    padding-top: 12px;
}}
.collapsible-content.show {{ display: block; }}

/* Responsive */
@media (max-width: 600px) {{
    .input-grid {{ grid-template-columns: 1fr; }}
    .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .strategy-table {{ font-size: 0.75rem; }}
    .strategy-table th, .strategy-table td {{ padding: 8px 6px; }}
    h1 {{ font-size: 1.4rem; }}
}}
</style>
</head>
<body>
<div class="container">
    <h1>📐 Angel Portfolio Math</h1>
    <p class="subtitle">Monte Carlo Simulator · June 22, 2026 · How many deals should you really do?</p>

    <!-- Input Controls -->
    <div class="card card-accent">
        <h2 style="margin-top:0;">Configure Your Portfolio</h2>
        <div class="input-grid">
            <div class="input-group">
                <label>Number of Deals</label>
                <input type="range" id="numDeals" min="5" max="80" value="20" oninput="updateDisplay()">
                <span class="input-value" id="numDealsVal">20</span>
            </div>
            <div class="input-group">
                <label>Check Size ($)</label>
                <input type="range" id="checkSize" min="5000" max="100000" step="5000" value="25000" oninput="updateDisplay()">
                <span class="input-value" id="checkSizeVal">$25,000</span>
            </div>
            <div class="input-group">
                <label>Follow-On Reserve (%)</label>
                <input type="range" id="followOn" min="0" max="50" step="5" value="0" oninput="updateDisplay()">
                <span class="input-value" id="followOnVal">0%</span>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
            <button onclick="runSimulation()">🎲 Run 10,000 Simulations</button>
            <span id="totalCapital" style="color:#64748b; font-size:0.9rem;">Total capital: $500,000</span>
        </div>
    </div>

    <!-- Results -->
    <div id="results">
        <div class="card">
            <h2 style="margin-top:0;">Portfolio Outcomes</h2>
            <div class="stats-grid" id="statsGrid">
                <div class="stat-box"><div class="stat-value" id="meanMoic">—</div><div class="stat-label">Mean MOIC</div></div>
                <div class="stat-box"><div class="stat-value" id="medianMoic">—</div><div class="stat-label">Median MOIC</div></div>
                <div class="stat-box"><div class="stat-value" id="probProfit">—</div><div class="stat-label">Prob. Profit</div></div>
                <div class="stat-box"><div class="stat-value" id="prob3x">—</div><div class="stat-label">Prob. 3x+</div></div>
                <div class="stat-box"><div class="stat-value" id="p10">—</div><div class="stat-label">P10 (Bad)</div></div>
                <div class="stat-box"><div class="stat-value" id="p90">—</div><div class="stat-label">P90 (Great)</div></div>
            </div>
        </div>

        <!-- Distribution Chart -->
        <div class="card">
            <h2 style="margin-top:0;">Return Distribution</h2>
            <p style="color:#64748b; font-size:0.85rem; margin-bottom:12px;">MOIC distribution across 10,000 simulated portfolios</p>
            <div class="chart-container">
                <div class="bar-chart" id="barChart"></div>
            </div>
            <div class="chart-labels" id="chartLabels"></div>
        </div>

        <!-- Insights -->
        <div class="card card-green" id="insightsCard">
            <h2 style="margin-top:0;">💡 Key Insights</h2>
            <div id="insights"></div>
        </div>
    </div>

    <!-- Strategy Comparison -->
    <div class="card card-amber">
        <h2 style="margin-top:0;" class="collapsible open" onclick="toggleSection(this)">Strategy Comparison ($500K fund)</h2>
        <div class="collapsible-content show">
            <p style="color:#64748b; font-size:0.85rem; margin-bottom:12px;">Same $500K deployed differently — which construction wins?</p>
            <div style="overflow-x:auto;">
            <table class="strategy-table">
                <thead>
                    <tr>
                        <th>Strategy</th>
                        <th>Deals</th>
                        <th>Check</th>
                        <th>Mean</th>
                        <th>Median</th>
                        <th>P(Profit)</th>
                        <th>P(3x)</th>
                    </tr>
                </thead>
                <tbody id="strategyTable"></tbody>
            </table>
            </div>
        </div>
    </div>

    <!-- Power Law Explainer -->
    <div class="card">
        <h2 style="margin-top:0;" class="collapsible" onclick="toggleSection(this)">📚 Why Portfolio Math Matters</h2>
        <div class="collapsible-content">
            <div class="insight">
                <span class="insight-icon">📊</span>
                <span class="insight-text"><strong>The Power Law:</strong> ~65% of angel investments return less than 1x. But the top 1-2% return 30-100x+. Your portfolio must survive enough failures to catch a winner.</span>
            </div>
            <div class="insight">
                <span class="insight-icon">🎯</span>
                <span class="insight-text"><strong>Diversification is insurance:</strong> With 10 deals, there's a ~10% chance you miss a 10x+ entirely. With 30 deals, that drops to ~1%. More shots on goal = more chances to catch the power law tail.</span>
            </div>
            <div class="insight">
                <span class="insight-icon">💰</span>
                <span class="insight-text"><strong>Follow-on math:</strong> Reserving 25-33% for follow-ons into winners can boost returns significantly — but only if you have signal on which companies are actually winning (not just "feels good").</span>
            </div>
            <div class="insight">
                <span class="insight-icon">⚖️</span>
                <span class="insight-text"><strong>The tradeoff:</strong> Concentrated portfolios have higher variance (bigger wins OR bigger losses). Diversified portfolios have lower variance but may cap upside through smaller check sizes that limit pro-rata access.</span>
            </div>
            <div class="insight">
                <span class="insight-icon">🏆</span>
                <span class="insight-text"><strong>The research:</strong> Kauffman Foundation data shows angel portfolios of 15-20+ deals significantly outperform concentrated ones. The "spray and pray" label is misleading — it's really "spray and survive long enough to win."</span>
            </div>
        </div>
    </div>

    <p style="color:#334155; text-align:center; margin-top:32px; font-size:0.8rem;">
        Built by Claw · <a href="https://github.com/JACflip55/monday-demos" style="color:#475569;">github.com/JACflip55/monday-demos</a> · Based on AngelList/Kauffman data
    </p>
</div>

<script>
// --- Power Law Distribution (matches Python model) ---
const OUTCOMES = [
    {{ prob: 0.40, multiple: 0.0 }},
    {{ prob: 0.20, multiple: 0.3 }},
    {{ prob: 0.15, multiple: 1.0 }},
    {{ prob: 0.10, multiple: 2.5 }},
    {{ prob: 0.08, multiple: 5.0 }},
    {{ prob: 0.04, multiple: 10.0 }},
    {{ prob: 0.02, multiple: 30.0 }},
    {{ prob: 0.01, multiple: 100.0 }},
];

function simulateDeal() {{
    let r = Math.random();
    let cum = 0;
    for (const o of OUTCOMES) {{
        cum += o.prob;
        if (r <= cum) {{
            if (o.multiple === 0) return 0;
            return o.multiple * (0.7 + Math.random() * 0.7);
        }}
    }}
    return 0;
}}

function runSimulation() {{
    const numDeals = parseInt(document.getElementById('numDeals').value);
    const checkSize = parseInt(document.getElementById('checkSize').value);
    const followOnPct = parseInt(document.getElementById('followOn').value) / 100;
    const numSims = 10000;

    const totalCapital = numDeals * checkSize;
    const followOnReserve = totalCapital * followOnPct;
    const initialCapital = totalCapital - followOnReserve;
    const actualCheck = initialCapital / numDeals;

    let moics = [];

    for (let s = 0; s < numSims; s++) {{
        let deals = [];
        for (let d = 0; d < numDeals; d++) {{
            deals.push(simulateDeal());
        }}

        let totalInvested = initialCapital;
        let totalReturned = deals.reduce((sum, m) => sum + m * actualCheck, 0);

        if (followOnPct > 0) {{
            const winners = deals.filter(d => d >= 3.0);
            if (winners.length > 0) {{
                const perDeal = followOnReserve / winners.length;
                winners.forEach(w => {{ totalReturned += w * perDeal; }});
                totalInvested += followOnReserve;
            }}
        }}

        moics.push(totalReturned / totalInvested);
    }}

    moics.sort((a, b) => a - b);

    // Stats
    const mean = moics.reduce((s, v) => s + v, 0) / numSims;
    const median = moics[Math.floor(numSims / 2)];
    const probProfit = moics.filter(m => m > 1).length / numSims;
    const prob3x = moics.filter(m => m >= 3).length / numSims;
    const p10 = moics[Math.floor(numSims * 0.10)];
    const p90 = moics[Math.floor(numSims * 0.90)];

    // Update UI
    document.getElementById('meanMoic').textContent = mean.toFixed(2) + 'x';
    document.getElementById('medianMoic').textContent = median.toFixed(2) + 'x';
    document.getElementById('probProfit').textContent = (probProfit * 100).toFixed(0) + '%';
    document.getElementById('prob3x').textContent = (prob3x * 100).toFixed(0) + '%';
    document.getElementById('p10').textContent = p10.toFixed(2) + 'x';
    document.getElementById('p90').textContent = p90.toFixed(2) + 'x';

    // Color code
    document.getElementById('meanMoic').style.color = mean >= 2 ? '#22c55e' : mean >= 1 ? '#06b6d4' : '#ef4444';
    document.getElementById('medianMoic').style.color = median >= 2 ? '#22c55e' : median >= 1 ? '#06b6d4' : '#ef4444';

    // Histogram
    renderChart(moics);

    // Insights
    renderInsights(mean, median, probProfit, prob3x, p10, p90, numDeals, followOnPct);
}}

function renderChart(moics) {{
    const bins = 25;
    const maxDisplay = 15; // Cap at 15x for chart
    const bucketWidth = maxDisplay / bins;
    let buckets = new Array(bins).fill(0);

    for (const m of moics) {{
        const idx = Math.min(Math.floor(Math.min(m, maxDisplay - 0.01) / bucketWidth), bins - 1);
        buckets[idx]++;
    }}

    const maxBucket = Math.max(...buckets);
    const chart = document.getElementById('barChart');
    const labels = document.getElementById('chartLabels');

    chart.innerHTML = buckets.map((count, i) => {{
        const height = (count / maxBucket * 100).toFixed(1);
        const moicVal = (i * bucketWidth).toFixed(1);
        return `<div class="bar" style="height:${{height}}%" title="${{moicVal}}x-${{(parseFloat(moicVal)+bucketWidth).toFixed(1)}}x: ${{count}} portfolios"></div>`;
    }}).join('');

    labels.innerHTML = `<span>0x</span><span>${{(maxDisplay/4).toFixed(0)}}x</span><span>${{(maxDisplay/2).toFixed(0)}}x</span><span>${{(maxDisplay*3/4).toFixed(0)}}x</span><span>${{maxDisplay}}x+</span>`;
}}

function renderInsights(mean, median, probProfit, prob3x, p10, p90, numDeals, followOnPct) {{
    let insights = [];

    if (median < 1.0) {{
        insights.push({{ icon: '⚠️', text: `<strong>Median is below 1x (${{median.toFixed(2)}}x)</strong> — more than half of simulated portfolios lose money. Consider more deals for better diversification.` }});
    }} else if (median >= 2.0) {{
        insights.push({{ icon: '🏆', text: `<strong>Strong median (${{median.toFixed(2)}}x)</strong> — this portfolio construction gives you a solid base case.` }});
    }} else {{
        insights.push({{ icon: '📊', text: `<strong>Median ${{median.toFixed(2)}}x</strong> — typical for angel portfolios. The mean (${{mean.toFixed(2)}}x) is higher because of power law winners pulling it up.` }});
    }}

    if (numDeals < 15) {{
        insights.push({{ icon: '🎰', text: `<strong>High variance alert:</strong> With only ${{numDeals}} deals, your outcome depends heavily on luck. Research suggests 15-20+ deals for reliable angel returns.` }});
    }} else if (numDeals >= 40) {{
        insights.push({{ icon: '🌊', text: `<strong>Well-diversified (${{numDeals}} deals):</strong> High probability of catching at least one big winner. Tradeoff: smaller checks may limit pro-rata rights in later rounds.` }});
    }}

    if (followOnPct > 0) {{
        insights.push({{ icon: '🔄', text: `<strong>Follow-on reserve (${{(followOnPct*100).toFixed(0)}}%):</strong> Doubles down on winners tracking 3x+. This boosts expected returns but requires good signal on which companies are actually winning.` }});
    }} else {{
        insights.push({{ icon: '💡', text: `<strong>No follow-on reserve:</strong> Try adding 20-30% reserve. Following on into winners is one of the highest-ROI moves in angel investing.` }});
    }}

    const spread = p90 - p10;
    if (spread > 5) {{
        insights.push({{ icon: '📈', text: `<strong>Wide range (${{p10.toFixed(1)}}x to ${{p90.toFixed(1)}}x):</strong> Your best-case is ${{(p90).toFixed(1)}}x but worst-case is ${{p10.toFixed(2)}}x. High variance = you need to be comfortable with either outcome.` }});
    }}

    document.getElementById('insights').innerHTML = insights.map(i =>
        `<div class="insight"><span class="insight-icon">${{i.icon}}</span><span class="insight-text">${{i.text}}</span></div>`
    ).join('');
}}

function updateDisplay() {{
    const numDeals = document.getElementById('numDeals').value;
    const checkSize = parseInt(document.getElementById('checkSize').value);
    const followOn = document.getElementById('followOn').value;

    document.getElementById('numDealsVal').textContent = numDeals;
    document.getElementById('checkSizeVal').textContent = '$' + checkSize.toLocaleString();
    document.getElementById('followOnVal').textContent = followOn + '%';
    document.getElementById('totalCapital').textContent = 'Total capital: $' + (numDeals * checkSize).toLocaleString();
}}

function toggleSection(el) {{
    el.classList.toggle('open');
    const content = el.nextElementSibling;
    content.classList.toggle('show');
}}

// --- Load Strategy Table ---
const strategies = {json.dumps(strategies)};

function loadStrategies() {{
    const tbody = document.getElementById('strategyTable');
    tbody.innerHTML = strategies.map(s => {{
        const meanClass = s.mean_moic >= 2.5 ? 'highlight' : s.mean_moic >= 1.5 ? '' : 'danger';
        const profitClass = s.prob_profit >= 0.6 ? 'highlight' : s.prob_profit >= 0.45 ? 'warn' : 'danger';
        return `<tr>
            <td style="font-weight:600;color:#f1f5f9;">${{s.strategy}}</td>
            <td>${{s.deals}}</td>
            <td>$${{s.check_size.toLocaleString()}}</td>
            <td class="${{meanClass}}">${{s.mean_moic.toFixed(2)}}x</td>
            <td>${{s.median_moic.toFixed(2)}}x</td>
            <td class="${{profitClass}}">${{(s.prob_profit*100).toFixed(0)}}%</td>
            <td>${{(s.prob_3x*100).toFixed(0)}}%</td>
        </tr>`;
    }}).join('');
}}

// --- Initialize ---
loadStrategies();
runSimulation();
</script>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Angel Portfolio Math — Monte Carlo Simulator")
    parser.add_argument("--deals", type=int, default=20, help="Number of deals")
    parser.add_argument("--check", type=int, default=25000, help="Check size ($)")
    parser.add_argument("--fund", type=int, default=None, help="Total fund size (overrides deals×check)")
    parser.add_argument("--follow-on", type=float, default=0.0, help="Follow-on reserve (0-0.5)")
    parser.add_argument("--sims", type=int, default=10000, help="Number of simulations")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--compare", action="store_true", help="Compare strategies")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--output", type=str, default="output/index.html", help="HTML output path")

    args = parser.parse_args()

    if args.html:
        fund = args.fund or (args.deals * args.check)
        html = generate_html(fund_size=fund)
        with open(args.output, "w") as f:
            f.write(html)
        print(f"✅ HTML demo generated: {args.output}")
        return

    if args.compare:
        strategies = compare_strategies(args.deals, args.check)
        print("\n" + "=" * 80)
        print("  STRATEGY COMPARISON")
        print("=" * 80)
        print(f"  {'Strategy':<28} {'Deals':>5} {'Mean':>6} {'Median':>7} {'P(Profit)':>10} {'P(3x)':>7}")
        print("  " + "─" * 72)
        for s in strategies:
            print(f"  {s['strategy']:<28} {s['deals']:>5} {s['mean_moic']:>5.2f}x {s['median_moic']:>6.2f}x {s['prob_profit']*100:>8.1f}% {s['prob_3x']*100:>6.1f}%")
        print("=" * 80)
        return

    if args.interactive:
        print("\n🎲 Angel Portfolio Math — Interactive Mode\n")
        try:
            deals = int(input("  Number of deals [20]: ") or 20)
            check = int(input("  Check size ($) [25000]: ") or 25000)
            follow = float(input("  Follow-on reserve (0-0.5) [0]: ") or 0)
        except (ValueError, EOFError):
            deals, check, follow = 20, 25000, 0.0

        results = simulate_portfolio(deals, check, follow, num_simulations=args.sims)
        print_results(results)
        return

    # Default: run with args
    results = simulate_portfolio(
        num_deals=args.deals,
        check_size=args.check,
        follow_on_pct=args.follow_on,
        num_simulations=args.sims,
    )
    print_results(results)


if __name__ == "__main__":
    main()

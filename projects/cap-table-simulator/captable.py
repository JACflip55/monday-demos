#!/usr/bin/env python3
"""
Cap Table Simulator — Model equity dilution across funding rounds.

Pure Python 3.6+, no dependencies.
"""

import json
import sys
import os
import argparse
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


# ─── Data Models ───────────────────────────────────────────────────────────────

@dataclass
class Shareholder:
    name: str
    shares: int = 0
    invested: float = 0.0
    share_type: str = "common"  # common, preferred

    @property
    def display_type(self):
        return "⭐" if self.share_type == "preferred" else "○"


@dataclass
class Round:
    name: str
    raised: float
    pre_money: float
    option_pool_pct: float = 0.0  # target pool % post-round
    lead_investor: str = ""

    @property
    def post_money(self):
        return self.pre_money + self.raised

    @property
    def price_per_share(self):
        return None  # calculated during simulation


@dataclass
class Scenario:
    company: str
    rounds: List[Dict]
    your_investment: Dict
    exit_valuations: List[float] = field(default_factory=lambda: [50_000_000, 100_000_000, 500_000_000])


# ─── Simulation Engine ─────────────────────────────────────────────────────────

class CapTableSimulator:
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self.shareholders: Dict[str, Shareholder] = {}
        self.total_shares = 0
        self.round_snapshots = []
        self.pps_history = []  # price per share each round

    def run(self):
        """Execute the full simulation."""
        # Initialize founders
        founder_shares = 10_000_000
        self.shareholders["Founders"] = Shareholder("Founders", founder_shares, 0, "common")
        self.total_shares = founder_shares

        for round_data in self.scenario.rounds:
            self._process_round(round_data)

        return self

    def _process_round(self, round_data: Dict):
        """Process a single funding round."""
        name = round_data["name"]
        raised = round_data["raised"]
        pre_money = round_data["pre_money"]
        option_pool_pct = round_data.get("option_pool_pct", 0)
        post_money = pre_money + raised

        # Option pool adjustment (created pre-money, dilutes existing holders)
        if option_pool_pct > 0:
            current_pool = self.shareholders.get("Option Pool", Shareholder("Option Pool", 0, 0, "common"))
            current_pool_pct = current_pool.shares / self.total_shares if self.total_shares > 0 else 0
            target_pool_shares = int(self.total_shares * option_pool_pct / (100 - option_pool_pct))
            new_pool_shares = max(0, target_pool_shares - current_pool.shares)
            if new_pool_shares > 0:
                current_pool.shares += new_pool_shares
                self.total_shares += new_pool_shares
                self.shareholders["Option Pool"] = current_pool

        # Calculate price per share
        pps = pre_money / self.total_shares
        self.pps_history.append({"round": name, "pps": pps})

        # Issue new shares to investors
        new_shares = int(raised / pps)
        self.total_shares += new_shares

        # Determine investor name
        investor_name = round_data.get("lead_investor", f"{name} Investors")

        # Check if this is the round where "you" invest
        your_inv = self.scenario.your_investment
        if your_inv.get("round") == name:
            your_amount = your_inv["amount"]
            your_shares = int(your_amount / pps)
            other_amount = raised - your_amount
            other_shares = new_shares - your_shares

            if "You (Angel)" in self.shareholders:
                self.shareholders["You (Angel)"].shares += your_shares
                self.shareholders["You (Angel)"].invested += your_amount
            else:
                self.shareholders["You (Angel)"] = Shareholder("You (Angel)", your_shares, your_amount, "preferred")

            if other_shares > 0:
                if investor_name in self.shareholders:
                    self.shareholders[investor_name].shares += other_shares
                    self.shareholders[investor_name].invested += other_amount
                else:
                    self.shareholders[investor_name] = Shareholder(investor_name, other_shares, other_amount, "preferred")
        else:
            if investor_name in self.shareholders:
                self.shareholders[investor_name].shares += new_shares
                self.shareholders[investor_name].invested += raised
            else:
                self.shareholders[investor_name] = Shareholder(investor_name, new_shares, raised, "preferred")

        # Snapshot
        snapshot = {
            "round": name,
            "raised": raised,
            "pre_money": pre_money,
            "post_money": post_money,
            "pps": pps,
            "total_shares": self.total_shares,
            "holdings": {k: {"shares": v.shares, "pct": v.shares / self.total_shares * 100}
                         for k, v in self.shareholders.items()}
        }
        self.round_snapshots.append(snapshot)

    def get_your_ownership(self) -> Tuple[float, float]:
        """Returns (ownership_pct, total_invested)."""
        you = self.shareholders.get("You (Angel)")
        if not you:
            return 0.0, 0.0
        return you.shares / self.total_shares * 100, you.invested

    def calculate_exits(self) -> List[Dict]:
        """Calculate exit payouts at various valuations."""
        results = []
        you = self.shareholders.get("You (Angel)")
        if not you:
            return results

        ownership_pct = you.shares / self.total_shares
        for valuation in self.scenario.exit_valuations:
            payout = valuation * ownership_pct
            moic = payout / you.invested if you.invested > 0 else 0
            results.append({
                "valuation": valuation,
                "payout": payout,
                "moic": moic,
                "invested": you.invested
            })
        return results

    def calculate_prorata(self) -> Dict:
        """Calculate cost to maintain ownership via pro-rata in subsequent rounds."""
        your_inv = self.scenario.your_investment
        initial_round_idx = None
        for i, r in enumerate(self.scenario.rounds):
            if r["name"] == your_inv["round"]:
                initial_round_idx = i
                break

        if initial_round_idx is None:
            return {}

        # Get ownership after initial round
        initial_snapshot = self.round_snapshots[initial_round_idx]
        initial_pct = initial_snapshot["holdings"].get("You (Angel)", {}).get("pct", 0)

        # Calculate pro-rata cost for each subsequent round
        prorata_costs = []
        cumulative_cost = your_inv["amount"]

        for i in range(initial_round_idx + 1, len(self.round_snapshots)):
            snapshot = self.round_snapshots[i]
            round_data = self.scenario.rounds[i]
            # To maintain initial_pct, need to buy proportional new shares
            pps = snapshot["pps"]
            # Shares needed = initial_pct% of new shares issued
            new_shares_total = int(round_data["raised"] / pps)
            shares_needed = int(new_shares_total * initial_pct / 100)
            cost = shares_needed * pps
            cumulative_cost += cost
            prorata_costs.append({
                "round": round_data["name"],
                "cost": cost,
                "cumulative": cumulative_cost
            })

        # Final ownership comparison
        passive_pct = self.get_your_ownership()[0]

        return {
            "initial_pct": initial_pct,
            "passive_pct": passive_pct,
            "prorata_pct": initial_pct,
            "initial_investment": your_inv["amount"],
            "prorata_total_cost": cumulative_cost,
            "round_costs": prorata_costs
        }


# ─── Display Functions ─────────────────────────────────────────────────────────

def bar_chart(pct: float, width: int = 24) -> str:
    filled = int(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


def format_money(amount: float) -> str:
    if amount >= 1_000_000_000:
        return f"${amount/1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"${amount/1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.0f}K"
    else:
        return f"${amount:.0f}"


def format_shares(shares: int) -> str:
    if shares >= 1_000_000:
        return f"{shares/1_000_000:.1f}M"
    elif shares >= 1_000:
        return f"{shares/1_000:.0f}K"
    return str(shares)


def print_header(company: str):
    width = 64
    print()
    print("╔" + "═" * width + "╗")
    title = f"CAP TABLE SIMULATOR — {company.upper()}"
    padding = (width - len(title)) // 2
    print("║" + " " * padding + title + " " * (width - padding - len(title)) + "║")
    print("╠" + "═" * width + "╣")
    print()


def print_round(snapshot: Dict, highlight_you: bool = True):
    name = snapshot["round"]
    raised = snapshot["raised"]
    pre = snapshot["pre_money"]
    post = snapshot["post_money"]
    pps = snapshot["pps"]

    print(f" {name.upper()}    {format_money(raised)} raised @ {format_money(pre)} pre ({format_money(post)} post)  │  PPS: ${pps:.4f}")
    print(" " + "─" * 60)

    # Sort: Founders first, then by ownership desc
    holdings = sorted(snapshot["holdings"].items(),
                      key=lambda x: (0 if x[0] == "Founders" else 1, -x[1]["pct"]))

    for holder, data in holdings:
        pct = data["pct"]
        shares = data["shares"]
        bar = bar_chart(pct)
        marker = " ◀ YOU" if holder == "You (Angel)" and highlight_you else ""
        print(f"  {holder:<20} {pct:>5.1f}%  │  {bar}  {format_shares(shares):>6} shares{marker}")

    print()


def print_exits(exits: List[Dict]):
    if not exits:
        return
    print(" EXIT SCENARIOS")
    print(" " + "─" * 60)
    for ex in exits:
        emoji = "🦄" if ex["moic"] >= 100 else "🚀" if ex["moic"] >= 50 else "🔥" if ex["moic"] >= 10 else "✓"
        print(f"  {format_money(ex['valuation']):>6} exit  →  {format_money(ex['payout']):<12}  ({ex['moic']:.1f}x on {format_money(ex['invested'])} check)  {emoji}")
    print()


def print_prorata(prorata: Dict):
    if not prorata:
        return
    print(" PRO-RATA COMPARISON")
    print(" " + "─" * 60)
    print(f"  Passive (no follow-on):  {prorata['passive_pct']:.1f}% ownership  │  {format_money(prorata['initial_investment'])} total invested")
    print(f"  Pro-rata (maintain):     {prorata['prorata_pct']:.1f}% ownership  │  {format_money(prorata['prorata_total_cost'])} total invested")
    extra_cost = prorata['prorata_total_cost'] - prorata['initial_investment']
    print(f"  Extra cost: {format_money(extra_cost)}")
    if prorata["round_costs"]:
        print()
        print("  Follow-on schedule:")
        for rc in prorata["round_costs"]:
            print(f"    {rc['round']}: {format_money(rc['cost'])} (cumulative: {format_money(rc['cumulative'])})")
    print()


def print_summary(sim: CapTableSimulator):
    """Print a one-line investment summary."""
    ownership, invested = sim.get_your_ownership()
    rounds_participated = sim.scenario.your_investment["round"]
    print(" ─── SUMMARY ───")
    print(f"  You invested {format_money(invested)} in the {rounds_participated}")
    print(f"  After {len(sim.round_snapshots)} rounds: {ownership:.2f}% ownership")
    dilution = 100 - (ownership / (sim.round_snapshots[0]["holdings"].get("You (Angel)", {}).get("pct", ownership) or ownership) * 100)
    if dilution > 0:
        print(f"  Total dilution from peak: {dilution:.1f}%")
    print()


# ─── HTML Report ───────────────────────────────────────────────────────────────

def generate_html(sim: CapTableSimulator) -> str:
    exits = sim.calculate_exits()
    prorata = sim.calculate_prorata()
    ownership, invested = sim.get_your_ownership()

    rows_html = ""
    for snap in sim.round_snapshots:
        for holder, data in sorted(snap["holdings"].items(), key=lambda x: -x[1]["pct"]):
            highlight = ' style="background:#fff3cd;"' if holder == "You (Angel)" else ""
            rows_html += f'<tr{highlight}><td>{snap["round"]}</td><td>{holder}</td><td>{data["pct"]:.1f}%</td><td>{format_shares(data["shares"])}</td></tr>\n'

    exit_rows = ""
    for ex in exits:
        exit_rows += f'<tr><td>{format_money(ex["valuation"])}</td><td>{format_money(ex["payout"])}</td><td>{ex["moic"]:.1f}x</td></tr>\n'

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Cap Table — {sim.scenario.company}</title>
<style>
body {{ font-family: -apple-system, system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; background: #f8f9fa; }}
h1 {{ color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 0.5rem; }}
h2 {{ color: #16213e; margin-top: 2rem; }}
table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
th, td {{ padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid #eee; }}
th {{ background: #1a1a2e; color: white; }}
tr:hover {{ background: #f5f5f5; }}
.metric {{ display: inline-block; background: white; padding: 1rem 1.5rem; margin: 0.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
.metric .value {{ font-size: 1.8rem; font-weight: bold; color: #e94560; }}
.metric .label {{ font-size: 0.85rem; color: #666; }}
.timestamp {{ color: #999; font-size: 0.85rem; }}
</style></head><body>
<h1>📊 Cap Table Simulator — {sim.scenario.company}</h1>
<p class="timestamp">Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

<div>
<div class="metric"><div class="value">{ownership:.1f}%</div><div class="label">Your Ownership</div></div>
<div class="metric"><div class="value">{format_money(invested)}</div><div class="label">Total Invested</div></div>
<div class="metric"><div class="value">{len(sim.round_snapshots)}</div><div class="label">Rounds</div></div>
<div class="metric"><div class="value">{exits[-1]['moic']:.0f}x</div><div class="label">MOIC @ {format_money(exits[-1]['valuation'])}</div></div>
</div>

<h2>Ownership by Round</h2>
<table><tr><th>Round</th><th>Holder</th><th>Ownership</th><th>Shares</th></tr>
{rows_html}</table>

<h2>Exit Scenarios</h2>
<table><tr><th>Exit Valuation</th><th>Your Payout</th><th>MOIC</th></tr>
{exit_rows}</table>

<h2>Pro-Rata Analysis</h2>
<p><strong>Passive:</strong> {prorata.get('passive_pct', 0):.1f}% ownership, {format_money(prorata.get('initial_investment', 0))} invested</p>
<p><strong>Pro-rata:</strong> {prorata.get('prorata_pct', 0):.1f}% ownership, {format_money(prorata.get('prorata_total_cost', 0))} invested</p>

</body></html>"""
    return html


# ─── Default Scenario ──────────────────────────────────────────────────────────

DEFAULT_SCENARIO = {
    "company": "NovaMart AI",
    "rounds": [
        {
            "name": "Seed",
            "raised": 2_500_000,
            "pre_money": 7_500_000,
            "option_pool_pct": 10,
            "lead_investor": "Other Angels"
        },
        {
            "name": "Series A",
            "raised": 12_000_000,
            "pre_money": 38_000_000,
            "option_pool_pct": 15,
            "lead_investor": "Sequoia Capital"
        },
        {
            "name": "Series B",
            "raised": 35_000_000,
            "pre_money": 120_000_000,
            "option_pool_pct": 18,
            "lead_investor": "a16z"
        }
    ],
    "your_investment": {
        "round": "Seed",
        "amount": 50_000,
        "pro_rata_rights": True
    },
    "exit_valuations": [50_000_000, 150_000_000, 500_000_000, 1_000_000_000]
}


# ─── Interactive Mode ──────────────────────────────────────────────────────────

def interactive_mode() -> Dict:
    """Build a scenario interactively."""
    print("\n 🏗️  BUILD YOUR SCENARIO\n")

    company = input("  Company name: ").strip() or "My Startup"

    rounds = []
    round_num = 1
    round_names = ["Seed", "Series A", "Series B", "Series C", "Series D"]

    while True:
        default_name = round_names[round_num - 1] if round_num <= len(round_names) else f"Round {round_num}"
        print(f"\n  --- Round {round_num} ---")
        name = input(f"  Round name [{default_name}]: ").strip() or default_name

        raised_str = input("  Amount raised ($): ").strip().replace(",", "").replace("$", "")
        try:
            raised = float(raised_str)
        except ValueError:
            print("  Invalid amount, skipping round.")
            break

        pre_str = input("  Pre-money valuation ($): ").strip().replace(",", "").replace("$", "")
        try:
            pre_money = float(pre_str)
        except ValueError:
            print("  Invalid valuation, skipping round.")
            break

        pool_str = input("  Option pool % [10]: ").strip()
        option_pool_pct = float(pool_str) if pool_str else 10.0

        lead = input("  Lead investor name []: ").strip() or f"{name} Investors"

        rounds.append({
            "name": name,
            "raised": raised,
            "pre_money": pre_money,
            "option_pool_pct": option_pool_pct,
            "lead_investor": lead
        })

        another = input("\n  Add another round? [y/N]: ").strip().lower()
        if another != "y":
            break
        round_num += 1

    print("\n  --- Your Investment ---")
    print(f"  Available rounds: {', '.join(r['name'] for r in rounds)}")
    inv_round = input(f"  Which round did you invest in? [{rounds[0]['name']}]: ").strip() or rounds[0]["name"]
    inv_amount_str = input("  Your investment amount ($): ").strip().replace(",", "").replace("$", "")
    try:
        inv_amount = float(inv_amount_str)
    except ValueError:
        inv_amount = 50000

    return {
        "company": company,
        "rounds": rounds,
        "your_investment": {
            "round": inv_round,
            "amount": inv_amount,
            "pro_rata_rights": True
        },
        "exit_valuations": [50_000_000, 100_000_000, 500_000_000, 1_000_000_000]
    }


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Cap Table Simulator — model equity dilution")
    parser.add_argument("--scenario", "-s", help="Path to scenario JSON file")
    parser.add_argument("--interactive", "-i", action="store_true", help="Build scenario interactively")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--compare-prorata", action="store_true", help="Show pro-rata comparison")
    parser.add_argument("--exits", nargs="*", type=float, help="Custom exit valuations (e.g. 50000000 100000000)")
    args = parser.parse_args()

    # Load scenario
    if args.interactive:
        scenario_data = interactive_mode()
    elif args.scenario:
        with open(args.scenario, "r") as f:
            scenario_data = json.load(f)
    else:
        scenario_data = DEFAULT_SCENARIO

    if args.exits:
        scenario_data["exit_valuations"] = args.exits

    scenario = Scenario(
        company=scenario_data["company"],
        rounds=scenario_data["rounds"],
        your_investment=scenario_data["your_investment"],
        exit_valuations=scenario_data.get("exit_valuations", [50_000_000, 100_000_000, 500_000_000])
    )

    # Run simulation
    sim = CapTableSimulator(scenario)
    sim.run()

    # Display results
    print_header(scenario.company)

    for snapshot in sim.round_snapshots:
        print_round(snapshot)

    print_summary(sim)
    print_exits(sim.calculate_exits())

    if args.compare_prorata or True:  # Always show pro-rata
        print_prorata(sim.calculate_prorata())

    # HTML report
    if args.html:
        os.makedirs("output", exist_ok=True)
        filename = f"output/captable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html = generate_html(sim)
        with open(filename, "w") as f:
            f.write(html)
        print(f" 📄 HTML report saved: {filename}")
        print()

    print("╚" + "═" * 64 + "╝")


if __name__ == "__main__":
    main()

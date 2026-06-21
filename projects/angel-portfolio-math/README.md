# Angel Portfolio Math 📐

**Monte Carlo portfolio construction simulator — how many deals should you really do?**

Stop guessing your angel strategy. Run 10,000 simulated portfolios in seconds to see how deal count, check size, and follow-on reserves affect your probability of profit, 3x, and 10x returns.

---

## 🎮 Try It

**[→ Open the Interactive Demo](output/index.html)** (self-contained HTML, works offline)

The demo includes:
- 🎚️ Interactive sliders (deals, check size, follow-on %)
- 📊 Real-time Monte Carlo simulation (10K runs in-browser)
- 📈 Return distribution chart
- 💡 Auto-generated insights based on your parameters
- ⚖️ Strategy comparison table (concentrated vs. diversified vs. follow-on)
- 📚 Power law education section

---

## What It Does

Models angel portfolio outcomes using empirically-derived power law distributions:

| Outcome | Probability | Multiple |
|---------|------------|----------|
| Total Loss | 40% | 0x |
| Partial Loss | 20% | ~0.3x |
| Break Even | 15% | ~1x |
| Modest Return | 10% | ~2.5x |
| Good Return | 8% | ~5x |
| Great Return | 4% | ~10x |
| Home Run | 2% | ~30x |
| Unicorn | 1% | ~100x |

These are based on AngelList and Kauffman Foundation data on actual angel returns.

---

## Key Findings (from 10K simulations)

| Strategy | Deals | Mean MOIC | Median | P(Profit) | P(3x) |
|----------|-------|-----------|--------|-----------|--------|
| Concentrated | 10 | ~3.0x | ~1.6x | ~72% | ~28% |
| Balanced | 20 | ~3.0x | ~2.1x | ~84% | ~33% |
| Diversified | 40 | ~3.0x | ~2.4x | ~95% | ~40% |
| Balanced + Follow-on | 15+reserve | ~5.6x | ~3.3x | ~95% | ~56% |

**Insight:** Mean returns are similar across strategies (~3x) because the power law dominates. But median and probability of profit improve dramatically with diversification. Follow-on into winners is the strongest lever.

---

## Quick Start (CLI)

```bash
# No dependencies — pure Python 3.6+
cd projects/angel-portfolio-math

# Default simulation (20 deals × $25K)
python portfolio_sim.py

# Custom parameters
python portfolio_sim.py --deals 30 --check 15000 --follow-on 0.25

# Compare strategies
python portfolio_sim.py --compare

# Generate HTML report
python portfolio_sim.py --html

# Interactive mode
python portfolio_sim.py --interactive
```

---

## Why This Matters for Angels

1. **Most angels under-diversify** — 10 deals feels like a lot, but the math says 20+ is where reliability kicks in
2. **Mean vs. Median** — Power law means your "average" portfolio does way better than your "typical" one
3. **Follow-on is the cheat code** — Reserving 25-33% to double down on 3x+ trackers dramatically improves outcomes
4. **Luck surface area** — More shots on goal = higher chance of catching the 30x+ outlier that makes the whole portfolio

---

## Files

```
angel-portfolio-math/
├── README.md              # This file
├── portfolio_sim.py       # Python simulator (no deps)
├── output/
│   └── index.html         # Self-contained interactive HTML demo
└── FEEDBACK.md            # Your feedback
```

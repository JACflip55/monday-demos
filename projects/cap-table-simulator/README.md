# Cap Table Simulator 📊

**Model equity dilution across funding rounds — see exactly how your angel check performs.**

Stop guessing what your 5% will look like after Series A, B, and C. Run scenarios in seconds, compare pro-rata vs. passive strategies, and know your exit math before writing the check.

---

## What It Does

Simulates a startup's cap table evolution across multiple funding rounds, showing:

- **Dilution Waterfall** — watch ownership % shrink (or hold) round by round
- **Pro-Rata Modeling** — compare exercising vs. passing on follow-on rights
- **Exit Scenarios** — what does your stake pay out at $50M, $100M, $500M exits?
- **Multiple Investors** — track founders, angels, VCs, and option pool simultaneously
- **Liquidation Preferences** — models 1x non-participating preferred (standard)

### Key Metrics

| Metric | What It Shows |
|--------|---------------|
| **Ownership %** | Your slice of the pie each round |
| **Dilution Impact** | How much each round costs you |
| **Pro-Rata Cost** | What it costs to maintain your % |
| **Exit Payout** | Cash back at various exit valuations |
| **MOIC** | Multiple on Invested Capital |

---

## Quick Start

```bash
# No dependencies — pure Python 3.6+
cd projects/cap-table-simulator

# Run with default scenario (seed → Series A → Series B → exit)
python captable.py

# Custom scenario from JSON
python captable.py --scenario my_deal.json

# Interactive mode — build a scenario step by step
python captable.py --interactive

# Generate HTML report
python captable.py --html

# Compare pro-rata vs. passive strategy
python captable.py --compare-prorata
```

---

## Sample Output

```
╔══════════════════════════════════════════════════════════════╗
║              CAP TABLE SIMULATOR — ACME ROBOTICS            ║
╠══════════════════════════════════════════════════════════════╣

 SEED ROUND    $2M raised @ $8M pre ($10M post)
 ─────────────────────────────────────────────────
  Founders        70.0%  │  ████████████████████░░░░  7,000,000 shares
  Option Pool     10.0%  │  ███░░░░░░░░░░░░░░░░░░░░  1,000,000 shares
  You (Angel)      5.0%  │  █░░░░░░░░░░░░░░░░░░░░░░    500,000 shares
  Other Angels    15.0%  │  ████░░░░░░░░░░░░░░░░░░░  1,500,000 shares

 SERIES A    $10M raised @ $30M pre ($40M post)
 ─────────────────────────────────────────────────
  Founders        52.5%  │  █████████████░░░░░░░░░░  7,000,000 shares
  Option Pool     12.0%  │  ███░░░░░░░░░░░░░░░░░░░░  1,600,000 shares
  You (Angel)      3.8%  │  █░░░░░░░░░░░░░░░░░░░░░░    500,000 shares
  Other Angels    11.3%  │  ███░░░░░░░░░░░░░░░░░░░░  1,500,000 shares
  Series A VC     20.5%  │  █████░░░░░░░░░░░░░░░░░░  2,733,333 shares

 EXIT SCENARIOS (Your stake: 3.8% after Series A)
 ─────────────────────────────────────────────────
  $50M exit   →  $1,875,000   (37.5x on $50K check)  🔥
  $100M exit  →  $3,750,000   (75.0x)                 🚀
  $500M exit  →  $18,750,000  (375.0x)                🦄

 PRO-RATA COMPARISON
 ─────────────────────────────────────────────────
  Passive (no follow-on):  3.8% ownership  │  $50K total invested
  Pro-rata (maintain 5%):  5.0% ownership  │  $175K total invested
  Extra cost: $125K  │  Extra exit value at $100M: +$1,250,000
```

---

## Scenario Format

```json
{
  "company": "Acme Robotics",
  "rounds": [
    {
      "name": "Seed",
      "raised": 2000000,
      "pre_money": 8000000,
      "option_pool_pct": 10
    },
    {
      "name": "Series A",
      "raised": 10000000,
      "pre_money": 30000000,
      "option_pool_pct": 12
    }
  ],
  "your_investment": {
    "round": "Seed",
    "amount": 50000,
    "pro_rata_rights": true
  }
}
```

---

## How It Works

1. **Share Calculation** — Converts dollar investments to share counts at each round's price-per-share
2. **Dilution Cascade** — New shares issued each round dilute all existing holders proportionally
3. **Option Pool Shuffle** — Models the "option pool shuffle" (pool created pre-money, diluting existing holders)
4. **Pro-Rata Math** — Calculates exact dollar amount needed to maintain ownership %
5. **Exit Waterfall** — Applies liquidation preferences before distributing remaining proceeds

---

## Why This Matters

Most angels don't model dilution before writing a check. They see "5% ownership" and imagine 5% of a $100M exit. Reality: after 2-3 rounds of dilution, that 5% is often 1.5-2.5%. This tool makes the math visceral and immediate.

**Use it to:**
- Decide check sizes (how much gets you to meaningful ownership?)
- Evaluate pro-rata rights (when is follow-on worth it?)
- Set realistic return expectations
- Compare deals (which structure preserves more value?)

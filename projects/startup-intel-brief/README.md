# Startup Intel Brief 🔍

**Pre-meeting due diligence tool for angel investors.**

Stop walking into pitch meetings cold. Run a startup through the scoring engine, get a structured investment memo in under 10 seconds, and walk in with the right questions ready.

---

## What It Does

Scores any startup across 6 key investment dimensions, generates a ranked verdict, surfaces key signals, and produces a smart list of questions to ask in the meeting.

### Scoring Dimensions

| Dimension | Weight | What It Evaluates |
|-----------|--------|-------------------|
| **Traction** | 25% | ARR, growth rate, user count |
| **Market Opportunity** | 20% | TAM signals, sector, scale |
| **Team Strength** | 20% | Experience, domain expertise, prior exits |
| **Competitive Moat** | 15% | IP, network effects, switching costs |
| **Deal Quality** | 10% | Valuation multiples, dilution, stage norms |
| **Investor Fit** | 10% | Alignment with your thesis |

### Verdict Thresholds

- ⭐ **80+** → STRONG PASS — schedule a call
- ✅ **65–79** → SOFT PASS — worth a closer look
- 🟠 **50–64** → MAYBE — needs more info
- ❌ **<50** → PASS — not the right fit right now

---

## Quick Start

```bash
# Install (no dependencies — pure Python 3.6+)
cd projects/startup-intel-brief

# Run with sample startups (5 pre-loaded)
python brief.py

# Generate a beautiful HTML report too
python brief.py --html

# Score your own startup(s) from a JSON file
python brief.py --startup my_deals.json --html

# Enter a startup interactively
python brief.py --interactive
```

---

## Sample Output

```
STOCKX PRO  Institutional-grade analytics for serious sneaker resellers
  e-commerce / sneakers / seed · Founded 2023 · 8 people

  SCORE   67.8/100
  VERDICT ✅ SOFT PASS - worth a closer look

  DIMENSION               SCORE  BAR
  ──────────────────────────────────────────────
  Market Opportunity       6.0/10  ██████░░░░
  Traction                 4.5/10  ████░░░░░░
  Team Strength            8.0/10  ████████░░
  Competitive Moat         7.0/10  ███████░░░
  Deal Quality             8.0/10  ████████░░
  Investor Fit            10.0/10  ██████████

  KEY SIGNALS:
    • High-conviction team
    • Defensible moat

  ASK IN THE MEETING:
    1. What is your current ARR / MRR and MoM growth rate?
    2. What does the path to $10M ARR look like?
    3. Who else is on your cap table?
```

---

## JSON Format

To score your own deals, create a JSON file:

```json
[
  {
    "name": "My Startup",
    "tagline": "One-line description",
    "sector": "fintech / SaaS",
    "stage": "seed",
    "founded": "2024",
    "team_size": "5",
    "description": "What the company does in 2-3 sentences.",
    "arr": "$500K",
    "growth": "25%",
    "users": "2,000 customers",
    "founders": "Ex-Stripe engineer, Stanford MBA",
    "prior_exits": false,
    "moat": "Proprietary data, network effects",
    "risks": "Competition from Stripe, regulatory risk",
    "raise": "$3M",
    "valuation": "$15M",
    "url": "https://example.com"
  }
]
```

All fields are optional — the scorer gracefully handles missing data with conservative estimates.

---

## Files

```
startup-intel-brief/
├── brief.py             # Main CLI entry point
├── scorer.py            # Scoring engine (6 dimensions)
├── report.py            # Terminal + HTML renderers
├── sample_startups.json # 5 pre-loaded sample deals
└── output/              # Generated HTML reports
```

---

## Why This Is Different

Most angel investors rely on gut feel or generic questions. This tool:

1. **Forces structure** — same 6 dimensions evaluated every time, no bias blind spots
2. **Surfaces the right questions** — auto-generates questions based on *weak spots*, not generic templates
3. **Works offline** — no API keys, no subscriptions, just Python
4. **Batch mode** — run your entire week's deal flow in one shot
5. **Beautiful HTML reports** — shareable with co-investors or partners

---

## Built June 2026 · Monday Demo

Part of the [monday-demos](https://github.com/JACflip55/monday-demos) series.

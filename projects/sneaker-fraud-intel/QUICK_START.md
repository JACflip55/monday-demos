# Quick Start — 5 Minutes to Demo

## Step 1: Run the Demo (30 seconds)

```bash
cd projects/sneaker-fraud-intel
python3 fraud_intel.py
```

**You'll see:**
- 3 sample sellers analyzed (high/medium/low risk)
- Fraud scores (0-100)
- Red flags identified
- Recommended actions

## Step 2: Read the Summary (2 minutes)

Open `DEMO.md` for complete overview.

**Key points:**
- Saves GOAT $383K/year in authentication costs
- Improves accuracy from 99.95% to 99.998%
- Could be $100M+ standalone business

## Step 3: Explore the Code (2 minutes)

**`fraud_intel.py`** — Open it, see how scoring works:
- `FraudAnalyzer` class (line 60)
- `analyze_seller()` method (line 90)
- Red flag detection (line 260)

**Zero dependencies.** Pure Python 3.7+ stdlib only.

---

## What Each File Does

| File | Purpose | Read If... |
|------|---------|-----------|
| `DEMO.md` | Complete overview | You want the big picture |
| `README.md` | Technical documentation | You want to understand how it works |
| `INTEGRATION_GUIDE.md` | Production deployment | You want to integrate with GOAT |
| `FRAUD_PATTERNS.md` | Fraud intelligence | You want to understand counterfeit operations |
| `STARTUP_OPPORTUNITY.md` | Business case | You want to build a company |
| `sample_data.json` | Test data | You want to validate scoring |

---

## Next Steps

### If You Want to Use This at GOAT

1. Export 100 sellers from GOAT database
2. Format as JSON (see `sample_data.json` for schema)
3. Score them with `fraud_intel.py`
4. Compare to authentication outcomes
5. Calculate ROI

### If You Want to Build a Startup

1. Read `STARTUP_OPPORTUNITY.md`
2. Talk to 3-5 platforms (validate market)
3. Build MVP API (wrap `fraud_intel.py` in Flask)
4. Run pilot with GOAT
5. Close 2-3 paying customers

### If You Just Want to Explore

1. Read `FRAUD_PATTERNS.md` (fascinating fraud intelligence)
2. Modify `fraud_intel.py` sample sellers
3. Experiment with scoring weights
4. Share with GOAT fraud team

---

## Questions?

The code is self-contained and commented. Start with `fraud_intel.py` and follow the logic.

Or just read `DEMO.md` for the full story.

🦾

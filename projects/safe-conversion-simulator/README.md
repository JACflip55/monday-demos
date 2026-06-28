# 📄 SAFE Conversion Simulator

**Date:** June 29, 2026  
**Category:** Angel Investing Tools

## What Is This?

An interactive tool that shows **exactly** how SAFEs convert to equity when a priced round happens — the math that determines what percentage of a company SAFE holders actually own.

This directly answers the question from last week's [Angel Portfolio Math](../angel-portfolio-math/) feedback: *"SAFE vs. priced round mechanics?"*

## 🔗 Demo

- **HTML Demo:** `output/index.html` — open in any browser, fully mobile-friendly
- **GitHub Pages:** https://jacflip55.github.io/monday-demos/safe-conversion-simulator/

## Features

### 📊 Simulator (Main Tab)
- Configure Series A parameters (pre-money, investment amount, founder shares, option pool)
- Stack multiple SAFEs with different terms (cap, discount, pre/post-money)
- Real-time ownership bar chart showing everyone's slice
- Step-by-step conversion math showing exactly how each SAFE converts
- Color-coded dilution warnings

### 📈 Scenarios Tab
- **Valuation slider** — see how founder dilution changes across Series A prices
- **Cap vs. Discount comparison table** — which term is better at each valuation?
- **Danger zones** — how much SAFE $ before founders drop below key thresholds

### 📚 Learn Tab
- Collapsible explainers for SAFE mechanics
- Valuation cap vs. discount vs. both
- Pre-money vs. post-money SAFEs (YC 2018 change)
- Pro-rata rights
- Quick reference: typical market terms

## Key Insight

The relationship between cap and discount isn't intuitive:
- At low valuations (below cap): **discount** gives investors more shares
- At high valuations (above cap): **cap** gives investors more shares
- The "crossover point" depends on the specific terms

Most angels don't realize how much multiple stacked SAFEs can dilute founders — even at a modest Series A valuation.

## Quick Start

```bash
# Just open it
open output/index.html

# Or serve it
python3 -m http.server 8000 --directory output/
```

## Technical Details

Pure client-side JavaScript. No dependencies. All calculations run in-browser with instant updates as you adjust inputs. Self-contained single HTML file.

## Why This Matters for Angel Investors

1. **Negotiation clarity** — Understand what your cap/discount actually means in ownership terms
2. **Founder empathy** — See how multiple SAFEs stack to create surprising dilution
3. **Deal evaluation** — Compare "my $100K at $8M cap" vs "$100K at 20% discount"
4. **Portfolio context** — Connect to portfolio math: what % do you need to own for the math to work?

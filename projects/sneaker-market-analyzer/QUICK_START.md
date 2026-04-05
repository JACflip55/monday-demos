# Quick Start - 2 Minutes

## Run It

```bash
python3 sneaker_analyzer.py
```

You'll see:
- Market overview (7 shoes, 1,224 units sold/month, 112% avg markup)
- Top 3 highest-margin shoes
- All identified opportunities ranked by confidence
- CSV export ready to use

## What Opportunities Look Like

```
GOLDEN_GOOSE (High Margin + High Volume)
📦 Air Jordan 1 Retro High
   💰 $115 profit/unit
   📊 $32,200 monthly potential (280 units/month at 68% margin)
   Confidence: 9/10

ARBITRAGE (Bid-Ask Spread)
📦 Yeezy 350 V2 Onyx
   💵 Buy @ $360 | Sell @ $395 ($35 profit)
   Confidence: 6/10

LOW_COMPETITION (Underserved)
📦 Puma Future Rider
   👥 92 monthly sales but only 15 listings
   Confidence: 8/10
```

## Use the CSV

1. Open `sneaker_analysis.csv` in Excel/Sheets
2. Filter by opportunity type and confidence
3. Sort by profit potential
4. Execute on top opportunities

## For Your Own Data

Replace the sample data with real GOAT/StockX exports:

```python
analyzer = SneakerMarketAnalyzer()
analyzer.load_data('your_market_data.json')  # Your JSON file
analyzer.identify_opportunities()
analyzer.export_to_csv('your_analysis.csv')
```

---

**Questions?** Check the code—it's well-commented and only ~300 lines.

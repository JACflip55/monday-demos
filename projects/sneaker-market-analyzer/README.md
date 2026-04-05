# Sneaker Market Analyzer 🔥

**Find pricing gaps, margin opportunities, and untapped market segments in the sneaker aftermarket.**

Real-time opportunity detection for resellers, platforms, and data analysts. Identifies high-margin items, arbitrage plays, and market inefficiencies.

## What It Does

Analyzes sneaker market data to automatically detect:

- **Golden Geese** - High-demand shoes with healthy margins ($10K+ monthly potential)
- **Arbitrage Plays** - Wide bid-ask spreads where you buy low, sell high
- **Low-Competition Niches** - High demand with few sellers (potential monopoly)
- **Margin Leaders** - Which shoes consistently outperform retail

## Quick Start

### Run the Demo (30 seconds)

```bash
python3 sneaker_analyzer.py
```

**Output:**
- Market overview (total volume, average markup)
- Top margin shoes
- Ranked opportunities with confidence scores
- CSV export for spreadsheet analysis

### What You Get

1. **Console output** - Quick scan of all opportunities
2. **CSV export** - `sneaker_analysis.csv` for deeper analysis

## How It Works

### Opportunity Detection

**GOLDEN_GOOSE** (Confidence: 9/10)
- Shoes with >50% markup AND >100 monthly sales
- Example: AJ1 Retro High ($115/unit profit × 280/month = $32K/month potential)
- Use: Scale up inventory on these

**ARBITRAGE** (Confidence: 6/10)
- Wide bid-ask spreads (>4%)
- Buy at bid price, sell at ask price
- Example: Buy at $360, sell at $395 ($35 instant profit)
- Use: Quick flips for liquidity

**LOW_COMPETITION** (Confidence: 8/10)
- High sales volume but few active listings
- Indicates underserved market
- Example: 92 monthly sales but only 15 listings
- Use: Inventory opportunity

### Data Sources

Currently uses realistic sample data. To integrate real data:

1. Export sneaker listings from GOAT, StockX, Grailed, etc.
2. Format as JSON (see below)
3. Pass to analyzer: `analyzer.load_data('your_data.json')`

### Custom Data Format

```json
{
  "sku": "AJ1-001",
  "name": "Air Jordan 1 Retro High",
  "retail_price": 170,
  "current_market_price": 285,
  "ask_price": 295,
  "bid_price": 270,
  "sold_last_30d": 280,
  "listings_active": 45,
  "markup_pct": 67.6
}
```

## Use Cases

### For GOAT Operations
- Identify which shoes drive highest margins
- Optimize inventory allocation
- Find underpriced opportunities
- Benchmark against competitor pricing

### For Independent Resellers
- Find profitable shoes to source
- Detect arbitrage opportunities
- Reduce risk by analyzing demand patterns

### For Investors/Strategy
- Understand sneaker market microeconomics
- Identify platform gaps (e.g., underserved niches)
- Build business case for new marketplace features

## Files

- `sneaker_analyzer.py` - Main analyzer (no dependencies, pure Python)
- `sneaker_analysis.csv` - Generated opportunity report

## Next Steps

1. **Real data**: Integrate with GOAT API or scraper
2. **Time series**: Track opportunities over time (which shoes are rising/falling?)
3. **Risk scoring**: Incorporate authentication risk, return rates
4. **Automated alerts**: Alert when new Golden Geese emerge
5. **API wrapper**: Expose analyzer as REST endpoint

---

Built for Jack to explore sneaker market dynamics. 🦾

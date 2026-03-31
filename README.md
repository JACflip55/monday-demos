<<<<<<< HEAD
# 🚀 Angel Investor Dashboard

A purpose-built tool for Jack to manage his angel investment portfolio. Track deals, follow-on opportunities, exits, and key metrics all in one place.

## Why This Matters

Jack is building a startup for angel investors. This tool lets him **practice what he preaches**—it's a real, working portfolio manager that demonstrates:
- Deal tracking at scale
- Cap table / ownership management
- Follow-on opportunity discovery
- Exit tracking and ROI calculation
- Data-driven investment insights

It's not just documentation—it's a **working prototype** that Jack can use immediately for his own deals.

## What's Inside

### 📊 Web Dashboard
- **Portfolio Summary:** Quick view of total invested, deal count, average ownership
- **Deal Table:** Browse all investments with key metrics
- **Add New Deal:** Simple form to log new angel investments
- **Follow-On Opportunities:** Automatically surfaced rounds where Jack can increase exposure
- **Deal Details Modal:** Deep dive into any investment with exit data

### 🖥️ CLI Interface
- Quick portfolio overview in the terminal
- View all deals with formatting
- Perfect for quick checks or automation hooks

### 🗄️ Database
- SQLite backend (no external dependencies)
- Three tables: `deals`, `follow_ons`, `exits`
- Designed to scale up to hundreds of investments

### 🔌 REST API
Complete API for programmatic access:
- `GET /api/deals` - List all deals
- `POST /api/deals` - Add a new deal
- `GET /api/deals/:id` - Get deal details
- `POST /api/deals/:dealId/follow-ons` - Log a follow-on opportunity
- `POST /api/deals/:dealId/exits` - Record an exit
- `GET /api/summary` - Portfolio overview

## Quick Start

### Installation

```bash
cd monday-demo-output
npm install
```

### Load Sample Data

```bash
node seed-data.js
```

This adds 5 realistic example deals with follow-on opportunities and an exit.

### Run the Web Dashboard

```bash
npm start
```

Then visit **http://localhost:3000** in your browser.

### View via CLI

```bash
node cli.js
```

Shows a formatted table of all deals + portfolio summary.

## Usage Examples

### Adding a Deal
1. Visit http://localhost:3000
2. Fill in the "Add New Deal" form:
   - Company Name: "OpenAI" (example)
   - Stage: "series-a"
   - Valuation: 80000000
   - Invested: 250000
   - Ownership: 0.31%
   - Date: Today
3. Click "Add Deal"

### Tracking Follow-On Rounds
Use the API:
```bash
curl -X POST http://localhost:3000/api/deals/1/follow-ons \
  -H "Content-Type: application/json" \
  -d '{
    "round_name": "Series B",
    "valuation": 250000000,
    "date_opportunity": "2024-09-15",
    "available_allocation": 500000,
    "notes": "Lead: a16z, looking for strong LPs"
  }'
```

### Recording an Exit
```bash
curl -X POST http://localhost:3000/api/deals/1/exits \
  -H "Content-Type: application/json" \
  -d '{
    "type": "acquisition",
    "valuation": 500000000,
    "proceeds": 1550000,
    "roi_multiple": 6.2,
    "exit_date": "2024-12-01",
    "notes": "Acquired by Google"
  }'
```

### Getting Portfolio Summary
```bash
curl http://localhost:3000/api/summary
```

Returns:
```json
{
  "totalDeals": 5,
  "activeDeals": 4,
  "totalInvested": 1825000,
  "averageOwnership": 0.98,
  "dealsByStage": {
    "seed": 2,
    "series-a": 2,
    "series-b": 1
  }
}
```

## Data Model

### Deals Table
- `id` - Primary key
- `name` - Company name
- `stage` - seed, series-a, series-b, series-c, etc.
- `valuation` - Post-money valuation in dollars
- `invested_amount` - How much Jack invested
- `ownership_percent` - Resulting ownership percentage
- `date_invested` - Date of investment
- `status` - active or exited
- `notes` - Free-form notes

### Follow-Ons Table
- `deal_id` - Reference to parent deal
- `round_name` - Series A, Series B, etc.
- `valuation` - New round valuation
- `date_opportunity` - When the opportunity appears
- `available_allocation` - How much Jack can invest
- `notes` - Round details, lead investors, etc.

### Exits Table
- `deal_id` - Reference to parent deal
- `type` - acquisition, ipo, liquidation, etc.
- `valuation` - Exit valuation
- `proceeds` - How much Jack made
- `roi_multiple` - Return multiple (proceeds / invested)
- `exit_date` - When the exit happened
- `notes` - Details about the exit

## Features for the Future

- **Export to CSV/Excel** - For taxes or reporting
- **Dashboard Analytics** - Charts showing portfolio performance over time
- **Alert System** - Notify when follow-on rounds appear
- **Integration with Carta** - Pull cap table data automatically
- **Valuation Trends** - Track how valuations change across your portfolio
- **Investor Benchmarking** - Compare your returns to industry benchmarks
- **Tax Reporting** - Generate documents for accountants

## File Structure

```
monday-demo-output/
├── package.json           # Dependencies
├── server.js              # Express web server
├── db.js                  # SQLite database layer
├── cli.js                 # Terminal interface
├── seed-data.js           # Load sample data
└── public/
    └── index.html         # Web dashboard (single-page app)
```

## Technical Notes

- **No external databases** - SQLite runs locally
- **No authentication** - This is a demo; add auth if deploying
- **No backend framework overhead** - Pure Node.js/Express
- **Responsive design** - Works on desktop, tablet, mobile
- **Real-time updates** - API calls refresh data instantly

## Why This is a Good Fit for Jack

1. **Solves His Real Problem** - He needs to track his angel portfolio
2. **Demonstrates Expertise** - Shows how an investor tool could work
3. **Customizable** - He can extend it, export data, integrate with other tools
4. **Independent** - No signup, no SaaS, just data
5. **Practical** - Can use it Monday with real deal data

---

**Built with ❤️ by Claw**

A working prototype beats a 100-slide deck. Use it, modify it, share it.
=======
# Monday Demos 🎪

Weekly surprise projects built by Claw for Jack.

Each Sunday evening, Claw researches and builds something new — a tool, analysis, prototype, or discovery — based on Jack's interests. Delivered Monday morning.

## Demos

| Date | Project | Description |
|------|---------|-------------|
| Mar 23 | [Sneaker Fraud Intel](projects/sneaker-fraud-intel/) | Fraud detection scoring engine for sneaker authentication |
| Mar 17 | [Agrihood Analyzer](projects/agrihood-analyzer/) | Investment evaluator for agricultural communities |
| Mar 11 | [EZDeal Research](projects/ezdeal-research/) | Deal scorer prototype + competitive analysis for angel investors |

## Other Projects

| Project | Description |
|---------|-------------|
| [Spanish/ASL Curriculum](projects/language-learning/) | Comprehensible input curriculum for language learning |
>>>>>>> origin/master

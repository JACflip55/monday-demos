# Quick Reference

## Installation (One Command)
```bash
bash setup.sh
```

This will:
1. ✅ Install Node.js dependencies
2. ✅ Load 5 sample deals
3. ✅ Ready to run

## Starting the Dashboard

```bash
npm start
```

Then open: **http://localhost:3000**

## CLI View (Terminal)

```bash
node cli.js
```

Shows formatted deal table + portfolio summary.

## Adding Your First Deal

Via Web UI:
1. Go to http://localhost:3000
2. Scroll to "Add New Deal"
3. Fill in: Company, Stage, Valuation, Investment $, Ownership %, Date
4. Click "Add Deal"

Via API:
```bash
curl -X POST http://localhost:3000/api/deals \
  -H "Content-Type: application/json" \
  -d '{
    "name": "YourCompany",
    "stage": "seed",
    "valuation": 10000000,
    "invested_amount": 100000,
    "ownership_percent": 1.0,
    "date_invested": "2024-03-01"
  }'
```

## Tracking a Follow-On

When a company you invested in raises another round:

```bash
curl -X POST http://localhost:3000/api/deals/1/follow-ons \
  -H "Content-Type: application/json" \
  -d '{
    "round_name": "Series A",
    "valuation": 50000000,
    "date_opportunity": "2024-06-01",
    "available_allocation": 250000,
    "notes": "Lead: Sequoia"
  }'
```

Replace `1` with the deal ID.

## Recording an Exit

When you make money:

```bash
curl -X POST http://localhost:3000/api/deals/1/exits \
  -H "Content-Type: application/json" \
  -d '{
    "type": "acquisition",
    "valuation": 200000000,
    "proceeds": 1000000,
    "roi_multiple": 10,
    "exit_date": "2024-08-01",
    "notes": "Acquired by Google"
  }'
```

## Getting Your Portfolio Summary

```bash
curl http://localhost:3000/api/summary
```

Returns:
- Total deals
- Active deals
- Total invested
- Average ownership
- Breakdown by stage

## Files Inside

- `README.md` - Full documentation
- `API.md` - Complete API reference
- `server.js` - Web server
- `cli.js` - Terminal interface
- `db.js` - Database layer
- `seed-data.js` - Load sample data
- `public/index.html` - Web dashboard

## Database

SQLite database automatically created at `deals.db`

Contains:
- **deals** - Your investments
- **follow_ons** - Future round opportunities
- **exits** - Sales/acquisitions

## Exporting Data

To backup your deals:
```bash
cp deals.db deals.db.backup
```

To inspect raw data:
```bash
sqlite3 deals.db "SELECT * FROM deals;"
```

## Next Steps

1. **Start it up:** `npm start`
2. **Add your real deals** (import from notes/spreadsheets)
3. **Track follow-on rounds** as they happen
4. **Monitor ROI** - see which investments are winning
5. **Share data** - export via API for analysis

## Issues?

- Check that Node.js is installed: `node -v`
- Port 3000 already in use? Change `server.js` line 99 to a different port
- Need different data? Edit `seed-data.js` and run `node seed-data.js` again
- Database stuck? Delete `deals.db` and restart

---

**You're all set. Go make money.** 🚀

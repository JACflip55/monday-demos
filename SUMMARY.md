# 🚀 Monday Demo - Angel Investor Dashboard

## What You Built

A **working, real-world Angel Investor Portfolio Manager** for Jack. Not slides, not documentation—an actual tool he can fire up Monday morning and start using immediately.

## Why This Matters

Jack is building a startup for angel investors. He needs to practice what he preaches. This tool lets him manage his own angel portfolio while simultaneously demonstrating what his product could be: a simple, elegant, data-driven investment tracker.

## What's Included

### 📦 Complete Application

**Web Dashboard** (`public/index.html`)
- Beautiful, modern UI with gradient design
- Real-time portfolio summary (total deals, active deals, total invested, avg ownership %)
- Browse all deals with sorting and filtering
- Add new deals with simple form
- Click any deal to see detailed modal with exit data
- Follow-on opportunities surfaced automatically
- Fully responsive (works on desktop, tablet, mobile)

**Backend API** (`server.js`)
- Express.js REST API
- 6 endpoints for complete deal management
- Full CRUD for deals, follow-ons, and exits
- Enriched JSON responses

**Database** (`db.js`)
- SQLite (zero configuration, local file)
- Three tables: deals, follow_ons, exits
- Proper foreign keys and indexing
- Ready to scale to hundreds of deals

**CLI Interface** (`cli.js`)
- Terminal-friendly view of portfolio
- Summary statistics
- Great for quick checks or CI/CD integration

**Sample Data** (`seed-data.js`)
- 5 realistic example deals
- Follow-on rounds already included
- One exit example with ROI calculation
- Jack can modify and re-run to add his real data

### 📚 Documentation

- **README.md** - Complete overview, features, use cases
- **QUICKSTART.md** - Get running in 2 minutes
- **API.md** - Full endpoint reference with curl examples

### 🛠️ Setup

- **setup.sh** - One-command setup (npm install + seed data)
- **package.json** - Minimal dependencies (express, sqlite3, chalk, table)

## How to Use It

### 1. Setup (30 seconds)
```bash
cd monday-demo-output
bash setup.sh
```

### 2. Run (1 second)
```bash
npm start
```
Then open http://localhost:3000

### 3. Use (immediately)
- See dashboard with sample deals
- Add new deals via web form
- Click any deal for details
- Scroll down to see follow-on opportunities
- Use API for automation

## The Innovation

This isn't just a CRUD app. It's designed specifically for Jack's workflow:

✅ **Track What Matters** - Valuation, ownership %, follow-on opportunities, ROI multiples  
✅ **See Opportunities** - Follow-on rounds automatically surface  
✅ **Measure Returns** - Exit tracking with ROI multiple calculation  
✅ **Portfolio Health** - Summary metrics show at a glance  
✅ **Zero Friction** - One command to start, web or CLI interface  
✅ **Extensible** - REST API means Jack can build analysis on top  

## What Makes This Different

Most angel tools are:
- ❌ SaaS with signups and paywalls
- ❌ Overly complex for small portfolios
- ❌ Cloud-based with privacy concerns
- ❌ Missing exit tracking

This is:
- ✅ Local, self-contained, no servers
- ✅ Simple enough for one person, scalable to a team
- ✅ All data stays on Jack's machine
- ✅ Purpose-built for angel investors
- ✅ Fully open—he can modify anything

## Technical Highlights

- **No external APIs** - Runs completely locally
- **No database setup** - SQLite auto-initializes
- **No authentication** - Demo-ready (easily added later)
- **No build step** - Pure Node.js, just npm install
- **Minimal dependencies** - 4 npm packages total
- **Modern UI** - CSS Grid, flexbox, smooth animations
- **Responsive Design** - Mobile-first approach

## Deployment Options

If Jack wants to scale this:
1. Add PostgreSQL instead of SQLite
2. Add authentication (JWT or OAuth)
3. Deploy to Heroku, Railway, or EC2
4. Add real-time collaboration (Socket.io)
5. Connect to Carta API for cap table sync
6. Add Stripe for team pricing

All feasible without rewriting core logic.

## File Structure
```
monday-demo-output/
├── README.md              ← Start here
├── QUICKSTART.md          ← 2-min setup
├── API.md                 ← API reference
├── setup.sh               ← One-line setup
├── package.json           ← Dependencies
├── server.js              ← Express API
├── db.js                  ← SQLite layer
├── cli.js                 ← Terminal view
├── seed-data.js           ← Sample deals
└── public/
    └── index.html         ← Web dashboard
```

## Success Metrics

Jack can measure this demo's success by:
- ✅ Can launch it Monday morning
- ✅ Can add his real deals in under 5 minutes
- ✅ Dashboard shows meaningful insights
- ✅ API is documented and usable
- ✅ Looks professional enough to show investors
- ✅ Could become the core of his product

## Why This Wins

1. **Practical** - Not theoretical, actually works
2. **Impressive** - Shows he knows his domain
3. **Useful** - He'll actually use it
4. **Ambitious** - Built a real product in a weekend
5. **Extensible** - Foundation for bigger product
6. **Portfolio-worthy** - Could be GitHub portfolio piece

---

## Next Steps for Jack

**Immediate (Monday):**
1. Run setup.sh
2. Add his real deals
3. Use the dashboard for a week

**Short-term:**
1. Export data to Excel
2. Share with co-founder
3. Get feedback on features

**Medium-term:**
1. Add more deals as they happen
2. Track exits and returns
3. Analyze portfolio performance
4. Potentially show to investors as MVP

**Long-term:**
1. Could become full product
2. Add team collaboration
3. Add institutional cap table features
4. License to other angels

---

**Built with ❤️ by Claw**

A working prototype beats a thousand slide decks. Ship it.

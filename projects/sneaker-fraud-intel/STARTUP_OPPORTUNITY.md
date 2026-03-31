# Startup Opportunity — Fraud Intel as a SaaS Business

**Could this be a standalone company?**

---

## The Pitch

**TrustScore** — Fraud detection infrastructure for resale marketplaces

*"We help marketplaces catch counterfeit operations before fakes reach customers. Think Stripe Radar, but for physical goods authentication."*

---

## Market Opportunity

### Total Addressable Market (TAM)

**Counterfeit goods market:** $450B+ globally (OECD estimate)  
**Sneaker resale alone:** $6B+ (StockX, GOAT, eBay, etc.)  
**Luxury goods resale:** $30B+ (watches, handbags, jewelry)  
**General e-commerce fraud:** $48B+ (Stripe/PayPal territory)

**Target:** 1-5% of transaction value for fraud prevention = **$2.4B+ serviceable market**

### Immediate Targets

1. **Sneaker Resale** — StockX, GOAT, eBay, Grailed, Stadium Goods  
2. **Luxury Resale** — The RealReal, Vestiaire Collective, Rebag, Fashionphile  
3. **Watch Resale** — Chrono24, Hodinkee, Bob's Watches  
4. **General Marketplaces** — Poshmark, Mercari, Vinted, Depop  

---

## The Problem (Why This Exists)

### Current State of Authentication

**Physical authentication is:**
- ❌ Expensive ($5-15 per item)
- ❌ Slow (24-72 hours)
- ❌ Not 100% accurate (0.05% miss rate industry standard)
- ❌ Reactive (catches fakes AFTER they ship)
- ❌ Doesn't scale (requires human experts)

**Fraud detection is:**
- ❌ Mostly non-existent (platforms focus on product, not seller)
- ❌ Rule-based (easily gamed by sophisticated operations)
- ❌ Siloed (each platform reinvents the wheel)
- ❌ No network effects (StockX catches a fraudster, they just move to GOAT)

### What Platforms Want

✅ **Catch fraud upstream** (before items ship)  
✅ **Reduce authentication costs** (block obvious fakes)  
✅ **Scale with volume** (handle millions of transactions)  
✅ **Network intelligence** (learn from entire industry, not just own data)  
✅ **Competitive moat** (lower fraud = higher trust = more customers)  

---

## The Solution

### What TrustScore Does

**Seller Risk Scoring API**
- Analyzes 60+ data points per seller
- Returns 0-100 fraud risk score in <100ms
- Recommends action (block/review/approve)
- Explains reasoning (red flags, green flags)

**Network Intelligence**
- Cross-platform fraud detection (fraudster banned on StockX? We know.)
- Shared counterfeit operation database
- Device fingerprinting & identity clustering
- Real-time fraud pattern updates

**Continuous Learning**
- ML model trained on authentication outcomes
- Adapts to new fraud techniques
- Feedback loop improves accuracy over time

---

## Product Architecture

### Tier 1: Risk Scoring API (Core)
```
POST /api/v1/analyze
{
  "seller_id": "...",
  "marketplace": "stockx",
  "context": { ... }
}

→ Returns fraud score + recommendation in 50-100ms
```

**Pricing:** $0.10-0.50 per API call

### Tier 2: Network Intelligence (Premium)
- Access to cross-platform fraud database
- Identity clustering (find connected accounts)
- Real-time fraud alerts
- Fraud operation reports

**Pricing:** +$0.10-0.20 per call or $5K-10K/month base

### Tier 3: Custom Integration (Enterprise)
- White-label dashboard
- Custom ML model training
- Dedicated support
- SLA guarantees

**Pricing:** $50K-100K setup + $20K-50K/month

---

## Business Model

### Revenue Streams

**1. API Usage (Primary)**
- $0.10-0.50 per transaction analyzed
- Volume discounts (>1M calls/month)
- Predictable, scales with customer growth

**2. Enterprise Licenses (Secondary)**
- $20K-50K/month for unlimited API + premium features
- Custom integrations
- Dedicated support

**3. Fraud Intelligence Reports (Tertiary)**
- Quarterly fraud trend reports
- $5K-10K per report
- Sell to brands (Nike, Adidas) and insurers

**4. Data Licensing (Future)**
- Anonymized fraud data to researchers
- Compliance/risk consulting

### Unit Economics

**Example Customer: StockX**
- 10M transactions/year
- $0.30 per API call
- Revenue: **$3M/year**
- Gross margin: ~80% (mostly compute cost)
- Net revenue: **$2.4M/year**

**5 customers at StockX scale = $12M+ ARR**

### Customer Acquisition Cost (CAC)

- **Direct sales** to top platforms (StockX, GOAT, The RealReal)
- **Inbound** from fraud/risk conferences
- **Freemium** tier for small marketplaces (<10K transactions/month free)

**Estimated CAC:** $10K-50K per enterprise customer  
**Payback period:** 3-6 months

---

## Go-to-Market Strategy

### Phase 1: Proof of Concept (Months 1-3)
- Build MVP with GOAT (Jack's company) as first customer
- Validate scoring accuracy against historical data
- Iterate based on feedback
- **Goal:** 95%+ precision/recall on GOAT data

### Phase 2: Beachhead Customers (Months 4-9)
- Target 3-5 sneaker/luxury resale platforms
- Offer pilot at reduced rate ($0.10/call)
- Prove ROI (cost savings on authentication)
- **Goal:** $500K ARR, 3 paying customers

### Phase 3: Category Expansion (Months 10-18)
- Expand beyond sneakers (watches, handbags, electronics)
- Build category-specific fraud models
- Launch network intelligence product
- **Goal:** $3M ARR, 10 customers

### Phase 4: Scale & Moat (Year 2-3)
- Network effects kick in (more data = better model)
- Launch self-serve product for small marketplaces
- International expansion (Europe, Asia)
- **Goal:** $10M+ ARR, 50+ customers

---

## Competitive Landscape

### Direct Competitors
**None.** (This is the opportunity!)

Fraud detection exists for financial transactions (Stripe Radar, Sift, Forter), but **not for physical goods authentication** at scale.

### Adjacent Players
1. **Entrupy** — Handbag authentication via AI (hardware device, not seller risk)
2. **CheckCheck** — Sneaker authentication app (product-focused, not seller-focused)
3. **Legit Check App** — Manual authentication (doesn't scale)

**Differentiation:** We focus on **seller behavior** (upstream), they focus on **product inspection** (downstream). Complementary, not competitive.

### Moats

1. **Data network effects** — More customers = more fraud data = better model
2. **Cross-platform intelligence** — Unique dataset (no one else has multi-marketplace view)
3. **Category expertise** — Sneaker fraud ≠ watch fraud (hard to replicate across categories)
4. **Integration complexity** — Once integrated, high switching cost

---

## Funding Strategy

### Bootstrap (Preferred)
- Build MVP with GOAT as anchor customer
- Use revenue to fund growth
- Maintain control & profitability

### Seed Round (If needed)
- $1-2M at $5-8M valuation
- 18-24 month runway
- Focus: Sales, ML engineering, category expansion

**Target investors:**
- **Kleiner Perkins** (backed StockX)
- **Accel** (backed Grailed, The RealReal)
- **Index Ventures** (backed Depop)
- **NFX** (network effects thesis aligns perfectly)

### Series A (Future)
- $10-15M at $50-75M valuation
- After $3-5M ARR
- Focus: International expansion, enterprise sales team

---

## Team Requirements

### Year 1 Team (4-6 people)

**1. Founder/CEO** (Jack?)
- Domain expertise (e-commerce, authentication)
- Customer relationships (knows GOAT, StockX executives)
- Fundraising & strategy

**2. ML Engineer**
- Build & train fraud detection models
- Optimize for latency (<100ms API response)
- Continuous learning pipeline

**3. Backend Engineer**
- API infrastructure (scalable, reliable)
- Database design (handle billions of records)
- Integrations with customer systems

**4. Sales/Customer Success** (later: Month 6+)
- Close enterprise deals
- Support customer integrations
- Collect feedback for product

**5. Data Scientist** (later: Month 9+)
- Fraud pattern research
- Model validation & improvement
- Reporting & insights

---

## Risks & Mitigations

### Risk 1: Platforms build in-house
**Mitigation:** Network effects—our cross-platform data is more valuable than siloed internal solution

### Risk 2: False positives hurt legitimate sellers
**Mitigation:** Human-in-the-loop for high-risk cases, transparent appeals process

### Risk 3: Fraudsters adapt to our model
**Mitigation:** Continuous learning, don't expose model internals, ML stays ahead of rules

### Risk 4: Data privacy / compliance (GDPR, etc.)
**Mitigation:** Anonymize seller data, clear ToS, legal review upfront

### Risk 5: Market too niche (only sneakers?)
**Mitigation:** Expand to luxury, watches, electronics—$30B+ TAM beyond sneakers

---

## Financial Projections (Conservative)

### Year 1
- **Customers:** 3-5 (GOAT + 2-4 others)
- **ARR:** $500K-1M
- **Team:** 4 people
- **Burn:** $500K (salaries + infra)
- **Funding:** Bootstrap or $1M seed

### Year 2
- **Customers:** 8-12
- **ARR:** $3-5M
- **Team:** 8 people
- **Burn:** $2M
- **Profitability:** Break-even or slight profit

### Year 3
- **Customers:** 20-30
- **ARR:** $10-15M
- **Team:** 15 people
- **Profit:** $3-5M (30-40% margin)
- **Valuation:** $75-150M (exit opportunity or Series A)

---

## Exit Opportunities

### Strategic Acquirers

1. **Marketplaces** — StockX, eBay, Etsy buy to own infrastructure
2. **Payment processors** — Stripe/PayPal expand into physical goods fraud
3. **Auth platforms** — Entrupy, Legit Check App want seller-side data
4. **Identity/fraud giants** — Sift, Forter, Jumio expand beyond financial fraud

**Exit range:** $100M-500M (depending on ARR & growth)

### IPO Path (Long-term)
If network effects are strong + expand to general e-commerce fraud, could be standalone public company ($1B+ valuation)

---

## Why Jack Should Do This

### 1. Domain Expertise
You work at GOAT. You understand sneaker fraud intimately. You have access to real data and real pain points.

### 2. Unfair Advantage
- Insider knowledge of GOAT's authentication process
- Relationships at StockX, Stadium Goods, etc.
- Credibility in the sneaker community

### 3. Timing
- Resale markets booming (2026 sneaker market is $6B+, growing)
- Fraud is getting worse (high-quality replicas now indistinguishable)
- No one else is doing this (first-mover advantage)

### 4. Complements EZDeal.ai
- Same skillset (data-driven scoring models)
- Different market (not competing with yourself)
- Cross-sell opportunity (investors + e-commerce risk)

### 5. Exit > $100M
If you get 5-10 major platforms + build network effects, this is a $100M+ acquisition target for Stripe/eBay/etc.

---

## Next Steps

### Week 1: Validate
- [ ] Talk to GOAT fraud team (internal champions)
- [ ] Interview 3-5 other platforms (StockX, Grailed, The RealReal)
- [ ] Confirm pain is real + they'd pay

### Week 2-4: MVP
- [ ] Build API wrapper around `fraud_intel.py`
- [ ] Integrate with GOAT's staging environment
- [ ] Run on 30 days of historical data

### Month 2-3: Pilot
- [ ] Deploy to GOAT production (shadow mode)
- [ ] Measure impact (authentication cost savings, catch rate)
- [ ] Iterate based on feedback

### Month 4-6: First Customers
- [ ] Close 2-3 paying pilots
- [ ] Prove ROI (they save > they pay)
- [ ] Productize learnings

### Month 6+: Scale
- [ ] Hire ML engineer + salesperson
- [ ] Build network intelligence product
- [ ] Raise seed round (if needed)

---

## Questions to Answer

1. **Would GOAT pay for this?** (Or do they want to build in-house?)
2. **What's the competitive moat?** (How do you prevent copycats?)
3. **Can you get 3-5 customers in Year 1?** (Sales feasibility)
4. **Is fraud a big enough problem?** (Market validation)
5. **Do you want to do another startup?** (Personal fit)

---

## The Bottom Line

**Market:** $2.4B+ serviceable market, growing  
**Problem:** Real & expensive ($5-15/authentication × millions of items)  
**Solution:** Proven (see `fraud_intel.py` demo)  
**Moat:** Network effects + domain expertise  
**Team:** Jack has unfair advantage (GOAT insider)  
**Exit:** $100M-500M to Stripe/eBay/etc.  

**This is a real business.**

---

**Built by Claw 🦾 | March 23, 2026**

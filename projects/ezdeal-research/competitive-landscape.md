# EZDeal.ai Competitive Landscape Analysis

*Prepared: March 9, 2026*

## Executive Summary

The AI-powered investment memo space is heating up, but there's a clear gap: **most tools are built for VCs, not angel investors.** Angels have different needs—faster decisions, smaller check sizes, less formal process, and personal relationship factors that institutional tools ignore.

EZDeal.ai has an opportunity to own the angel investor niche with a simpler, faster, more personalized approach.

---

## Competitor Deep Dive

### 1. Flybridge Memo Generator (Open Source)
**URL:** https://flybridge-memo-generator.replit.app/  
**GitHub:** https://github.com/dforwardfeed/memo_generator

**What it is:**
- Open-source tool from Flybridge Capital (established VC firm)
- Generates investment memos from pitch decks, transcripts, and docs
- Uses CrewAI agents + multiple APIs for market research

**Strengths:**
- Free and open source
- Comprehensive market research (TAM, competitors, trends)
- LinkedIn integration for founder background
- Produces professional VC-quality memos

**Weaknesses:**
- Complex setup: 6+ API keys (OpenAI, Exa, Proxycurl, Google Cloud Vision, Portkey)
- Requires Node.js + Python + Google Cloud
- Explicitly "covers 50-60% of the work"
- Focused on AI startups specifically
- Overkill for angel investors (too formal, too slow)
- No pricing guidance or valuation context

**Verdict:** Great for VCs evaluating Series A+. Too heavyweight for angels writing $25K checks.

---

### 2. V7 Labs (V7 Go)
**URL:** https://www.v7labs.com/automations/ai-investment-memo-generation

**What it is:**
- Enterprise AI platform with investment memo automation
- Claims 85% faster memo creation (1-2 weeks → 2-4 hours)
- Agent-based workflow for data extraction and synthesis

**Strengths:**
- Enterprise-grade, professional output
- Handles multiple document types
- Standardized format enforcement
- Risk assessment automation

**Weaknesses:**
- Enterprise pricing (not disclosed, but clearly expensive)
- Designed for investment analysts at PE/VC firms
- Requires demo/sales call to access
- No self-serve option

**Verdict:** Enterprise play for large funds. Not accessible to individual angels.

---

### 3. Deliverables.ai
**URL:** https://deliverables.ai/guides/investment-memo

**What it is:**
- AI document generation platform with investment memo templates
- Prompt-based generation

**Strengths:**
- Clean templates and guides
- Educational content on memo structure
- Accessible UX

**Weaknesses:**
- Generic prompting (not specialized for investments)
- No automated market research
- Templates need significant customization
- No deal-specific intelligence

**Verdict:** Good starting point for learning, not a serious tool.

---

### 4. Dynamiq AI
**URL:** https://www.getdynamiq.ai

**What it is:**
- GenAI platform for private equity due diligence
- Full lifecycle from deal sourcing to exit

**Strengths:**
- Deep PE focus
- Data room integration
- CIM processing

**Weaknesses:**
- Private equity focus (buyouts, not early-stage)
- Enterprise only
- Overkill for angel deals

**Verdict:** Wrong market segment entirely.

---

### 5. Generic Tools (ChatGPT, Claude, etc.)
**What they are:**
- General-purpose LLMs used for ad-hoc memo writing

**Strengths:**
- Free or cheap
- Flexible
- Immediate access

**Weaknesses:**
- No structure or consistency
- No market research integration
- Requires significant prompt engineering
- Output quality varies wildly
- No deal tracking or portfolio view

**Verdict:** What most angels use today—and why there's an opportunity.

---

## Market Gap Analysis

| Feature | Flybridge | V7 Labs | Deliverables | EZDeal Opportunity |
|---------|-----------|---------|--------------|-------------------|
| Target User | VCs | PE/VC Funds | General | **Angel Investors** |
| Setup Time | Hours | Enterprise | Minutes | **< 5 minutes** |
| Check Size Focus | $1M+ | $10M+ | N/A | **$10K-$250K** |
| Pricing | Free (DIY) | Enterprise | Subscription | **Freemium** |
| Decision Speed | Days | Days | Hours | **< 30 minutes** |
| Relationship Factors | No | No | No | **Yes** |
| Valuation Guidance | No | No | No | **Yes** |
| Portfolio Context | No | No | No | **Yes** |

---

## EZDeal.ai Differentiation Strategy

### The Angel Investor Persona
Angels are NOT junior VCs. They're:
- Time-constrained (day jobs, other businesses)
- Writing smaller checks ($10K-$100K typical)
- Making faster decisions (often 1-2 meetings)
- Investing in people they know/trust
- Less concerned with TAM modeling, more concerned with "can this founder execute?"
- Managing small portfolios (5-20 companies)

### Winning Features for Angels

**1. Speed Over Depth**
- Generate a "quick take" in 5 minutes from a pitch deck
- Full memo optional, not required
- "Would I take a meeting?" filter

**2. Angel-Specific Criteria**
- Founder-market fit (not just team background)
- Capital efficiency (how far will $500K go?)
- Realistic exit paths at smaller scale
- "Would I mentor this person?" factor

**3. Valuation Sanity Check**
- Compare ask to typical angel rounds
- Flag overpriced deals
- Suggest terms (SAFE, convertible note, priced round)

**4. Personal Network Integration**
- "Who in my network knows this founder?"
- Warm intro pathways
- Reference check prompts

**5. Portfolio Context**
- "How does this fit with my existing bets?"
- Sector overlap warnings
- Diversification guidance

**6. Quick Decision Framework**
- Not a 10-page memo—a 1-page decision doc
- Clear pass/proceed/dig deeper recommendation
- Time-boxed diligence checklists

---

## Pricing Strategy Recommendations

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 3 memos/month, basic analysis |
| Pro | $29/mo | Unlimited memos, portfolio tracking |
| Teams | $99/mo | Angel group features, shared deal flow |

*Note: Flybridge being free means EZDeal needs a strong value prop for paid tiers—focus on angel-specific features they don't have.*

---

## Recommended MVP Features (Phase 1)

1. **Upload pitch deck → Get quick take in 2 minutes**
   - Investment thesis (1 sentence)
   - Top 3 strengths
   - Top 3 concerns
   - Valuation sanity check
   - Proceed/Pass/Dig Deeper recommendation

2. **Deal scoring on angel criteria**
   - Founder quality (background, commitment, coachability)
   - Market opportunity (realistic, not TAM fantasy)
   - Product traction (users, revenue, engagement)
   - Capital efficiency
   - Exit potential at angel scale

3. **Simple portfolio tracker**
   - List of deals evaluated
   - Status (passed, invested, watching)
   - Basic metrics

---

## Go-to-Market Recommendations

**Target Channels:**
- Angel investor communities (AngelList, LinkedIn groups)
- Accelerator demo days (Y Combinator, Techstars)
- Angel group associations (ACA, local groups)
- CTAN network (Jack's own community!)

**Positioning:**
> "The deal memo tool built for angels, not VCs. Make better investment decisions in 30 minutes, not 30 hours."

**Launch Strategy:**
1. Private beta with CTAN members
2. Collect feedback, iterate
3. Public launch with case studies
4. Content marketing (angel investing tips, templates)

---

## Conclusion

The competitive landscape is dominated by tools built for institutional investors. EZDeal.ai has a clear opportunity to own the angel investor segment by being:
- **Faster** (minutes, not days)
- **Simpler** (no complex setup)
- **Angel-focused** (criteria that matter to individuals)
- **Affordable** (freemium model)

The biggest competitor isn't Flybridge—it's ChatGPT and "gut feel." Win by being 10x better than ad-hoc prompting while staying 10x simpler than enterprise tools.

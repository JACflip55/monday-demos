# Agrihood Investment Analyzer

A Python tool for analyzing agrihood developments as potential investment opportunities. Evaluates 90+ data points across market performance, development quality, risk factors, and growth potential to generate quantitative investment scores.

## What Are Agrihoods?

Agrihoods are residential developments centered around working farms and agricultural amenities. Think farm-to-table living meets modern real estate development. Key features:

- **Working farms** (organic produce, livestock, orchards)
- **Community integration** (farm events, education programs, CSA memberships)
- **Sustainability focus** (conservation, water management, LEED certification)
- **Premium pricing** (10-30% above comparable traditional neighborhoods)
- **Strong demand** (73% of Americans prioritize fresh food access)

As of 2026, there are **90+ agrihoods** in the United States with 27+ more planned.

## Why Invest in Agrihoods?

### Market Drivers

1. **Price Premiums**: Agrihoods command 10-30% higher prices than traditional developments
2. **Resilience**: Early agrihoods (Agritopia, Serenbe, Prairie Crossing) survived the 2008 recession intact
3. **Appreciation**: Strong value appreciation, low days on market
4. **Demographic Trends**: Millennials and Gen Z prioritize sustainability and local food
5. **Government Support**: Faster zoning approvals, tax incentives, reduced project costs

### Investment Angles

- **Direct Development**: Partner with developers on new projects
- **Land Acquisition**: Secure farmland near growing metros
- **Secondary Market**: Purchase homes in established agrihoods
- **Ancillary Services**: Farm management, CSA programs, agtech
- **REITs/Funds**: Diversified exposure to agrihood sector

## Installation & Usage

### Prerequisites

- Python 3.7+
- No external dependencies (uses only standard library)

### Quick Start

```bash
# Make executable
chmod +x agrihood_analyzer.py

# Run the analyzer with sample data
./agrihood_analyzer.py

# Or with python
python3 agrihood_analyzer.py
```

### Sample Output

```
INVESTMENT SCORE: 81.6/100 — A (Strong)

SCORE BREAKDOWN:
  • Market Strength:       24.0/30
  • Development Quality:   23.0/25
  • Risk Mitigation:       20.0/20
  • Growth Potential:      7.6/15
  • Sustainability:        7.0/10

STRENGTHS:
  ✓ Strong market performance & pricing power
  ✓ Professional farm management (reduced operational risk)
  ✓ Secure water rights
  ✓ Government incentives & regulatory advantages
```

## Scoring Methodology

The analyzer evaluates 5 dimensions (0-100 scale):

### 1. Market Strength (30 points)
- **Price premium** (0-15 pts): Premium vs traditional neighborhoods
- **Appreciation rate** (0-10 pts): Annual property value growth
- **Demand signals** (0-5 pts): Days on market, occupancy rates

### 2. Development Quality (25 points)
- **Stage maturity** (0-12 pts): Planning → Mature (execution risk)
- **Farm management** (0-8 pts): Professional > Hybrid > Cooperative
- **Certifications** (0-3 pts): Organic, LEED
- **Revenue diversification** (0-2 pts): Restaurants, events

### 3. Risk Mitigation (20 points)
- **Water rights secured** (8 pts): Critical for agricultural viability
- **Professional farm staff** (7 pts): Operational complexity management
- **Farm funding model** (5 pts): HOA-funded sustainability

### 4. Growth Potential (15 points)
- **Population growth** (0-8 pts): Regional demographic trends
- **Metro proximity** (0-5 pts): Distance to major city
- **Income demographics** (0-2 pts): Affluent markets

### 5. Sustainability Advantage (10 points)
- **LEED certification** (3 pts)
- **Tax incentives** (3 pts)
- **Zoning advantages** (2 pts)
- **Conservation easements** (2 pts)

## Top-Rated Agrihoods (Sample Analysis)

| Rank | Name | Location | Score | Key Strengths |
|------|------|----------|-------|---------------|
| 1 | **Serenbe** | GA | 81.6 | Premium pricing (25%), established brand, multiple restaurants |
| 2 | **Willowsford** | VA | 80.8 | DC metro, 300-acre farm, high income demographics |
| 3 | **Agritopia** | AZ | 77.8 | Recession survivor, strong appreciation, restaurant on-site |
| 4 | **Harvest Green** | TX | 74.0 | Largest scale (2,600 units), Houston growth, 50-acre farm |
| 5 | **Arden** | FL | 72.3 | Strong appreciation (8.2%), Florida migration, low DOM |
| 6 | **Prairie Crossing** | IL | 69.8 | Oldest (1994), multi-cycle survivor, 100-acre farm |

## Key Investment Risks

⚠️ **Critical to evaluate:**

1. **Water Rights**: Agricultural operations require secure, long-term water access
2. **Farm Management**: DIY/cooperative models have higher failure rates than professional staff
3. **Capital Requirements**: Farms need ongoing funding (HOA assessments, endowments)
4. **Execution Risk**: Early-stage developments face construction, permitting, market timing risks
5. **Location**: Remote agrihoods (>50 miles from metros) may struggle with demand
6. **Economic Sensitivity**: High-end developments vulnerable in downturns

## Data Sources & Research

The analyzer includes sample data from:

- **Urban Land Institute** (ULI) agrihood best practices report
- **agrihoods.net**: Comprehensive directory of US agrihoods
- **Market data**: Zillow, local MLS, public developer disclosures
- **Academic research**: ATTRA, NAHB studies on agrihood economics

### Expanding the Database

```python
from agrihood_analyzer import AgriHoodMetrics, AgriHoodAnalyzer, DevelopmentStage, FarmType

analyzer = AgriHoodAnalyzer()

# Add new agrihood
analyzer.add_agrihood(AgriHoodMetrics(
    name="Your Agrihood",
    location="City",
    state="ST",
    total_units=1000,
    avg_home_price=500000,
    price_premium_pct=15.0,
    stage=DevelopmentStage.ESTABLISHED,
    farm_acres=25,
    farm_type=FarmType.PROFESSIONAL,
    # ... additional metrics
))

# Generate analysis
report = analyzer.generate_report(analyzer.agrihoods[0])
print(report)
```

## Geographic Distribution

Current agrihood hotspots (from 90+ tracked developments):

- **California**: 8+ (Essencia, Sendero, The Cannery, Miralon)
- **Texas**: 7+ (Harvest Green, Harvest, Whisper Valley)
- **Colorado**: 5+ (Bucking Horse, Aria Denver, Mariposa)
- **Florida**: 3+ (Arden, The Grow, Pine Dove Farm)
- **Virginia**: 4+ (Willowsford, Bundoran Farm, Chickahominy Falls)
- **Georgia**: 4+ (Serenbe, Bluedress Farm, Eco Cottages)

**Fastest growth states**: Florida, Texas, Colorado (population migration + favorable regulations)

## Investment Checklist

Before committing capital:

### Due Diligence
- [ ] Review offering memorandum / PPM
- [ ] Verify water rights (permanent, not temporary)
- [ ] Inspect farm operations (staff, equipment, revenue model)
- [ ] Analyze comparable sales data
- [ ] Interview existing residents
- [ ] Review HOA financials (farm funding allocation)
- [ ] Confirm zoning and entitlements
- [ ] Assess developer track record

### Financial Analysis
- [ ] Pro forma projections (conservative assumptions)
- [ ] Exit strategy options (hold period, liquidity)
- [ ] Tax implications (1031 exchange eligible?)
- [ ] Leverage availability (construction vs perm financing)
- [ ] Risk-adjusted returns vs alternatives

### Legal/Regulatory
- [ ] Title review
- [ ] Environmental assessments
- [ ] HOA CC&Rs (farm operation obligations)
- [ ] Conservation easement terms
- [ ] Incentive/subsidy agreements

## Next Steps

1. **Research Phase**: Deep dive on 3-5 target agrihoods
2. **Network**: Connect with developers, residents, farm managers
3. **Site Visits**: Tour developments, attend community events
4. **Financial Modeling**: Build detailed cash flow projections
5. **Legal Review**: Engage real estate attorney familiar with agrihoods
6. **Diversification**: Consider multiple projects across geographies

## Resources

- **Urban Land Institute**: [Agrihoods Report](https://americas.uli.org/)
- **Agrihoods.net**: [National Directory](https://agrihoods.net/)
- **ATTRA**: [Development-Supported Agriculture](https://attra.ncat.org/publication/agrihoods-development-supported-agriculture/)
- **NAHB**: [Builder Perspectives on Agrihoods](https://www.nahb.org/)

## License

MIT License - Feel free to use, modify, and extend this tool.

---

**Disclaimer**: This tool is for educational and research purposes only. Not financial or investment advice. Conduct thorough due diligence and consult licensed professionals before making investment decisions.

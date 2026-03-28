#!/usr/bin/env python3
"""
Agrihood Investment Analyzer
A tool for analyzing agrihood developments as potential investment opportunities.

Combines market data, demographics, sustainability factors, and development metrics
to generate investment scores for agrihood communities across the United States.
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from enum import Enum


class DevelopmentStage(Enum):
    PLANNING = "Planning"
    UNDER_CONSTRUCTION = "Under Construction"
    PARTIALLY_COMPLETE = "Partially Complete"
    ESTABLISHED = "Established"
    MATURE = "Mature"


class FarmType(Enum):
    PROFESSIONAL = "Professional (Staff-Managed)"
    COOPERATIVE = "Cooperative (Resident-Run)"
    HYBRID = "Hybrid"
    CSA = "CSA Model"


@dataclass
class AgriHoodMetrics:
    """Core metrics for evaluating an agrihood investment opportunity."""
    name: str
    location: str
    state: str
    
    # Development metrics
    total_units: Optional[int] = None
    units_sold: Optional[int] = None
    avg_home_price: Optional[int] = None
    price_premium_pct: Optional[float] = None  # vs comparable traditional neighborhoods
    stage: Optional[DevelopmentStage] = None
    year_established: Optional[int] = None
    
    # Agricultural component
    farm_acres: Optional[float] = None
    farm_type: Optional[FarmType] = None
    organic_certified: bool = False
    
    # Market factors
    metro_area: Optional[str] = None
    distance_to_city_miles: Optional[float] = None
    median_household_income_area: Optional[int] = None
    population_growth_rate: Optional[float] = None  # annual %
    
    # Sustainability & Incentives
    leed_certified: bool = False
    tax_incentives: bool = False
    faster_zoning: bool = False
    conservation_easement: bool = False
    
    # Community factors
    walkability_score: Optional[int] = None  # 0-100
    community_events_annual: Optional[int] = None
    restaurant_farm_table: bool = False
    
    # Financial performance
    property_value_appreciation: Optional[float] = None  # annual %
    occupancy_rate: Optional[float] = None  # %
    days_on_market_avg: Optional[int] = None
    
    # Risk factors
    water_rights_secure: Optional[bool] = None
    agricultural_staff_hired: Optional[bool] = None
    hoa_farm_funded: Optional[bool] = None
    
    website: Optional[str] = None
    notes: Optional[str] = None


class AgriHoodAnalyzer:
    """Analyzes and scores agrihood developments as investment opportunities."""
    
    def __init__(self):
        self.agrihoods: List[AgriHoodMetrics] = []
        
    def add_agrihood(self, agrihood: AgriHoodMetrics):
        """Add an agrihood to the database."""
        self.agrihoods.append(agrihood)
    
    def calculate_investment_score(self, agrihood: AgriHoodMetrics) -> Dict:
        """
        Calculate a comprehensive investment score (0-100).
        
        Scoring factors:
        - Market strength (30 points): price premium, appreciation, location
        - Development quality (25 points): stage, units, farm quality
        - Risk mitigation (20 points): water rights, staff, funding
        - Growth potential (15 points): population growth, metro proximity
        - Sustainability advantage (10 points): certifications, incentives
        """
        score = 0
        breakdown = {}
        
        # Market Strength (30 points max)
        market_score = 0
        if agrihood.price_premium_pct:
            # 0-15 points based on price premium (0-30% premium range)
            market_score += min(15, (agrihood.price_premium_pct / 30) * 15)
        if agrihood.property_value_appreciation:
            # 0-10 points based on appreciation (0-10% annual range)
            market_score += min(10, (agrihood.property_value_appreciation / 10) * 10)
        if agrihood.days_on_market_avg and agrihood.days_on_market_avg < 60:
            market_score += 5  # Strong demand signal
        breakdown['market_strength'] = round(market_score, 1)
        score += market_score
        
        # Development Quality (25 points max)
        dev_score = 0
        if agrihood.stage == DevelopmentStage.ESTABLISHED:
            dev_score += 10
        elif agrihood.stage == DevelopmentStage.MATURE:
            dev_score += 12
        elif agrihood.stage == DevelopmentStage.PARTIALLY_COMPLETE:
            dev_score += 6
        
        if agrihood.farm_type == FarmType.PROFESSIONAL:
            dev_score += 8  # Professional management = less risk
        elif agrihood.farm_type == FarmType.HYBRID:
            dev_score += 6
        
        if agrihood.organic_certified:
            dev_score += 3
        if agrihood.restaurant_farm_table:
            dev_score += 2  # Revenue diversification
        
        breakdown['development_quality'] = round(dev_score, 1)
        score += dev_score
        
        # Risk Mitigation (20 points max)
        risk_score = 0
        if agrihood.water_rights_secure:
            risk_score += 8
        if agrihood.agricultural_staff_hired:
            risk_score += 7
        if agrihood.hoa_farm_funded:
            risk_score += 5
        
        breakdown['risk_mitigation'] = round(risk_score, 1)
        score += risk_score
        
        # Growth Potential (15 points max)
        growth_score = 0
        if agrihood.population_growth_rate:
            # 0-8 points for population growth (0-4% annual range)
            growth_score += min(8, (agrihood.population_growth_rate / 4) * 8)
        if agrihood.distance_to_city_miles and agrihood.distance_to_city_miles < 30:
            growth_score += 5  # Proximity to major metro
        elif agrihood.distance_to_city_miles and agrihood.distance_to_city_miles < 50:
            growth_score += 2
        if agrihood.median_household_income_area and agrihood.median_household_income_area > 80000:
            growth_score += 2  # Affluent market
        
        breakdown['growth_potential'] = round(growth_score, 1)
        score += growth_score
        
        # Sustainability Advantage (10 points max)
        sustain_score = 0
        if agrihood.leed_certified:
            sustain_score += 3
        if agrihood.tax_incentives:
            sustain_score += 3
        if agrihood.faster_zoning:
            sustain_score += 2
        if agrihood.conservation_easement:
            sustain_score += 2
        
        breakdown['sustainability'] = round(sustain_score, 1)
        score += sustain_score
        
        # Determine rating
        rating = self._get_rating(score)
        
        return {
            'total_score': round(score, 1),
            'rating': rating,
            'breakdown': breakdown,
            'strengths': self._identify_strengths(agrihood, breakdown),
            'risks': self._identify_risks(agrihood)
        }
    
    def _get_rating(self, score: float) -> str:
        """Convert numerical score to letter rating."""
        if score >= 85:
            return "A+ (Exceptional)"
        elif score >= 75:
            return "A (Strong)"
        elif score >= 65:
            return "B+ (Above Average)"
        elif score >= 55:
            return "B (Good)"
        elif score >= 45:
            return "C+ (Moderate)"
        elif score >= 35:
            return "C (Fair)"
        else:
            return "D (High Risk)"
    
    def _identify_strengths(self, agrihood: AgriHoodMetrics, breakdown: Dict) -> List[str]:
        """Identify key investment strengths."""
        strengths = []
        
        if breakdown.get('market_strength', 0) >= 20:
            strengths.append("Strong market performance & pricing power")
        if agrihood.farm_type == FarmType.PROFESSIONAL:
            strengths.append("Professional farm management (reduced operational risk)")
        if agrihood.water_rights_secure:
            strengths.append("Secure water rights")
        if agrihood.tax_incentives or agrihood.faster_zoning:
            strengths.append("Government incentives & regulatory advantages")
        if agrihood.population_growth_rate and agrihood.population_growth_rate > 2:
            strengths.append(f"High population growth area ({agrihood.population_growth_rate}% annually)")
        if agrihood.days_on_market_avg and agrihood.days_on_market_avg < 45:
            strengths.append("High demand (low days on market)")
        
        return strengths
    
    def _identify_risks(self, agrihood: AgriHoodMetrics) -> List[str]:
        """Identify key investment risks."""
        risks = []
        
        if not agrihood.water_rights_secure:
            risks.append("⚠️ Water rights not confirmed - critical risk in agriculture")
        if not agrihood.agricultural_staff_hired:
            risks.append("⚠️ No professional farm staff - operational complexity risk")
        if agrihood.farm_type == FarmType.COOPERATIVE:
            risks.append("⚠️ Resident-run farm model - higher management risk")
        if not agrihood.hoa_farm_funded:
            risks.append("⚠️ Farm funding model unclear - sustainability risk")
        if agrihood.stage in [DevelopmentStage.PLANNING, DevelopmentStage.UNDER_CONSTRUCTION]:
            risks.append("⚠️ Early-stage development - execution risk")
        if agrihood.distance_to_city_miles and agrihood.distance_to_city_miles > 50:
            risks.append("⚠️ Remote location - demand may be limited")
        
        return risks if risks else ["No major red flags identified"]
    
    def rank_opportunities(self, min_score: float = 0) -> List[tuple]:
        """Rank all agrihoods by investment score."""
        scored = []
        for agrihood in self.agrihoods:
            analysis = self.calculate_investment_score(agrihood)
            if analysis['total_score'] >= min_score:
                scored.append((agrihood, analysis))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1]['total_score'], reverse=True)
        return scored
    
    def generate_report(self, agrihood: AgriHoodMetrics) -> str:
        """Generate a detailed investment report for an agrihood."""
        analysis = self.calculate_investment_score(agrihood)
        
        report = f"""
{'='*70}
AGRIHOOD INVESTMENT ANALYSIS
{'='*70}

PROJECT: {agrihood.name}
LOCATION: {agrihood.location}, {agrihood.state}
WEBSITE: {agrihood.website or 'N/A'}

{'='*70}
INVESTMENT SCORE: {analysis['total_score']}/100 — {analysis['rating']}
{'='*70}

SCORE BREAKDOWN:
  • Market Strength:       {analysis['breakdown']['market_strength']:.1f}/30
  • Development Quality:   {analysis['breakdown']['development_quality']:.1f}/25
  • Risk Mitigation:       {analysis['breakdown']['risk_mitigation']:.1f}/20
  • Growth Potential:      {analysis['breakdown']['growth_potential']:.1f}/15
  • Sustainability:        {analysis['breakdown']['sustainability']:.1f}/10

KEY METRICS:
"""
        if agrihood.total_units:
            report += f"  • Total Units: {agrihood.total_units:,}\n"
        if agrihood.avg_home_price:
            report += f"  • Avg Home Price: ${agrihood.avg_home_price:,}\n"
        if agrihood.price_premium_pct:
            report += f"  • Price Premium: +{agrihood.price_premium_pct}% vs traditional neighborhoods\n"
        if agrihood.property_value_appreciation:
            report += f"  • Appreciation Rate: {agrihood.property_value_appreciation}% annually\n"
        if agrihood.farm_acres:
            report += f"  • Farm Size: {agrihood.farm_acres} acres\n"
        if agrihood.farm_type:
            report += f"  • Farm Management: {agrihood.farm_type.value}\n"
        
        report += f"\nSTRENGTHS:\n"
        for strength in analysis['strengths']:
            report += f"  ✓ {strength}\n"
        
        report += f"\nRISKS & CONSIDERATIONS:\n"
        for risk in analysis['risks']:
            report += f"  {risk}\n"
        
        if agrihood.notes:
            report += f"\nADDITIONAL NOTES:\n{agrihood.notes}\n"
        
        report += f"\n{'='*70}\n"
        
        return report
    
    def export_database(self, filepath: str):
        """Export all agrihoods to JSON."""
        data = []
        for agrihood in self.agrihoods:
            agrihood_dict = asdict(agrihood)
            # Convert enums to strings
            if agrihood_dict['stage']:
                agrihood_dict['stage'] = agrihood_dict['stage'].value
            if agrihood_dict['farm_type']:
                agrihood_dict['farm_type'] = agrihood_dict['farm_type'].value
            data.append(agrihood_dict)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Exported {len(data)} agrihoods to {filepath}")


def build_sample_database():
    """Build a sample database with well-known agrihoods."""
    analyzer = AgriHoodAnalyzer()
    
    # Serenbe - Established, premium agrihood near Atlanta
    analyzer.add_agrihood(AgriHoodMetrics(
        name="Serenbe",
        location="Chattahoochee Hills",
        state="GA",
        total_units=700,  # Planned
        avg_home_price=750000,
        price_premium_pct=25.0,
        stage=DevelopmentStage.ESTABLISHED,
        year_established=2004,
        farm_acres=25,
        farm_type=FarmType.PROFESSIONAL,
        organic_certified=True,
        metro_area="Atlanta",
        distance_to_city_miles=30,
        median_household_income_area=95000,
        population_growth_rate=1.8,
        leed_certified=True,
        tax_incentives=False,
        faster_zoning=True,
        conservation_easement=True,
        walkability_score=85,
        restaurant_farm_table=True,
        property_value_appreciation=6.5,
        days_on_market_avg=45,
        water_rights_secure=True,
        agricultural_staff_hired=True,
        hoa_farm_funded=True,
        website="https://www.serenbe.com",
        notes="Pioneering agrihood, strong brand, multiple restaurants, arts community integration"
    ))
    
    # Agritopia - Phoenix area, established model
    analyzer.add_agrihood(AgriHoodMetrics(
        name="Agritopia",
        location="Gilbert",
        state="AZ",
        total_units=450,
        avg_home_price=520000,  # 2018: $400k, appreciation estimated
        price_premium_pct=18.0,
        stage=DevelopmentStage.MATURE,
        year_established=2000,
        farm_acres=11,
        farm_type=FarmType.PROFESSIONAL,
        organic_certified=False,
        metro_area="Phoenix",
        distance_to_city_miles=20,
        median_household_income_area=82000,
        population_growth_rate=2.3,
        leed_certified=False,
        tax_incentives=True,
        faster_zoning=True,
        conservation_easement=False,
        walkability_score=75,
        restaurant_farm_table=True,
        property_value_appreciation=5.2,
        occupancy_rate=97.0,
        days_on_market_avg=38,
        water_rights_secure=True,
        agricultural_staff_hired=True,
        hoa_farm_funded=True,
        website="https://www.agritopia.com",
        notes="One of first agrihoods, survived 2008 recession, farm-to-table restaurant on-site"
    ))
    
    # Harvest Green - Houston area, large scale
    analyzer.add_agrihood(AgriHoodMetrics(
        name="Harvest Green",
        location="Richmond",
        state="TX",
        total_units=2600,  # Massive scale
        avg_home_price=380000,
        price_premium_pct=12.0,
        stage=DevelopmentStage.PARTIALLY_COMPLETE,
        year_established=2014,
        farm_acres=50,
        farm_type=FarmType.PROFESSIONAL,
        organic_certified=True,
        metro_area="Houston",
        distance_to_city_miles=28,
        median_household_income_area=76000,
        population_growth_rate=3.1,  # Texas growth
        leed_certified=False,
        tax_incentives=True,
        faster_zoning=True,
        conservation_easement=True,
        walkability_score=68,
        restaurant_farm_table=False,
        property_value_appreciation=7.8,
        days_on_market_avg=52,
        water_rights_secure=True,
        agricultural_staff_hired=True,
        hoa_farm_funded=True,
        website="https://www.harvestgreentexas.com",
        notes="Largest agrihood development, Houston's strong population growth, farm education programs"
    ))
    
    # Willowsford - Northern Virginia (Jack's area!)
    analyzer.add_agrihood(AgriHoodMetrics(
        name="Willowsford",
        location="Ashburn",
        state="VA",
        total_units=4000,  # Master-planned community
        avg_home_price=720000,
        price_premium_pct=20.0,
        stage=DevelopmentStage.ESTABLISHED,
        year_established=2010,
        farm_acres=300,  # Large working farm
        farm_type=FarmType.PROFESSIONAL,
        organic_certified=True,
        metro_area="Washington DC",
        distance_to_city_miles=35,
        median_household_income_area=145000,  # Loudoun County is wealthy
        population_growth_rate=2.5,
        leed_certified=True,
        tax_incentives=True,
        faster_zoning=True,
        conservation_easement=True,
        walkability_score=72,
        restaurant_farm_table=False,
        property_value_appreciation=5.8,
        days_on_market_avg=41,
        water_rights_secure=True,
        agricultural_staff_hired=True,
        hoa_farm_funded=True,
        website="https://www.willowsford.com",
        notes="DC metro area, very high income demographics, extensive trail system, CSA programs"
    ))
    
    # Arden - Florida, newer development
    analyzer.add_agrihood(AgriHoodMetrics(
        name="Arden",
        location="Wellington",
        state="FL",
        total_units=3500,
        avg_home_price=420000,
        price_premium_pct=15.0,
        stage=DevelopmentStage.PARTIALLY_COMPLETE,
        year_established=2019,
        farm_acres=18,
        farm_type=FarmType.PROFESSIONAL,
        organic_certified=False,
        metro_area="Palm Beach",
        distance_to_city_miles=18,
        median_household_income_area=88000,
        population_growth_rate=2.8,  # Florida growth
        leed_certified=False,
        tax_incentives=True,
        faster_zoning=True,
        conservation_easement=False,
        walkability_score=70,
        restaurant_farm_table=False,
        property_value_appreciation=8.2,  # Strong Florida appreciation
        days_on_market_avg=36,
        water_rights_secure=True,
        agricultural_staff_hired=True,
        hoa_farm_funded=True,
        website="https://www.ardenfl.com",
        notes="Florida's population influx, newer development, strong sales velocity"
    ))
    
    # Prairie Crossing - Chicago area, early pioneer
    analyzer.add_agrihood(AgriHoodMetrics(
        name="Prairie Crossing",
        location="Grayslake",
        state="IL",
        total_units=359,
        avg_home_price=480000,
        price_premium_pct=22.0,
        stage=DevelopmentStage.MATURE,
        year_established=1994,  # Very early!
        farm_acres=100,
        farm_type=FarmType.HYBRID,
        organic_certified=True,
        metro_area="Chicago",
        distance_to_city_miles=45,
        median_household_income_area=92000,
        population_growth_rate=0.8,  # Slower Midwest growth
        leed_certified=True,
        tax_incentives=True,
        faster_zoning=False,
        conservation_easement=True,
        walkability_score=78,
        restaurant_farm_table=False,
        property_value_appreciation=4.2,
        days_on_market_avg=68,
        water_rights_secure=True,
        agricultural_staff_hired=True,
        hoa_farm_funded=True,
        website="https://www.prairiecrossing.com",
        notes="Oldest agrihood (1994), survived multiple economic cycles, conservation-focused"
    ))
    
    return analyzer


def main():
    """Demo the analyzer with sample data."""
    print("\n" + "="*70)
    print("AGRIHOOD INVESTMENT ANALYZER")
    print("Analyzing agrihood developments as investment opportunities")
    print("="*70 + "\n")
    
    # Build sample database
    analyzer = build_sample_database()
    
    # Generate full reports for top opportunities
    print("GENERATING DETAILED INVESTMENT REPORTS...\n")
    
    rankings = analyzer.rank_opportunities()
    
    for i, (agrihood, analysis) in enumerate(rankings[:6], 1):
        print(f"\n{'#'*70}")
        print(f"RANK #{i}")
        print(analyzer.generate_report(agrihood))
    
    # Summary rankings table
    print("\n" + "="*70)
    print("INVESTMENT RANKINGS SUMMARY")
    print("="*70 + "\n")
    print(f"{'Rank':<6} {'Name':<20} {'Location':<18} {'Score':<8} {'Rating':<20}")
    print("-" * 70)
    
    for i, (agrihood, analysis) in enumerate(rankings, 1):
        print(f"{i:<6} {agrihood.name:<20} {agrihood.location}, {agrihood.state:<15} "
              f"{analysis['total_score']:<8.1f} {analysis['rating']:<20}")
    
    # Export data
    print("\n" + "="*70)
    analyzer.export_database('/home/ec2-user/.openclaw/workspace/projects/agrihood-analyzer/agrihood_database.json')
    print("="*70 + "\n")
    
    print("✓ Analysis complete!")
    print("\nNEXT STEPS:")
    print("  1. Research specific agrihoods in detail (due diligence)")
    print("  2. Connect with developers for investment opportunities")
    print("  3. Review offering memorandums and financial projections")
    print("  4. Consider geographic diversification")
    print("  5. Evaluate timeline: early-stage vs. established properties")
    print("\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Angel Deal Scorer - A quick decision framework for angel investors
Built for EZDeal.ai research | March 2026

Usage:
  python deal_scorer.py                    # Interactive mode
  python deal_scorer.py --json input.json  # Batch mode
  python deal_scorer.py --demo             # Demo with sample data
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

# Scoring weights optimized for angel investors (different from VC criteria!)
WEIGHTS = {
    "founder": 0.30,      # Angels bet on people more than anything
    "traction": 0.25,     # Proof points matter
    "market": 0.20,       # Realistic opportunity, not TAM fantasy
    "capital_efficiency": 0.15,  # How far will the money go?
    "exit_potential": 0.10,      # Realistic exits, not unicorn dreams
}

@dataclass
class FounderScore:
    """Founder quality assessment"""
    domain_expertise: int  # 1-10: How well do they know this space?
    commitment: int        # 1-10: Full-time? Skin in game?
    coachability: int      # 1-10: Will they listen and learn?
    track_record: int      # 1-10: Prior success (doesn't have to be startups)
    network_strength: int  # 1-10: Can they hire, sell, raise?
    
    @property
    def score(self) -> float:
        return (self.domain_expertise + self.commitment + self.coachability + 
                self.track_record + self.network_strength) / 5

@dataclass
class TractionScore:
    """Evidence of progress"""
    users_or_customers: int     # 1-10: Active usage
    revenue: int                # 1-10: Any paying customers?
    growth_rate: int            # 1-10: Month-over-month trajectory
    engagement: int             # 1-10: Do users love it?
    testimonials_or_pilots: int # 1-10: Social proof
    
    @property
    def score(self) -> float:
        return (self.users_or_customers + self.revenue + self.growth_rate + 
                self.engagement + self.testimonials_or_pilots) / 5

@dataclass
class MarketScore:
    """Market opportunity (angel lens, not VC lens)"""
    problem_severity: int       # 1-10: Is this a real pain point?
    willingness_to_pay: int     # 1-10: Will people actually pay?
    competition_intensity: int  # 1-10: (Inverse) How crowded? (10 = low competition)
    timing: int                 # 1-10: Why now?
    market_access: int          # 1-10: Can this team reach customers?
    
    @property
    def score(self) -> float:
        return (self.problem_severity + self.willingness_to_pay + 
                self.competition_intensity + self.timing + self.market_access) / 5

@dataclass
class CapitalScore:
    """Capital efficiency assessment"""
    runway_months: int          # 1-10: How long will this round last?
    burn_rate_reasonability: int # 1-10: Is spending sensible?
    milestone_clarity: int      # 1-10: Clear goals for this raise?
    previous_funding_use: int   # 1-10: Did they use past $ well?
    capital_needs_fit: int      # 1-10: Is amount raised appropriate?
    
    @property
    def score(self) -> float:
        return (self.runway_months + self.burn_rate_reasonability + 
                self.milestone_clarity + self.previous_funding_use + 
                self.capital_needs_fit) / 5

@dataclass
class ExitScore:
    """Exit potential (realistic for angel timelines)"""
    acquirer_interest: int      # 1-10: Are there obvious buyers?
    strategic_value: int        # 1-10: Technology/team acquisition potential
    revenue_path: int           # 1-10: Path to sustainable revenue
    exit_timeline: int          # 1-10: Realistic 5-7 year horizon?
    comparable_exits: int       # 1-10: Similar companies that exited well?
    
    @property
    def score(self) -> float:
        return (self.acquirer_interest + self.strategic_value + self.revenue_path + 
                self.exit_timeline + self.comparable_exits) / 5

@dataclass
class DealTerms:
    """Deal structure info"""
    company_name: str
    stage: str  # pre-seed, seed, series-a
    instrument: str  # SAFE, convertible, priced
    valuation_cap: Optional[int] = None
    pre_money: Optional[int] = None
    raise_amount: Optional[int] = None
    check_size: Optional[int] = None
    discount: Optional[float] = None  # e.g., 0.20 for 20%

@dataclass
class DealEvaluation:
    """Complete deal evaluation"""
    terms: DealTerms
    founder: FounderScore
    traction: TractionScore
    market: MarketScore
    capital: CapitalScore
    exit: ExitScore
    notes: str = ""
    evaluated_at: str = ""
    
    @property
    def weighted_score(self) -> float:
        return (
            self.founder.score * WEIGHTS["founder"] +
            self.traction.score * WEIGHTS["traction"] +
            self.market.score * WEIGHTS["market"] +
            self.capital.score * WEIGHTS["capital_efficiency"] +
            self.exit.score * WEIGHTS["exit_potential"]
        )
    
    @property
    def recommendation(self) -> str:
        score = self.weighted_score
        if score >= 7.5:
            return "🟢 STRONG PROCEED - High conviction opportunity"
        elif score >= 6.0:
            return "🟡 PROCEED WITH DILIGENCE - Worth deeper evaluation"
        elif score >= 4.5:
            return "🟠 CONDITIONAL - Significant concerns to address"
        else:
            return "🔴 PASS - Does not meet investment criteria"
    
    def get_top_strengths(self, n: int = 3) -> list:
        """Return the top N scoring areas"""
        scores = [
            ("Founder Quality", self.founder.score),
            ("Traction", self.traction.score),
            ("Market Opportunity", self.market.score),
            ("Capital Efficiency", self.capital.score),
            ("Exit Potential", self.exit.score),
        ]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:n]
    
    def get_top_concerns(self, n: int = 3) -> list:
        """Return the top N areas of concern"""
        scores = [
            ("Founder Quality", self.founder.score),
            ("Traction", self.traction.score),
            ("Market Opportunity", self.market.score),
            ("Capital Efficiency", self.capital.score),
            ("Exit Potential", self.exit.score),
        ]
        return sorted(scores, key=lambda x: x[1])[:n]
    
    def valuation_sanity_check(self) -> str:
        """Check if valuation is reasonable for stage"""
        cap = self.terms.valuation_cap or self.terms.pre_money
        if not cap:
            return "⚪ No valuation info provided"
        
        stage_benchmarks = {
            "pre-seed": (1_000_000, 5_000_000),
            "seed": (3_000_000, 15_000_000),
            "series-a": (10_000_000, 40_000_000),
        }
        
        benchmark = stage_benchmarks.get(self.terms.stage.lower())
        if not benchmark:
            return "⚪ Unknown stage"
        
        low, high = benchmark
        if cap < low:
            return f"🟢 Below market ({cap/1e6:.1f}M vs {low/1e6:.0f}-{high/1e6:.0f}M typical)"
        elif cap <= high:
            return f"🟡 Market rate ({cap/1e6:.1f}M within {low/1e6:.0f}-{high/1e6:.0f}M range)"
        else:
            return f"🔴 Above market ({cap/1e6:.1f}M vs {low/1e6:.0f}-{high/1e6:.0f}M typical)"
    
    def generate_report(self) -> str:
        """Generate a formatted decision report"""
        lines = [
            "=" * 60,
            f"ANGEL DEAL EVALUATION: {self.terms.company_name}",
            "=" * 60,
            "",
            f"Stage: {self.terms.stage.upper()}",
            f"Instrument: {self.terms.instrument}",
        ]
        
        if self.terms.valuation_cap:
            lines.append(f"Valuation Cap: ${self.terms.valuation_cap:,}")
        if self.terms.pre_money:
            lines.append(f"Pre-Money: ${self.terms.pre_money:,}")
        if self.terms.raise_amount:
            lines.append(f"Raise Amount: ${self.terms.raise_amount:,}")
        if self.terms.check_size:
            lines.append(f"Your Check: ${self.terms.check_size:,}")
        
        lines.extend([
            "",
            "-" * 60,
            "SCORES (1-10 scale, weighted for angel investing)",
            "-" * 60,
            f"  Founder Quality (30%):    {self.founder.score:.1f}",
            f"  Traction (25%):           {self.traction.score:.1f}",
            f"  Market Opportunity (20%): {self.market.score:.1f}",
            f"  Capital Efficiency (15%): {self.capital.score:.1f}",
            f"  Exit Potential (10%):     {self.exit.score:.1f}",
            "",
            f"  OVERALL SCORE: {self.weighted_score:.1f}/10",
            "",
            "-" * 60,
            "RECOMMENDATION",
            "-" * 60,
            f"  {self.recommendation}",
            "",
            "-" * 60,
            "VALUATION CHECK",
            "-" * 60,
            f"  {self.valuation_sanity_check()}",
            "",
            "-" * 60,
            "TOP STRENGTHS",
            "-" * 60,
        ])
        
        for name, score in self.get_top_strengths():
            lines.append(f"  ✓ {name}: {score:.1f}")
        
        lines.extend([
            "",
            "-" * 60,
            "KEY CONCERNS",
            "-" * 60,
        ])
        
        for name, score in self.get_top_concerns():
            if score < 6:
                lines.append(f"  ⚠ {name}: {score:.1f}")
        
        if self.notes:
            lines.extend([
                "",
                "-" * 60,
                "NOTES",
                "-" * 60,
                f"  {self.notes}",
            ])
        
        lines.extend([
            "",
            "=" * 60,
            f"Evaluated: {self.evaluated_at or datetime.now().isoformat()}",
            "Generated by Angel Deal Scorer (EZDeal.ai Research)",
            "=" * 60,
        ])
        
        return "\n".join(lines)
    
    def to_json(self) -> str:
        """Export evaluation as JSON"""
        return json.dumps(asdict(self), indent=2)


def interactive_score(prompt: str, description: str = "") -> int:
    """Get a 1-10 score interactively"""
    while True:
        try:
            if description:
                print(f"  ({description})")
            val = int(input(f"  {prompt} [1-10]: "))
            if 1 <= val <= 10:
                return val
            print("  Please enter a number between 1 and 10")
        except ValueError:
            print("  Please enter a valid number")


def run_interactive():
    """Run interactive evaluation"""
    print("\n" + "=" * 60)
    print("ANGEL DEAL SCORER - Interactive Mode")
    print("=" * 60 + "\n")
    
    # Deal terms
    print("DEAL TERMS")
    print("-" * 40)
    company = input("Company name: ")
    stage = input("Stage (pre-seed/seed/series-a): ").lower() or "seed"
    instrument = input("Instrument (SAFE/convertible/priced): ") or "SAFE"
    
    val_cap = input("Valuation cap ($ or blank): ")
    val_cap = int(val_cap.replace(",", "").replace("$", "")) if val_cap else None
    
    raise_amt = input("Raise amount ($ or blank): ")
    raise_amt = int(raise_amt.replace(",", "").replace("$", "")) if raise_amt else None
    
    check = input("Your check size ($ or blank): ")
    check = int(check.replace(",", "").replace("$", "")) if check else None
    
    terms = DealTerms(
        company_name=company,
        stage=stage,
        instrument=instrument,
        valuation_cap=val_cap,
        raise_amount=raise_amt,
        check_size=check,
    )
    
    # Founder scoring
    print("\nFOUNDER QUALITY (30% weight)")
    print("-" * 40)
    founder = FounderScore(
        domain_expertise=interactive_score("Domain expertise", "How well do they know this space?"),
        commitment=interactive_score("Commitment level", "Full-time? Skin in game?"),
        coachability=interactive_score("Coachability", "Will they listen and learn?"),
        track_record=interactive_score("Track record", "Prior success (any field)"),
        network_strength=interactive_score("Network strength", "Can they hire, sell, raise?"),
    )
    
    # Traction scoring
    print("\nTRACTION (25% weight)")
    print("-" * 40)
    traction = TractionScore(
        users_or_customers=interactive_score("Users/customers", "Active usage level"),
        revenue=interactive_score("Revenue", "Any paying customers?"),
        growth_rate=interactive_score("Growth rate", "Month-over-month trajectory"),
        engagement=interactive_score("Engagement", "Do users love it?"),
        testimonials_or_pilots=interactive_score("Social proof", "Testimonials, pilots, LOIs"),
    )
    
    # Market scoring
    print("\nMARKET OPPORTUNITY (20% weight)")
    print("-" * 40)
    market = MarketScore(
        problem_severity=interactive_score("Problem severity", "Is this a real pain point?"),
        willingness_to_pay=interactive_score("Willingness to pay", "Will people actually pay?"),
        competition_intensity=interactive_score("Competition", "10 = low competition, 1 = crowded"),
        timing=interactive_score("Timing", "Why now? Is the market ready?"),
        market_access=interactive_score("Market access", "Can this team reach customers?"),
    )
    
    # Capital efficiency
    print("\nCAPITAL EFFICIENCY (15% weight)")
    print("-" * 40)
    capital = CapitalScore(
        runway_months=interactive_score("Runway", "How long will this round last?"),
        burn_rate_reasonability=interactive_score("Burn rate", "Is spending sensible?"),
        milestone_clarity=interactive_score("Milestone clarity", "Clear goals for this raise?"),
        previous_funding_use=interactive_score("Previous funding", "Did they use past $ well?"),
        capital_needs_fit=interactive_score("Amount fit", "Is raise amount appropriate?"),
    )
    
    # Exit potential
    print("\nEXIT POTENTIAL (10% weight)")
    print("-" * 40)
    exit_score = ExitScore(
        acquirer_interest=interactive_score("Acquirer interest", "Are there obvious buyers?"),
        strategic_value=interactive_score("Strategic value", "Tech/team acquisition potential"),
        revenue_path=interactive_score("Revenue path", "Path to sustainable revenue"),
        exit_timeline=interactive_score("Timeline", "Realistic 5-7 year horizon?"),
        comparable_exits=interactive_score("Comparables", "Similar companies that exited?"),
    )
    
    # Notes
    print("\nADDITIONAL NOTES")
    print("-" * 40)
    notes = input("Any additional notes (optional): ")
    
    # Create evaluation
    evaluation = DealEvaluation(
        terms=terms,
        founder=founder,
        traction=traction,
        market=market,
        capital=capital,
        exit=exit_score,
        notes=notes,
        evaluated_at=datetime.now().isoformat(),
    )
    
    # Output
    print("\n" + evaluation.generate_report())
    
    # Save option
    save = input("\nSave to file? (y/n): ").lower()
    if save == 'y':
        filename = f"{company.lower().replace(' ', '_')}_eval_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w') as f:
            f.write(evaluation.to_json())
        print(f"Saved to {filename}")
    
    return evaluation


def run_demo():
    """Run with demo data"""
    print("\n" + "=" * 60)
    print("ANGEL DEAL SCORER - Demo Mode")
    print("=" * 60 + "\n")
    
    # Sample evaluation: A fictional AI startup
    demo = DealEvaluation(
        terms=DealTerms(
            company_name="DataLens AI",
            stage="seed",
            instrument="SAFE",
            valuation_cap=8_000_000,
            raise_amount=1_500_000,
            check_size=25_000,
        ),
        founder=FounderScore(
            domain_expertise=8,  # Former data scientist at Stripe
            commitment=9,        # Full-time, quit job, invested savings
            coachability=7,      # Open to feedback, some ego
            track_record=6,      # First startup, but strong career
            network_strength=7,  # Good but not exceptional
        ),
        traction=TractionScore(
            users_or_customers=6,     # 15 paying customers
            revenue=5,                # $8K MRR
            growth_rate=7,            # 20% month-over-month
            engagement=8,             # Users love it, low churn
            testimonials_or_pilots=7, # Good case studies
        ),
        market=MarketScore(
            problem_severity=8,       # Real pain point
            willingness_to_pay=7,     # Enterprise will pay
            competition_intensity=5,  # Crowded but differentiable
            timing=8,                 # AI moment is now
            market_access=6,          # Still building GTM
        ),
        capital=CapitalScore(
            runway_months=7,          # 18 months
            burn_rate_reasonability=8,# Lean team
            milestone_clarity=7,      # Clear goals
            previous_funding_use=6,   # First institutional raise
            capital_needs_fit=7,      # Appropriate for stage
        ),
        exit=ExitScore(
            acquirer_interest=6,      # Several potential buyers
            strategic_value=7,        # Valuable tech
            revenue_path=7,           # Clear path to profitability
            exit_timeline=6,          # Maybe 5-7 years
            comparable_exits=5,       # Some, not many
        ),
        notes="Strong technical founder, good early traction. Main risk is crowded market. Worth further diligence on competitive moat.",
        evaluated_at=datetime.now().isoformat(),
    )
    
    print(demo.generate_report())
    return demo


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            run_demo()
        elif sys.argv[1] == "--json" and len(sys.argv) > 2:
            with open(sys.argv[2]) as f:
                data = json.load(f)
            # Parse JSON into evaluation (simplified)
            print("JSON batch mode not fully implemented - use interactive mode")
        elif sys.argv[1] == "--help":
            print(__doc__)
        else:
            print(__doc__)
    else:
        run_interactive()


if __name__ == "__main__":
    main()

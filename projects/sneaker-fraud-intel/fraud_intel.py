#!/usr/bin/env python3
"""
Sneaker Resale Fraud Intelligence System
Analyzes seller/buyer patterns to detect counterfeit operations

Usage:
    python3 fraud_intel.py analyze --seller <seller_id>
    python3 fraud_intel.py batch --input sellers.json
    python3 fraud_intel.py report --output report.json
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class RiskLevel(Enum):
    CRITICAL = "CRITICAL"  # 80-100
    HIGH = "HIGH"          # 60-79
    MEDIUM = "MEDIUM"      # 40-59
    LOW = "LOW"            # 20-39
    MINIMAL = "MINIMAL"    # 0-19


@dataclass
class SellerProfile:
    """Seller profile with transaction history"""
    seller_id: str
    account_age_days: int
    total_sales: int
    categories_sold: List[str]
    avg_price: float
    high_value_count: int  # Sales > $500
    return_rate: float
    negative_feedback_pct: float
    new_in_box_pct: float
    rapid_listing_count: int  # >10 items/day
    location: str
    ships_from_known_counterfeit_region: bool
    social_media_verified: bool
    business_entity: bool


@dataclass
class ListingSignals:
    """Individual listing red flags"""
    below_market_pct: float  # % below market price
    stock_photo_used: bool
    description_copied: bool
    multiple_sizes_available: bool
    new_release_immediate_stock: bool  # Has stock of just-released shoe
    bulk_quantity: int  # Selling multiples of same SKU
    inconsistent_photos: bool  # Photo quality/background varies


@dataclass
class FraudScore:
    """Complete fraud risk assessment"""
    seller_id: str
    overall_score: float  # 0-100
    risk_level: RiskLevel
    seller_signals: Dict[str, float]
    listing_signals: Dict[str, float]
    red_flags: List[str]
    green_flags: List[str]
    confidence: float
    recommended_action: str
    timestamp: str


class FraudAnalyzer:
    """Core fraud detection engine"""
    
    # Known counterfeit hotspots (based on industry data)
    COUNTERFEIT_REGIONS = [
        "Putian, China",
        "Guangzhou, China",
        "Dongguan, China",
        "Vietnam (bulk)",
        "Turkey (bulk)"
    ]
    
    # Weights for scoring model
    WEIGHTS = {
        "account_age": 0.10,
        "transaction_history": 0.15,
        "pricing_anomaly": 0.20,
        "geographic_risk": 0.15,
        "listing_patterns": 0.20,
        "feedback_quality": 0.10,
        "verification_status": 0.10
    }
    
    def __init__(self):
        self.fraud_patterns = self._load_fraud_patterns()
    
    def _load_fraud_patterns(self) -> Dict:
        """Load known fraud operation patterns"""
        return {
            "new_account_bulk": {
                "indicators": ["account_age < 30 days", "bulk_listings > 50"],
                "weight": 0.85
            },
            "price_dumping": {
                "indicators": ["below_market > 20%", "high_value_items"],
                "weight": 0.90
            },
            "replica_wholesaler": {
                "indicators": ["multiple_sizes", "immediate_stock", "known_region"],
                "weight": 0.95
            },
            "photo_theft": {
                "indicators": ["stock_photos", "copied_descriptions"],
                "weight": 0.70
            },
            "return_abuse": {
                "indicators": ["high_return_rate", "new_in_box_only"],
                "weight": 0.60
            }
        }
    
    def analyze_seller(self, profile: SellerProfile, 
                      listings: List[ListingSignals]) -> FraudScore:
        """Analyze seller and return fraud score"""
        
        # Calculate component scores
        seller_scores = self._score_seller_profile(profile)
        listing_scores = self._score_listings(listings)
        
        # Weighted overall score
        overall = self._calculate_weighted_score(seller_scores, listing_scores)
        
        # Identify specific red/green flags
        red_flags = self._identify_red_flags(profile, listings, seller_scores, listing_scores)
        green_flags = self._identify_green_flags(profile, seller_scores)
        
        # Risk level and confidence
        risk_level = self._determine_risk_level(overall)
        confidence = self._calculate_confidence(profile, len(listings))
        
        # Recommended action
        action = self._recommend_action(risk_level, confidence)
        
        return FraudScore(
            seller_id=profile.seller_id,
            overall_score=round(overall, 2),
            risk_level=risk_level,
            seller_signals=seller_scores,
            listing_signals=listing_scores,
            red_flags=red_flags,
            green_flags=green_flags,
            confidence=round(confidence, 2),
            recommended_action=action,
            timestamp=datetime.utcnow().isoformat()
        )
    
    def _score_seller_profile(self, profile: SellerProfile) -> Dict[str, float]:
        """Score seller profile attributes (higher = more suspicious)"""
        scores = {}
        
        # Account age (newer = riskier)
        if profile.account_age_days < 30:
            scores["account_age"] = 80.0
        elif profile.account_age_days < 90:
            scores["account_age"] = 50.0
        elif profile.account_age_days < 180:
            scores["account_age"] = 25.0
        else:
            scores["account_age"] = 10.0
        
        # Transaction volume (too many too fast = suspicious)
        sales_per_day = profile.total_sales / max(profile.account_age_days, 1)
        if sales_per_day > 10:
            scores["volume_anomaly"] = 90.0
        elif sales_per_day > 5:
            scores["volume_anomaly"] = 60.0
        else:
            scores["volume_anomaly"] = 20.0
        
        # Pricing (high-value items = higher risk if other signals present)
        high_value_pct = profile.high_value_count / max(profile.total_sales, 1)
        if high_value_pct > 0.5 and profile.account_age_days < 90:
            scores["pricing_risk"] = 70.0
        else:
            scores["pricing_risk"] = 20.0
        
        # Return rate
        scores["return_rate"] = min(profile.return_rate * 100, 100.0)
        
        # Feedback
        scores["negative_feedback"] = profile.negative_feedback_pct
        
        # Geographic risk
        if profile.ships_from_known_counterfeit_region:
            scores["geographic"] = 85.0
        else:
            scores["geographic"] = 10.0
        
        # Verification (-ve signal, good if verified)
        verification_score = 0.0
        if profile.social_media_verified:
            verification_score -= 15.0
        if profile.business_entity:
            verification_score -= 10.0
        scores["verification"] = max(verification_score, -25.0)  # Cap benefit
        
        return scores
    
    def _score_listings(self, listings: List[ListingSignals]) -> Dict[str, float]:
        """Score listing patterns (higher = more suspicious)"""
        if not listings:
            return {"insufficient_data": 50.0}
        
        scores = {}
        
        # Pricing anomalies
        avg_below_market = sum(l.below_market_pct for l in listings) / len(listings)
        if avg_below_market > 20:
            scores["pricing_anomaly"] = 90.0
        elif avg_below_market > 10:
            scores["pricing_anomaly"] = 60.0
        else:
            scores["pricing_anomaly"] = 20.0
        
        # Stock photos
        stock_photo_pct = sum(1 for l in listings if l.stock_photo_used) / len(listings)
        scores["stock_photos"] = stock_photo_pct * 100
        
        # Multiple sizes available (common counterfeit signal)
        multi_size_pct = sum(1 for l in listings if l.multiple_sizes_available) / len(listings)
        scores["multiple_sizes"] = multi_size_pct * 80
        
        # Immediate new release stock
        immediate_stock_pct = sum(1 for l in listings if l.new_release_immediate_stock) / len(listings)
        scores["immediate_stock"] = immediate_stock_pct * 95
        
        # Bulk quantities
        avg_bulk = sum(l.bulk_quantity for l in listings) / len(listings)
        if avg_bulk > 5:
            scores["bulk_quantity"] = 85.0
        elif avg_bulk > 2:
            scores["bulk_quantity"] = 50.0
        else:
            scores["bulk_quantity"] = 10.0
        
        return scores
    
    def _calculate_weighted_score(self, seller_scores: Dict[str, float],
                                  listing_scores: Dict[str, float]) -> float:
        """Calculate final weighted score"""
        
        # Seller component (60% weight)
        seller_avg = sum(seller_scores.values()) / len(seller_scores) if seller_scores else 50.0
        
        # Listing component (40% weight)
        listing_avg = sum(listing_scores.values()) / len(listing_scores) if listing_scores else 50.0
        
        # Weighted combination
        overall = (seller_avg * 0.6) + (listing_avg * 0.4)
        
        return min(overall, 100.0)
    
    def _identify_red_flags(self, profile: SellerProfile, 
                           listings: List[ListingSignals],
                           seller_scores: Dict[str, float],
                           listing_scores: Dict[str, float]) -> List[str]:
        """Identify specific red flags"""
        flags = []
        
        # Account age
        if profile.account_age_days < 30:
            flags.append("⚠️ New account (<30 days old)")
        
        # Known counterfeit region
        if profile.ships_from_known_counterfeit_region:
            flags.append("🌏 Ships from known counterfeit region")
        
        # Pricing
        if listing_scores.get("pricing_anomaly", 0) > 70:
            flags.append("💰 Significantly below market prices")
        
        # Volume
        if seller_scores.get("volume_anomaly", 0) > 70:
            flags.append("📦 Abnormally high sales volume")
        
        # Stock photos
        if listing_scores.get("stock_photos", 0) > 50:
            flags.append("📸 Majority listings use stock photos")
        
        # Multiple sizes
        if listing_scores.get("multiple_sizes", 0) > 60:
            flags.append("👟 Multiple sizes available (common replica signal)")
        
        # Immediate stock on new releases
        if listing_scores.get("immediate_stock", 0) > 70:
            flags.append("⚡ Immediate stock on new releases")
        
        # High return rate
        if profile.return_rate > 0.15:
            flags.append(f"↩️ High return rate ({profile.return_rate*100:.1f}%)")
        
        # Negative feedback
        if profile.negative_feedback_pct > 10:
            flags.append(f"👎 High negative feedback ({profile.negative_feedback_pct:.1f}%)")
        
        # Bulk quantities
        if listing_scores.get("bulk_quantity", 0) > 70:
            flags.append("📊 Selling in bulk quantities")
        
        return flags
    
    def _identify_green_flags(self, profile: SellerProfile,
                             seller_scores: Dict[str, float]) -> List[str]:
        """Identify positive trust signals"""
        flags = []
        
        if profile.account_age_days > 365:
            flags.append("✅ Established account (>1 year)")
        
        if profile.social_media_verified:
            flags.append("✅ Social media verified")
        
        if profile.business_entity:
            flags.append("✅ Registered business entity")
        
        if profile.negative_feedback_pct < 2:
            flags.append("✅ Low negative feedback rate")
        
        if profile.return_rate < 0.05:
            flags.append("✅ Low return rate")
        
        if profile.total_sales > 100:
            flags.append(f"✅ Strong sales history ({profile.total_sales} transactions)")
        
        return flags
    
    def _determine_risk_level(self, score: float) -> RiskLevel:
        """Map score to risk level"""
        if score >= 80:
            return RiskLevel.CRITICAL
        elif score >= 60:
            return RiskLevel.HIGH
        elif score >= 40:
            return RiskLevel.MEDIUM
        elif score >= 20:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _calculate_confidence(self, profile: SellerProfile, listing_count: int) -> float:
        """Calculate confidence in assessment"""
        
        # More data = higher confidence
        data_points = profile.total_sales + listing_count
        
        if data_points < 5:
            base_confidence = 0.4
        elif data_points < 20:
            base_confidence = 0.6
        elif data_points < 50:
            base_confidence = 0.75
        else:
            base_confidence = 0.9
        
        # Adjust for account age (more history = more confident)
        if profile.account_age_days > 180:
            base_confidence += 0.05
        
        return min(base_confidence, 0.95)
    
    def _recommend_action(self, risk_level: RiskLevel, confidence: float) -> str:
        """Recommend action based on risk and confidence"""
        
        if risk_level == RiskLevel.CRITICAL:
            if confidence > 0.8:
                return "BLOCK: High confidence counterfeit operation"
            else:
                return "MANUAL REVIEW: Critical risk signals detected"
        
        elif risk_level == RiskLevel.HIGH:
            return "ENHANCED AUTHENTICATION: Require additional verification"
        
        elif risk_level == RiskLevel.MEDIUM:
            return "MONITOR: Watch for additional red flags"
        
        elif risk_level == RiskLevel.LOW:
            return "STANDARD PROCESS: Normal authentication flow"
        
        else:  # MINIMAL
            return "LOW RISK: Trusted seller"


def print_fraud_report(score: FraudScore):
    """Pretty print fraud assessment"""
    print(f"\n{'='*70}")
    print(f"FRAUD RISK ASSESSMENT — Seller: {score.seller_id}")
    print(f"{'='*70}\n")
    
    print(f"Overall Score:    {score.overall_score}/100")
    print(f"Risk Level:       {score.risk_level.value}")
    print(f"Confidence:       {score.confidence*100:.0f}%")
    print(f"Timestamp:        {score.timestamp}")
    print(f"\nRecommended Action:")
    print(f"  → {score.recommended_action}")
    
    if score.red_flags:
        print(f"\n⚠️  RED FLAGS ({len(score.red_flags)}):")
        for flag in score.red_flags:
            print(f"  {flag}")
    
    if score.green_flags:
        print(f"\n✅ GREEN FLAGS ({len(score.green_flags)}):")
        for flag in score.green_flags:
            print(f"  {flag}")
    
    print(f"\n📊 DETAILED SCORES:")
    print(f"\nSeller Signals:")
    for signal, value in sorted(score.seller_signals.items(), key=lambda x: x[1], reverse=True):
        print(f"  {signal:.<30} {value:>5.1f}")
    
    print(f"\nListing Signals:")
    for signal, value in sorted(score.listing_signals.items(), key=lambda x: x[1], reverse=True):
        print(f"  {signal:.<30} {value:>5.1f}")
    
    print(f"\n{'='*70}\n")


# Sample data for demonstration
def create_sample_sellers():
    """Create sample seller profiles for testing"""
    
    # High-risk seller (likely counterfeit operation)
    high_risk = SellerProfile(
        seller_id="sneaker_plug_888",
        account_age_days=25,
        total_sales=150,
        categories_sold=["Jordans", "Yeezys", "Dunks"],
        avg_price=320.00,
        high_value_count=120,
        return_rate=0.22,
        negative_feedback_pct=8.5,
        new_in_box_pct=100.0,
        rapid_listing_count=45,
        location="Putian, China",
        ships_from_known_counterfeit_region=True,
        social_media_verified=False,
        business_entity=False
    )
    
    high_risk_listings = [
        ListingSignals(
            below_market_pct=25.0,
            stock_photo_used=True,
            description_copied=True,
            multiple_sizes_available=True,
            new_release_immediate_stock=True,
            bulk_quantity=10,
            inconsistent_photos=False
        ) for _ in range(15)
    ]
    
    # Low-risk seller (legitimate reseller)
    low_risk = SellerProfile(
        seller_id="kickscollector_nyc",
        account_age_days=890,
        total_sales=420,
        categories_sold=["Jordans", "Nike SB", "New Balance", "Asics"],
        avg_price=185.00,
        high_value_count=85,
        return_rate=0.03,
        negative_feedback_pct=1.2,
        new_in_box_pct=75.0,
        rapid_listing_count=2,
        location="Brooklyn, NY",
        ships_from_known_counterfeit_region=False,
        social_media_verified=True,
        business_entity=True
    )
    
    low_risk_listings = [
        ListingSignals(
            below_market_pct=5.0,
            stock_photo_used=False,
            description_copied=False,
            multiple_sizes_available=False,
            new_release_immediate_stock=False,
            bulk_quantity=1,
            inconsistent_photos=False
        ) for _ in range(20)
    ]
    
    # Medium-risk seller (needs more investigation)
    medium_risk = SellerProfile(
        seller_id="freshkicks_la",
        account_age_days=120,
        total_sales=85,
        categories_sold=["Jordans", "Yeezys"],
        avg_price=410.00,
        high_value_count=65,
        return_rate=0.08,
        negative_feedback_pct=4.5,
        new_in_box_pct=95.0,
        rapid_listing_count=12,
        location="Los Angeles, CA",
        ships_from_known_counterfeit_region=False,
        social_media_verified=False,
        business_entity=False
    )
    
    medium_risk_listings = [
        ListingSignals(
            below_market_pct=12.0,
            stock_photo_used=False,
            description_copied=False,
            multiple_sizes_available=True,
            new_release_immediate_stock=True,
            bulk_quantity=3,
            inconsistent_photos=True
        ) for _ in range(10)
    ]
    
    return [
        (high_risk, high_risk_listings, "High Risk Example"),
        (low_risk, low_risk_listings, "Low Risk Example"),
        (medium_risk, medium_risk_listings, "Medium Risk Example")
    ]


def main():
    """Main entry point"""
    
    print("\n" + "="*70)
    print("SNEAKER RESALE FRAUD INTELLIGENCE SYSTEM")
    print("="*70)
    print("\nAnalyzing sample seller profiles...\n")
    
    analyzer = FraudAnalyzer()
    
    # Analyze sample sellers
    samples = create_sample_sellers()
    results = []
    
    for profile, listings, label in samples:
        print(f"\n{'─'*70}")
        print(f"Analyzing: {label} ({profile.seller_id})")
        print(f"{'─'*70}")
        
        score = analyzer.analyze_seller(profile, listings)
        results.append(score)
        print_fraud_report(score)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\nAnalyzed {len(results)} sellers:")
    for score in results:
        risk_emoji = "🔴" if score.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH] else \
                     "🟡" if score.risk_level == RiskLevel.MEDIUM else "🟢"
        print(f"  {risk_emoji} {score.seller_id:.<30} {score.overall_score:>5.1f}/100 ({score.risk_level.value})")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()

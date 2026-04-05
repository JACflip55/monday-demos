#!/usr/bin/env python3
"""
Sneaker Market Analyzer - Margin & Opportunity Detection
Analyzes market data to find pricing gaps, margin opportunities, and trends.
"""

import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import statistics

class SneakerMarketAnalyzer:
    """Analyzes sneaker market data for pricing, margins, and opportunities."""
    
    def __init__(self):
        self.market_data = []
        self.opportunities = []
        
    def load_data(self, file_path=None):
        """Load sneaker market data from JSON."""
        if not file_path:
            # Use sample data
            self.market_data = self._sample_data()
        else:
            with open(file_path, 'r') as f:
                self.market_data = json.load(f)
    
    def _sample_data(self) -> List[Dict]:
        """Generate realistic sample sneaker market data."""
        return [
            {
                "sku": "AJ1-001",
                "name": "Air Jordan 1 Retro High",
                "brand": "Nike",
                "retail_price": 170,
                "current_market_price": 285,
                "ask_price": 295,
                "bid_price": 270,
                "volume_30d": 1200,
                "markup_pct": 67.6,
                "size": "Size 10",
                "condition": "New",
                "release_date": "2023-11-15",
                "listings_active": 45,
                "sold_last_30d": 280,
            },
            {
                "sku": "YEEZY-350",
                "name": "Yeezy 350 V2 Onyx",
                "brand": "Adidas",
                "retail_price": 220,
                "current_market_price": 380,
                "ask_price": 395,
                "bid_price": 360,
                "volume_30d": 890,
                "markup_pct": 72.7,
                "size": "Size 10",
                "condition": "New",
                "release_date": "2023-06-22",
                "listings_active": 32,
                "sold_last_30d": 195,
            },
            {
                "sku": "DUNK-LOW-001",
                "name": "Dunk Low Retro",
                "brand": "Nike",
                "retail_price": 110,
                "current_market_price": 165,
                "ask_price": 172,
                "bid_price": 158,
                "volume_30d": 2100,
                "markup_pct": 50.0,
                "size": "Size 10",
                "condition": "New",
                "release_date": "2024-02-01",
                "listings_active": 78,
                "sold_last_30d": 520,
            },
            {
                "sku": "NB-2002R",
                "name": "New Balance 2002R",
                "brand": "New Balance",
                "retail_price": 140,
                "current_market_price": 155,
                "ask_price": 162,
                "bid_price": 148,
                "volume_30d": 350,
                "markup_pct": 10.7,
                "size": "Size 10",
                "condition": "New",
                "release_date": "2024-01-20",
                "listings_active": 22,
                "sold_last_30d": 85,
            },
            {
                "sku": "TRAVIS-DUNK",
                "name": "Travis Scott x Dunk Low OG",
                "brand": "Nike",
                "retail_price": 140,
                "current_market_price": 850,
                "ask_price": 899,
                "bid_price": 800,
                "volume_30d": 42,
                "markup_pct": 507.1,
                "size": "Size 10",
                "condition": "New",
                "release_date": "2023-01-15",
                "listings_active": 8,
                "sold_last_30d": 10,
            },
            {
                "sku": "PUMA-FUTURE",
                "name": "Puma Future Rider",
                "brand": "Puma",
                "retail_price": 90,
                "current_market_price": 105,
                "ask_price": 110,
                "bid_price": 100,
                "volume_30d": 420,
                "markup_pct": 16.7,
                "size": "Size 10",
                "condition": "New",
                "release_date": "2024-03-10",
                "listings_active": 15,
                "sold_last_30d": 92,
            },
            {
                "sku": "YEEZY-500",
                "name": "Yeezy 500 High Slate",
                "brand": "Adidas",
                "retail_price": 200,
                "current_market_price": 320,
                "ask_price": 335,
                "bid_price": 305,
                "volume_30d": 180,
                "markup_pct": 60.0,
                "size": "Size 10",
                "condition": "New",
                "release_date": "2023-08-30",
                "listings_active": 11,
                "sold_last_30d": 42,
            },
        ]
    
    def analyze_margins(self) -> Dict:
        """Calculate margin analysis across the market."""
        margins = []
        
        for shoe in self.market_data:
            bid_ask_spread = shoe['ask_price'] - shoe['bid_price']
            bid_ask_spread_pct = (bid_ask_spread / shoe['bid_price']) * 100
            
            margins.append({
                'sku': shoe['sku'],
                'name': shoe['name'],
                'retail': shoe['retail_price'],
                'market': shoe['current_market_price'],
                'markup_pct': shoe['markup_pct'],
                'bid_ask_spread': bid_ask_spread,
                'bid_ask_spread_pct': round(bid_ask_spread_pct, 1),
            })
        
        # Sort by markup % descending
        margins.sort(key=lambda x: x['markup_pct'], reverse=True)
        
        avg_markup = statistics.mean([m['markup_pct'] for m in margins])
        avg_spread = statistics.mean([m['bid_ask_spread_pct'] for m in margins])
        
        return {
            'by_shoe': margins,
            'market_avg_markup_pct': round(avg_markup, 1),
            'market_avg_spread_pct': round(avg_spread, 1),
            'highest_markup': margins[0] if margins else None,
            'lowest_markup': margins[-1] if margins else None,
        }
    
    def identify_opportunities(self) -> List[Dict]:
        """Identify market opportunities."""
        opportunities = []
        
        # Opportunity 1: High markup + High volume = "Golden Geese"
        for shoe in self.market_data:
            if shoe['markup_pct'] > 50 and shoe['sold_last_30d'] > 100:
                opportunities.append({
                    'type': 'GOLDEN_GOOSE',
                    'sku': shoe['sku'],
                    'name': shoe['name'],
                    'reason': f"High demand ({shoe['sold_last_30d']}/mo) + healthy margin ({shoe['markup_pct']:.0f}%)",
                    'profit_per_unit': shoe['current_market_price'] - shoe['retail_price'],
                    'monthly_volume_potential': shoe['sold_last_30d'],
                    'monthly_profit_potential': (shoe['current_market_price'] - shoe['retail_price']) * shoe['sold_last_30d'],
                    'confidence': 9,
                })
        
        # Opportunity 2: Large bid-ask spread = arbitrage
        for shoe in self.market_data:
            bid_ask_pct = ((shoe['ask_price'] - shoe['bid_price']) / shoe['bid_price']) * 100
            if bid_ask_pct > 4:
                opportunities.append({
                    'type': 'ARBITRAGE',
                    'sku': shoe['sku'],
                    'name': shoe['name'],
                    'reason': f"Wide bid-ask spread ({bid_ask_pct:.1f}%) - buy low, sell high",
                    'profit_per_unit': shoe['ask_price'] - shoe['bid_price'],
                    'buy_at': shoe['bid_price'],
                    'sell_at': shoe['ask_price'],
                    'confidence': 6,
                })
        
        # Opportunity 3: Low competition = potential monopoly
        for shoe in self.market_data:
            if shoe['listings_active'] < 20 and shoe['sold_last_30d'] > 50:
                opportunities.append({
                    'type': 'LOW_COMPETITION',
                    'sku': shoe['sku'],
                    'name': shoe['name'],
                    'reason': f"High demand ({shoe['sold_last_30d']}/mo) but only {shoe['listings_active']} listings",
                    'demand': shoe['sold_last_30d'],
                    'active_listings': shoe['listings_active'],
                    'confidence': 8,
                })
        
        # Sort by confidence
        opportunities.sort(key=lambda x: x['confidence'], reverse=True)
        self.opportunities = opportunities
        
        return opportunities
    
    def portfolio_analysis(self) -> Dict:
        """Analyze overall portfolio/market health."""
        if not self.market_data:
            return {}
        
        markups = [s['markup_pct'] for s in self.market_data]
        volumes = [s['sold_last_30d'] for s in self.market_data]
        
        return {
            'total_shoes_analyzed': len(self.market_data),
            'avg_markup_pct': round(statistics.mean(markups), 1),
            'median_markup_pct': round(statistics.median(markups), 1),
            'total_market_volume_30d': sum(volumes),
            'avg_listing_depth': round(statistics.mean([s['listings_active'] for s in self.market_data]), 1),
            'high_demand_volume': sum([v for v in volumes if v > 200]),
        }
    
    def export_to_csv(self, filename='sneaker_analysis.csv'):
        """Export analysis to CSV."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Type', 'SKU', 'Name', 'Details', 'Confidence', 'Potential Profit/Unit'])
            
            # Opportunities
            for opp in self.opportunities:
                details = opp.get('reason', '')
                profit = opp.get('profit_per_unit', opp.get('monthly_profit_potential', 'N/A'))
                writer.writerow([
                    opp['type'],
                    opp['sku'],
                    opp['name'],
                    details,
                    opp['confidence'],
                    profit,
                ])
        
        return filename


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_section(title):
    """Print a formatted section."""
    print(f"\n{title}")
    print(f"{'-'*len(title)}")


def main():
    """Run the analyzer with sample data."""
    
    print("\n🔥 SNEAKER MARKET ANALYZER - Opportunity Detection\n")
    
    analyzer = SneakerMarketAnalyzer()
    analyzer.load_data()
    
    # Portfolio Overview
    print_header("MARKET OVERVIEW")
    portfolio = analyzer.portfolio_analysis()
    print(f"Total Shoes Analyzed: {portfolio['total_shoes_analyzed']}")
    print(f"Total 30-Day Volume: {portfolio['total_market_volume_30d']:,} units")
    print(f"Average Markup: {portfolio['avg_markup_pct']:.1f}%")
    print(f"Median Markup: {portfolio['median_markup_pct']:.1f}%")
    
    # Margin Analysis
    print_header("MARGIN ANALYSIS")
    margins = analyzer.analyze_margins()
    
    print(f"Market Average Markup: {margins['market_avg_markup_pct']:.1f}%")
    print(f"Market Average Bid-Ask Spread: {margins['market_avg_spread_pct']:.1f}%\n")
    
    print("Top 3 Highest Markup Shoes:")
    for i, shoe in enumerate(margins['by_shoe'][:3], 1):
        print(f"  {i}. {shoe['name']}")
        print(f"     Retail: ${shoe['retail']} → Market: ${shoe['market']} (+{shoe['markup_pct']:.0f}%)")
        print()
    
    # Opportunities
    print_header("IDENTIFIED OPPORTUNITIES")
    opportunities = analyzer.identify_opportunities()
    
    opportunity_types = {}
    for opp in opportunities:
        opp_type = opp['type']
        if opp_type not in opportunity_types:
            opportunity_types[opp_type] = []
        opportunity_types[opp_type].append(opp)
    
    for opp_type, opps in sorted(opportunity_types.items()):
        print_section(f"{opp_type} ({len(opps)} found)")
        
        for opp in opps[:3]:
            print(f"\n  📦 {opp['name']}")
            print(f"     SKU: {opp['sku']}")
            print(f"     {opp['reason']}")
            print(f"     Confidence: {opp['confidence']}/10")
            
            # Type-specific details
            if opp['type'] == 'GOLDEN_GOOSE':
                print(f"     💰 Profit/Unit: ${opp['profit_per_unit']:.0f}")
                print(f"     📊 Monthly Potential: ${opp['monthly_profit_potential']:,.0f}")
            elif opp['type'] == 'ARBITRAGE':
                print(f"     💵 Buy @ ${opp['buy_at']} | Sell @ ${opp['sell_at']} (${opp['profit_per_unit']} profit)")
            elif opp['type'] == 'LOW_COMPETITION':
                print(f"     👥 {opp['active_listings']} listings for {opp['demand']} monthly sales")
    
    # Export
    print_header("EXPORT")
    csv_file = analyzer.export_to_csv()
    print(f"✅ Analysis exported to: {csv_file}")
    print(f"\nTo use:")
    print(f"  1. python3 sneaker_analyzer.py")
    print(f"  2. Load {csv_file} into Excel or Google Sheets")
    print(f"  3. Filter by opportunity type & confidence level")
    print(f"  4. Execute on high-confidence opportunities\n")


if __name__ == '__main__':
    main()

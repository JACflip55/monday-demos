#!/usr/bin/env python3
"""
Quick CLI wrapper for agrihood lookups and analysis.
Usage: ./quick_lookup.py [agrihood_name]
"""

import sys
import json
from agrihood_analyzer import AgriHoodAnalyzer, AgriHoodMetrics, DevelopmentStage, FarmType, build_sample_database


def quick_lookup(name_query: str):
    """Quick lookup and analysis for an agrihood."""
    analyzer = build_sample_database()
    
    # Find matching agrihood (case-insensitive partial match)
    matches = [a for a in analyzer.agrihoods if name_query.lower() in a.name.lower()]
    
    if not matches:
        print(f"❌ No agrihood found matching '{name_query}'")
        print(f"\nAvailable agrihoods:")
        for a in analyzer.agrihoods:
            print(f"  • {a.name} ({a.location}, {a.state})")
        return
    
    if len(matches) > 1:
        print(f"⚠️  Multiple matches found for '{name_query}':")
        for a in matches:
            print(f"  • {a.name} ({a.location}, {a.state})")
        print(f"\nShowing first match: {matches[0].name}")
    
    agrihood = matches[0]
    print(analyzer.generate_report(agrihood))


def list_all():
    """List all agrihoods with scores."""
    analyzer = build_sample_database()
    rankings = analyzer.rank_opportunities()
    
    print("\n" + "="*70)
    print("ALL AGRIHOODS - RANKED BY INVESTMENT SCORE")
    print("="*70 + "\n")
    print(f"{'Rank':<6} {'Name':<20} {'Location':<18} {'Score':<8} {'Rating':<20}")
    print("-" * 70)
    
    for i, (agrihood, analysis) in enumerate(rankings, 1):
        print(f"{i:<6} {agrihood.name:<20} {agrihood.location}, {agrihood.state:<15} "
              f"{analysis['total_score']:<8.1f} {analysis['rating']:<20}")
    
    print("\n")


def show_help():
    """Show usage help."""
    print("""
Agrihood Investment Analyzer - Quick Lookup

USAGE:
  ./quick_lookup.py [agrihood_name]    Look up specific agrihood
  ./quick_lookup.py --list             List all agrihoods
  ./quick_lookup.py --help             Show this help

EXAMPLES:
  ./quick_lookup.py serenbe
  ./quick_lookup.py willowsford
  ./quick_lookup.py agritopia
  ./quick_lookup.py --list

FULL ANALYSIS:
  ./agrihood_analyzer.py               Run complete analysis
    """)


def main():
    if len(sys.argv) < 2:
        print("❌ Missing argument")
        show_help()
        sys.exit(1)
    
    arg = sys.argv[1].lower()
    
    if arg in ['--help', '-h', 'help']:
        show_help()
    elif arg in ['--list', '-l', 'list']:
        list_all()
    else:
        quick_lookup(sys.argv[1])


if __name__ == "__main__":
    main()

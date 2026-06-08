#!/usr/bin/env python3
"""
Startup Intel Brief
====================
Pre-meeting due diligence tool for angel investors.
Score startups across 6 dimensions, generate structured investment memos.

Usage:
    python brief.py                   # run sample startups (default)
    python brief.py --startup FILE    # batch mode from JSON
    python brief.py --interactive     # enter startup details manually
    python brief.py --html            # also generate HTML report in ./output/
"""

import argparse
import json
import os
from datetime import datetime
from scorer import score_startup
from report import render_terminal, render_html

SAMPLE_FILE = os.path.join(os.path.dirname(__file__), "sample_startups.json")
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "output")


def load_startups(path):
    with open(path) as f:
        return json.load(f)


def interactive_mode():
    print(chr(10) + "Startup Intel Brief - Interactive Mode" + chr(10))
    s = {}
    s["name"]        = input("Company name: ").strip()
    s["tagline"]     = input("One-line tagline: ").strip()
    s["sector"]      = input("Sector (e.g. fintech, SaaS, marketplace): ").strip()
    s["stage"]       = input("Stage (pre-seed / seed / Series A): ").strip()
    s["founded"]     = input("Founded year: ").strip()
    s["team_size"]   = input("Team size: ").strip()
    s["description"] = input("Describe the product/business:" + chr(10) + "> ").strip()
    print(chr(10) + "Traction (leave blank if unknown):")
    s["arr"]         = input("  ARR / revenue: ").strip()
    s["growth"]      = input("  MoM or YoY growth %: ").strip()
    s["users"]       = input("  Users / customers: ").strip()
    print(chr(10) + "Team:")
    s["founders"]    = input("  Founder backgrounds: ").strip()
    s["prior_exits"] = input("  Prior exits? (y/n): ").strip().lower() == "y"
    print(chr(10) + "Moat:")
    s["moat"]        = input("  Competitive advantages: ").strip()
    print(chr(10) + "Risks:")
    s["risks"]       = input("  Key risks (comma-separated): ").strip()
    print(chr(10) + "Deal:")
    s["raise"]       = input("  Raising ($): ").strip()
    s["valuation"]   = input("  Valuation cap/pre-money ($): ").strip()
    s["url"]         = input("  Website or deck URL: ").strip()
    return [s]


def main():
    parser = argparse.ArgumentParser(description="Startup Intel Brief - pre-meeting due diligence scorer")
    parser.add_argument("--startup",     help="Path to JSON file with startup(s) data")
    parser.add_argument("--interactive", action="store_true", help="Enter startup details interactively")
    parser.add_argument("--html",        action="store_true", help="Also generate HTML report in ./output/")
    args = parser.parse_args()

    if args.interactive:
        startups = interactive_mode()
    elif args.startup:
        startups = load_startups(args.startup)
    else:
        startups = load_startups(SAMPLE_FILE)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = [score_startup(s) for s in startups]
    results.sort(key=lambda x: x["total_score"], reverse=True)

    render_terminal(results)

    if args.html:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_path = os.path.join(OUTPUT_DIR, "brief_{}.html".format(ts))
        render_html(results, html_path)
        print(chr(10) + "HTML report saved to: " + html_path)

    print(chr(10) + "Analyzed {} startup(s). Run with --html for full HTML report.".format(len(results)))


if __name__ == "__main__":
    main()

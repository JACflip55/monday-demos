"""
Scoring engine for Startup Intel Brief.

Six dimensions, each scored 0-10:
  1. Market Opportunity  - size, growth, TAM signals
  2. Traction            - revenue, users, growth rate
  3. Team Strength       - experience, prior exits, domain expertise
  4. Competitive Moat    - defensibility, IP, network effects
  5. Deal Quality        - valuation, stage fit, terms
  6. Investor Fit        - alignment with Jack's thesis

Verdict thresholds:
  80+   STRONG PASS - schedule call
  65-79 SOFT PASS - worth a closer look
  50-64 MAYBE - needs more info
  <50   PASS - not the right fit right now
"""

import re


def _parse_money(s):
    if not s:
        return 0
    s = str(s).upper().replace(",", "").replace("$", "").strip()
    m = re.match(r"([0-9.]+)\s*([KMB]?)", s)
    if not m:
        return 0
    val = float(m.group(1))
    suffix = m.group(2)
    return val * {"K": 1e3, "M": 1e6, "B": 1e9}.get(suffix, 1)


def _parse_pct(s):
    if not s:
        return 0
    s = str(s).replace("%", "").replace("x", "").strip()
    try:
        return float(s)
    except ValueError:
        return 0


def score_market(startup):
    sector = startup.get("sector", "").lower()
    desc = startup.get("description", "").lower()
    combined = sector + " " + desc
    score = 5
    big_market_kws = [
        "billion", "trillion", "global", "enterprise", "platform",
        "marketplace", "infrastructure", "b2b", "saas", "fintech",
        "healthcare", "logistics", "supply chain", "ai", "automation"
    ]
    niche_kws = ["niche", "local", "single city", "very small", "boutique"]
    score += min(4, sum(1 for kw in big_market_kws if kw in combined))
    score -= sum(1 for kw in niche_kws if kw in combined)
    stage = startup.get("stage", "").lower()
    if "series a" in stage:
        score += 1
    return max(0, min(10, score))


def score_traction(startup):
    arr = _parse_money(startup.get("arr", ""))
    growth = _parse_pct(startup.get("growth", ""))
    users = startup.get("users", "")
    score = 0
    if arr >= 5e6:
        score += 4
    elif arr >= 1e6:
        score += 3
    elif arr >= 500e3:
        score += 2
    elif arr >= 100e3:
        score += 1
    elif arr > 0:
        score += 0.5
    if growth >= 300:
        score += 4
    elif growth >= 100:
        score += 3
    elif growth >= 50:
        score += 2
    elif growth >= 20:
        score += 1
    elif growth > 0:
        score += 0.5
    if users:
        users_lower = users.lower()
        if any(x in users_lower for x in ["10k", "100k", "1m", "million", "10,000", "100,000"]):
            score += 2
        elif any(x in users_lower for x in ["1k", "5k", "1,000", "5,000"]):
            score += 1
        else:
            score += 0.5
    return max(0, min(10, score))


def score_team(startup):
    founders = startup.get("founders", "").lower()
    prior_exits = startup.get("prior_exits", False)
    team_size = str(startup.get("team_size", "")).lower()
    score = 4
    if prior_exits or "exit" in founders or "acquired" in founders or "ipo" in founders:
        score += 3
    domain_kws = [
        "phd", "ex-google", "ex-facebook", "ex-meta", "ex-amazon", "ex-stripe",
        "ex-uber", "ex-airbnb", "ex-yc", "y combinator", "stanford", "mit",
        "harvard", "10 years", "expert", "built", "founded", "operator",
        "ex-", "former", "cto", "engineer", "product"
    ]
    score += min(3, sum(1 for kw in domain_kws if kw in founders))
    if team_size.isdigit():
        n = int(team_size)
        if 2 <= n <= 15:
            score += 1
    return max(0, min(10, score))


def score_moat(startup):
    moat = startup.get("moat", "").lower()
    desc = startup.get("description", "").lower()
    combined = moat + " " + desc
    score = 3
    strong_moat_kws = [
        "patent", "ip", "proprietary", "network effect", "switching cost",
        "data moat", "exclusive", "license", "regulatory", "brand",
        "viral", "platform", "ecosystem", "lock-in", "first mover",
        "unique data", "trained model", "10x better"
    ]
    weak_moat_kws = [
        "just like", "similar to", "competitive market", "many competitors",
        "no moat", "commodity", "easy to copy"
    ]
    score += min(5, sum(1 for kw in strong_moat_kws if kw in combined))
    score -= sum(1 for kw in weak_moat_kws if kw in combined)
    return max(0, min(10, score))


def score_deal(startup):
    valuation = _parse_money(startup.get("valuation", ""))
    arr = _parse_money(startup.get("arr", ""))
    stage = startup.get("stage", "").lower()
    raise_amt = _parse_money(startup.get("raise", ""))
    score = 5
    if arr > 0 and valuation > 0:
        multiple = valuation / arr
        if multiple <= 10:
            score += 3
        elif multiple <= 20:
            score += 2
        elif multiple <= 40:
            score += 1
        else:
            score -= 1
    elif valuation > 0:
        if "pre-seed" in stage and valuation <= 5e6:
            score += 2
        elif "seed" in stage and valuation <= 15e6:
            score += 2
        elif "series a" in stage and valuation <= 30e6:
            score += 1
        elif valuation > 50e6:
            score -= 2
    if raise_amt > 0 and valuation > 0:
        dilution = raise_amt / valuation
        if 0.05 <= dilution <= 0.25:
            score += 1
    return max(0, min(10, score))


def score_fit(startup):
    thesis_kws = [
        "angel", "investor", "investment", "startup", "founder", "venture",
        "e-commerce", "ecommerce", "marketplace", "resale", "sneaker",
        "automation", "productivity", "workflow", "ai", "saas", "b2b",
        "fintech", "payments", "data", "analytics", "platform", "tools"
    ]
    text = " ".join([
        startup.get("description", ""),
        startup.get("sector", ""),
        startup.get("tagline", ""),
        startup.get("moat", ""),
    ]).lower()
    score = 3
    matches = sum(1 for kw in thesis_kws if kw in text)
    score += min(7, matches)
    return max(0, min(10, score))


WEIGHTS = {
    "market":   0.20,
    "traction": 0.25,
    "team":     0.20,
    "moat":     0.15,
    "deal":     0.10,
    "fit":      0.10,
}


def score_startup(startup):
    """Score a startup dict and return enriched result with scores and verdict."""
    scores = {
        "market":   score_market(startup),
        "traction": score_traction(startup),
        "team":     score_team(startup),
        "moat":     score_moat(startup),
        "deal":     score_deal(startup),
        "fit":      score_fit(startup),
    }
    total = sum(scores[dim] * WEIGHTS[dim] * 10 for dim in scores)
    total = round(total, 1)

    if total >= 80:
        verdict = "STRONG PASS - schedule a call"
        verdict_short = "STRONG PASS"
        color = "green"
    elif total >= 65:
        verdict = "SOFT PASS - worth a closer look"
        verdict_short = "SOFT PASS"
        color = "cyan"
    elif total >= 50:
        verdict = "MAYBE - needs more info"
        verdict_short = "MAYBE"
        color = "yellow"
    else:
        verdict = "PASS - not the right fit"
        verdict_short = "PASS"
        color = "red"

    highlights = []
    if scores["traction"] >= 7:
        highlights.append("Strong traction signal")
    if scores["team"] >= 7:
        highlights.append("High-conviction team")
    if scores["moat"] >= 7:
        highlights.append("Defensible moat")
    if scores["deal"] <= 3:
        highlights.append("WARNING: Valuation looks stretched")
    if scores["traction"] <= 2:
        highlights.append("Low/no traction yet - early bet")
    if scores["market"] >= 8:
        highlights.append("Massive addressable market")

    questions = _generate_questions(startup, scores)

    return {
        **startup,
        "scores": scores,
        "total_score": total,
        "verdict": verdict,
        "verdict_short": verdict_short,
        "verdict_color": color,
        "highlights": highlights,
        "questions": questions,
    }


def _generate_questions(startup, scores):
    questions = []
    if scores["traction"] < 5:
        questions.append("What is your current ARR / MRR and month-over-month growth rate?")
    if scores["team"] < 5:
        questions.append("Walk me through why YOU are the right team for this specific problem.")
    if scores["moat"] < 5:
        questions.append("Why will you be hard to copy in 3 years? What is your long-term defensibility?")
    if scores["market"] < 5:
        questions.append("What is the total addressable market and who is your beachhead customer?")
    if scores["deal"] < 5:
        questions.append("How did you arrive at this valuation? What are comparable rounds?")
    questions.append("What does the path to $10M ARR look like — key milestones and assumptions?")
    questions.append("Who else is on your cap table? Any lead investors already committed?")
    if not startup.get("arr"):
        questions.append("When do you expect to reach first revenue / product-market fit?")
    return questions[:5]

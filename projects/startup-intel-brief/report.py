"""
Report renderers for Startup Intel Brief.
- render_terminal: ANSI-colored terminal output
- render_html: full styled HTML report
"""

from datetime import datetime


RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"

COLOR_MAP = {"green": GREEN, "cyan": CYAN, "yellow": YELLOW, "red": RED}
BAR_LEN   = 10

DIMENSION_LABELS = {
    "market":   "Market Opportunity",
    "traction": "Traction          ",
    "team":     "Team Strength     ",
    "moat":     "Competitive Moat  ",
    "deal":     "Deal Quality      ",
    "fit":      "Investor Fit      ",
}

EMOJI = {
    "green":  "\u2b50",
    "cyan":   "\u2705",
    "yellow": "\U0001f7e0",
    "red":    "\u274c",
}


def _bar(score, max_score=10):
    filled = round((score / max_score) * BAR_LEN)
    color = GREEN if score >= 7 else YELLOW if score >= 5 else RED
    return color + "\u2588" * filled + DIM + "\u2591" * (BAR_LEN - filled) + RESET


def _score_color(score):
    if score >= 7:
        return GREEN
    if score >= 5:
        return YELLOW
    return RED


def render_terminal(results):
    width = 68
    sep = "\u2500" * width
    nl = chr(10)
    print(nl + BOLD + WHITE + sep)
    print("  \U0001f50d  STARTUP INTEL BRIEF  \u00b7  " + datetime.now().strftime("%b %d, %Y  %H:%M UTC"))
    print(sep + RESET)
    for r in results:
        vc = COLOR_MAP.get(r["verdict_color"], WHITE)
        em = EMOJI.get(r["verdict_color"], "")
        print(nl + BOLD + WHITE + r["name"].upper() + RESET + "  " + DIM + r.get("tagline", "") + RESET)
        info_parts = [
            r.get("sector", ""),
            r.get("stage", ""),
            "Founded " + r.get("founded", "?"),
            r.get("team_size", "?") + " people",
        ]
        print("  " + DIM + " \u00b7 ".join(p for p in info_parts if p and p.strip()) + RESET)
        if r.get("url"):
            print("  " + DIM + "\U0001f517 " + r["url"] + RESET)
        if r.get("description"):
            print(nl + "  " + r["description"])
        print(nl + "  " + BOLD + "SCORE   " + vc + str(r["total_score"]) + "/100" + RESET)
        print("  " + BOLD + "VERDICT " + vc + em + " " + r["verdict"] + RESET + nl)
        print("  " + BOLD + "{:<22}  {:>6}  BAR".format("DIMENSION", "SCORE") + RESET)
        print("  " + sep[:58])
        for dim, label in DIMENSION_LABELS.items():
            s = r["scores"][dim]
            sc = _score_color(s)
            print("  " + sc + label + RESET + "  " + sc + "{:>5.1f}/10".format(s) + RESET + "  " + _bar(s))
        if r["highlights"]:
            print(nl + "  " + BOLD + "KEY SIGNALS:" + RESET)
            for h in r["highlights"]:
                print("    \u2022 " + h)
        if r["questions"]:
            print(nl + "  " + BOLD + "ASK IN THE MEETING:" + RESET)
            for i, q in enumerate(r["questions"], 1):
                print("    " + DIM + str(i) + "." + RESET + " " + q)
        deal_parts = []
        if r.get("raise"):
            deal_parts.append("Raising: " + r["raise"])
        if r.get("valuation"):
            deal_parts.append("Val: " + r["valuation"])
        if r.get("arr"):
            deal_parts.append("ARR: " + r["arr"])
        if deal_parts:
            print(nl + "  " + DIM + "\U0001f4b0 " + " \u00b7 ".join(deal_parts) + RESET)
        print(nl + "  " + sep)
    if len(results) > 1:
        print(nl + BOLD + "  RANKING SUMMARY" + RESET)
        print("  " + "{:<3}  {:<25}  {:>5}  {}".format("#", "Company", "Score", "Verdict"))
        print("  " + "\u2500" * 52)
        for i, r in enumerate(results, 1):
            vc = COLOR_MAP.get(r["verdict_color"], WHITE)
            em = EMOJI.get(r["verdict_color"], "")
            print("  " + "{:<3}  {:<25}  ".format(i, r["name"]) + vc + "{:>5}".format(r["total_score"]) + RESET + "  " + vc + em + " " + r["verdict_short"] + RESET)
        print()


HTML_COLORS = {
    "green":  "#22c55e",
    "cyan":   "#06b6d4",
    "yellow": "#f59e0b",
    "red":    "#ef4444",
}


def _html_bar(score):
    pct   = (score / 10) * 100
    color = "#22c55e" if score >= 7 else "#f59e0b" if score >= 5 else "#ef4444"
    return (
        '<div style="background:#0f172a;border-radius:4px;height:10px;width:140px;'
        'display:inline-block;vertical-align:middle;">'
        '<div style="background:{c};width:{p:.0f}%;height:100%;border-radius:4px;"></div></div>'.format(c=color, p=pct)
    )


def _td(content, style=""):
    return "<td style='{}'>{}</td>".format(style, content)


def render_html(results, path):
    cards = ""
    for r in results:
        vc = HTML_COLORS.get(r["verdict_color"], "#94a3b8")
        dim_rows = ""
        for dim, label in DIMENSION_LABELS.items():
            s = r["scores"][dim]
            sc = "#22c55e" if s >= 7 else "#f59e0b" if s >= 5 else "#ef4444"
            dim_rows += (
                "<tr>"
                + _td(label.strip(), "padding:6px 16px;color:#94a3b8;")
                + _td("{:.1f}/10".format(s), "padding:6px 8px;color:{};font-weight:700;".format(sc))
                + _td(_html_bar(s), "padding:6px 8px;")
                + "</tr>"
            )
        highlights_html = "".join(
            "<li style='margin:4px 0;color:#94a3b8;'>{}</li>".format(h)
            for h in r.get("highlights", [])
        )
        questions_html = "".join(
            "<li style='margin:6px 0;color:#94a3b8;'>{}</li>".format(q)
            for q in r.get("questions", [])
        )
        deal_parts = []
        if r.get("raise"):
            deal_parts.append("Raising: " + r["raise"])
        if r.get("valuation"):
            deal_parts.append("Valuation: " + r["valuation"])
        if r.get("arr"):
            deal_parts.append("ARR: " + r["arr"])
        deal_html = (
            "<p style='color:#60a5fa;margin:12px 0;font-size:0.9rem;'>&#x1F4B0; {}</p>".format(
                " &middot; ".join(deal_parts)
            )
        ) if deal_parts else ""
        url_html = (
            "<p style='margin:4px 0 0;'>"
            "<a href='{u}' style='color:#60a5fa;font-size:0.9rem;'>{u}</a></p>".format(u=r["url"])
        ) if r.get("url") else ""
        desc_html = (
            "<p style='color:#cbd5e1;margin:16px 0;line-height:1.6;'>{}</p>".format(r["description"])
        ) if r.get("description") else ""
        sig = ""
        if highlights_html:
            sig += (
                "<div><h4 style='color:#f1f5f9;margin:0 0 10px;font-size:0.95rem;'>Key Signals</h4>"
                "<ul style='margin:0;padding-left:18px;'>{}</ul></div>".format(highlights_html)
            )
        if questions_html:
            sig += (
                "<div><h4 style='color:#f1f5f9;margin:0 0 10px;font-size:0.95rem;'>Ask in the Meeting</h4>"
                "<ol style='margin:0;padding-left:18px;'>{}</ol></div>".format(questions_html)
            )
        info_line = " &middot; ".join(filter(None, [
            r.get("tagline", ""), r.get("sector", ""), r.get("stage", ""),
            (r.get("team_size", "") + " people") if r.get("team_size") else "",
        ]))
        cards += (
            "<div style='background:#1e293b;border-radius:12px;padding:28px 32px;"
            "margin-bottom:24px;border-left:5px solid {vc};'>"
            "<div style='display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;'>"
            "<div><h2 style='margin:0;color:#f1f5f9;font-size:1.5rem;'>{name}</h2>"
            "<p style='margin:6px 0 0;color:#64748b;'>{info}</p>{url}</div>"
            "<div style='text-align:right;min-width:90px;'>"
            "<div style='font-size:2.8rem;font-weight:800;color:{vc};line-height:1;'>{score}</div>"
            "<div style='color:#475569;font-size:0.8rem;'>/100</div>"
            "<div style='color:{vc};font-weight:600;font-size:0.9rem;margin-top:6px;'>{verdict}</div>"
            "</div></div>{desc}{deal}"
            "<table style='border-collapse:collapse;width:100%;margin:16px 0;'>"
            "<tr style='border-bottom:1px solid #334155;'>"
            "<th style='padding:6px 16px;text-align:left;color:#475569;font-size:0.85rem;'>DIMENSION</th>"
            "<th style='padding:6px 8px;text-align:left;color:#475569;font-size:0.85rem;'>SCORE</th>"
            "<th style='padding:6px 8px;text-align:left;color:#475569;font-size:0.85rem;'>BAR</th>"
            "</tr>{rows}</table>"
            "<div style='display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px;'>{sig}</div>"
            "</div>"
        ).format(
            vc=vc, name=r["name"], info=info_line, url=url_html,
            score=r["total_score"], verdict=r["verdict_short"],
            desc=desc_html, deal=deal_html, rows=dim_rows, sig=sig,
        )

    summary_rows = ""
    for i, r in enumerate(results, 1):
        vc = HTML_COLORS.get(r["verdict_color"], "#94a3b8")
        summary_rows += (
            "<tr style='border-bottom:1px solid #0f172a;'>"
            + _td(str(i), "padding:10px 16px;color:#475569;")
            + _td(r["name"], "padding:10px 16px;color:#f1f5f9;font-weight:600;")
            + _td(r.get("sector", ""), "padding:10px 16px;color:#94a3b8;font-size:0.9rem;")
            + _td(str(r["total_score"]), "padding:10px 16px;color:{};font-weight:700;font-size:1.1rem;".format(vc))
            + _td(r["verdict_short"], "padding:10px 16px;color:{};font-weight:600;".format(vc))
            + "</tr>"
        )
    summary_section = ""
    if len(results) > 1:
        summary_section = (
            "<div style='background:#1e293b;border-radius:12px;overflow:hidden;margin-bottom:28px;'>"
            "<table style='border-collapse:collapse;width:100%;'>"
            "<tr style='border-bottom:1px solid #334155;'>"
            "<th style='padding:12px 16px;text-align:left;color:#475569;font-size:0.85rem;'>#</th>"
            "<th style='padding:12px 16px;text-align:left;color:#475569;font-size:0.85rem;'>COMPANY</th>"
            "<th style='padding:12px 16px;text-align:left;color:#475569;font-size:0.85rem;'>SECTOR</th>"
            "<th style='padding:12px 16px;text-align:left;color:#475569;font-size:0.85rem;'>SCORE</th>"
            "<th style='padding:12px 16px;text-align:left;color:#475569;font-size:0.85rem;'>VERDICT</th>"
            "</tr>{rows}</table></div>"
        ).format(rows=summary_rows)

    dt = datetime.now()
    html = (
        "<!DOCTYPE html>"
        "<html lang='en'><head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>Startup Intel Brief &mdash; {date}</title>"
        "<style>* {{ box-sizing: border-box; margin: 0; padding: 0; }}"
        "body {{ background: #0f172a; color: #e2e8f0; "
        "font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; "
        "padding: 32px 24px; line-height: 1.5; }}"
        "a {{ color: #60a5fa; text-decoration: none; }}"
        "a:hover {{ text-decoration: underline; }}"
        "</style></head><body>"
        "<div style='max-width:920px;margin:0 auto;'>"
        "<div style='border-bottom:1px solid #1e293b;padding-bottom:24px;margin-bottom:32px;'>"
        "<h1 style='font-size:2rem;font-weight:800;'>&#x1F50D; Startup Intel Brief</h1>"
        "<p style='color:#475569;margin-top:6px;'>Generated {dt_str} &middot; {count} startup{plural} analyzed</p>"
        "</div>{summary}{cards}"
        "<p style='color:#1e293b;text-align:center;margin-top:40px;font-size:0.8rem;'>"
        "Generated by Startup Intel Brief &middot; "
        "<a href='https://github.com/JACflip55/monday-demos' style='color:#334155;'>"
        "github.com/JACflip55/monday-demos</a></p>"
        "</div></body></html>"
    ).format(
        date=dt.strftime("%b %d, %Y"),
        dt_str=dt.strftime("%B %d, %Y at %H:%M UTC"),
        count=len(results),
        plural="s" if len(results) != 1 else "",
        summary=summary_section,
        cards=cards,
    )

    with open(path, "w") as fh:
        fh.write(html)

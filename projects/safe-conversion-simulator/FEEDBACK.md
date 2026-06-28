# Feedback — SAFE Conversion Simulator

## Jun 29, 2026

**What was built:** Interactive SAFE conversion simulator — model how SAFEs convert at a priced round, stack multiple SAFEs with different terms, see ownership breakdown, compare scenarios.

---

### Questions for Jack

1. **Does the conversion math match your understanding?** The simulator uses standard pre-money SAFE mechanics (convert at lower of cap price vs. discount price). Does this match what you've seen in actual term sheets?

2. **Post-money SAFEs:** The YC post-money SAFE (2018) works differently — the investor's ownership is fixed regardless of other SAFEs. Would you like a dedicated post-money mode that shows the "SAFE holder gets exactly X% regardless" mechanic more clearly?

3. **Real scenarios:** If you share a deal you're looking at (SAFE amount, cap, discount), I can pre-load it as a scenario. Would that be useful?

4. **Missing features?**
   - [ ] Convertible note mode (interest rate + maturity)
   - [ ] MFN (Most Favored Nation) clause modeling
   - [ ] Multiple rounds (Seed → A → B dilution cascade)
   - [ ] "Investor view" vs "Founder view" toggle
   - [ ] Export ownership table to PDF/image

5. **Connection to Portfolio Math:** Last week's demo showed "you need 20-30 deals at $50-100K checks." This week shows what % ownership each check actually buys. Want me to connect them — e.g., "at typical SAFE terms, your $100K check = X% ownership"?

6. **Next iteration ideas:**
   - [ ] Add pro-rata exercise calculator (cost to maintain ownership in Series A)
   - [ ] Side letter terms (information rights, board observer, etc.)
   - [ ] "Red flags in SAFE terms" educational section
   - [ ] Link to real YC SAFE templates

---

### Meta

- [ ] Was it easy to use on mobile?
- [ ] Did the "Learn" tab add value, or is it too basic for you?
- [ ] Preferred topic for next week?

# Feedback — Angel Portfolio Math

## Jun 22, 2026

**What was built:** Monte Carlo angel portfolio simulator — interactive HTML demo with sliders for deals/check/follow-on, real-time distribution charts, strategy comparison, and power law education.

---

### Questions for Jack

1. **Does the outcome distribution feel right?** The probabilities are based on AngelList/Kauffman data (40% total loss, 1% unicorn). Does this match your experience?

2. **Follow-on modeling:** Currently models follow-on as "double down on anything tracking 3x+". Would you prefer more nuanced follow-on logic (e.g., signal-based, round-specific)?

3. **What's your actual strategy?** If you share your target (# deals/year, check size, fund size), I can pre-load the demo with your parameters as the default.

4. **Missing dimensions?**
   - Should it model time-to-exit (IRR vs. MOIC)?
   - Vintage year effects (market cycles)?
   - Sector concentration risk?
   - SAFE vs. priced round mechanics?

5. **Useful as a tool?** Would you want this deployed as a Streamlit app you can share with other angels, or is the HTML demo sufficient?

6. **Next iteration ideas:**
   - [ ] Add "your portfolio" mode — input your actual deals and see projected outcomes
   - [ ] Model specific scenarios (recession, AI boom, etc.)
   - [ ] Export to PDF for LP reports
   - [ ] Add IRR modeling with time-to-exit assumptions

---

### Meta

- [ ] Was the demo easy to review on mobile?
- [ ] Was it engaging enough to actually play with?
- [ ] Preferred topic for next week?

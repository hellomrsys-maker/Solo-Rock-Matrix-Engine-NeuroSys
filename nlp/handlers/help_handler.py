"""Help handler for natural language queries."""


class HelpHandler:
    """Provides help and examples for natural language queries."""

    def handle(self, entities: dict) -> dict:
        """
        Provide help information.

        Args:
            entities: Dict with extracted entities (not used)

        Returns:
            dict with help content
        """
        return {
            'type': 'help',
            'title': 'SOLO ROCK Natural Language Guide',
            'content': self.get_help_text(),
        }

    def get_help_text(self) -> str:
        """Get comprehensive help text."""
        return """
## SOLO ROCK Natural Language Interface

Ask questions about your system's performance and behavior. The system understands natural language queries and converts them to actions.

### What You Can Ask

#### 📊 Reports & Summaries
Generate system reports with key metrics and insights.

**Examples:**
- "show me a report"
- "generate a summary"
- "what happened last hour"
- "create a detailed report"

**What you'll get:**
- System health status (Healthy, Warning, Critical)
- Temperature and load metrics
- Decision distribution (how often FULL_RATE, BATCH, THROTTLE, EMERGENCY were active)
- Thermal and load trends
- Recommendations for optimization

---

#### 📈 Current Status
Check the current health and performance of your system.

**Examples:**
- "how is it working"
- "what is the current status"
- "is everything ok"
- "show me the status"

**What you'll get:**
- Overall system health indicator
- Current CPU temperature and load
- RAM usage percentage
- Active routing decision (FULL_RATE, BATCH, THROTTLE, EMERGENCY)
- Reason for the current decision

---

#### 📉 Trend Analysis
Analyze historical data and detect patterns.

**Examples:**
- "analyze the data"
- "show me trends"
- "what changed"
- "analyze trends for the last day"

**What you'll get:**
- Temperature trend (rising, falling, stable)
- CPU load trend
- Average, peak, and minimum values for each metric
- Decision distribution over the time period
- Statistical analysis (standard deviation, averages)

**Time ranges supported:**
- "last hour" (default)
- "last day"
- "last week"

---

#### ⚙️ Configuration
Adjust system thresholds (requires config access).

**Examples:**
- "change thermal warning to 75"
- "update cpu threshold to 80"
- "set critical temperature to 90"

**Note:** Configuration changes affect how decisions are made. See `/docs/CONFIGURATION.md` for details.

---

#### 🔔 Alerts
Set up notifications for system events (requires alerting config).

**Examples:**
- "set up email alerts"
- "enable slack notifications"
- "alert me on emergency"

**Note:** See `/docs/WEB_SETUP.md` for alert configuration.

---

### System Concepts

**SOLO ROCK Routing Decisions:**
1. **FULL_RATE** ✅
   - System healthy, all tasks dispatched immediately
   - Used when: CPU temp < warning, load < high threshold

2. **BATCH** ⚡
   - CPU temperature or load elevated
   - Similar tasks are batched together to reduce overhead
   - Used when: temp warning threshold exceeded OR load > 85%

3. **THROTTLE** ⚠️
   - System approaching thermal limits
   - Task dispatch is paced (delayed) to give hardware cooling time
   - Used when: temp > warning threshold

4. **EMERGENCY** 🚨
   - Critical thermal or memory conditions detected
   - Aggressive throttling, non-essential processes terminated
   - Used when: temp >= critical OR RAM >= critical

**Key Metrics:**
- **Temperature:** CPU core temperature in Celsius (affects thermal decisions)
- **CPU Load:** Percentage of CPU cores in use (affects batch/throttle decisions)
- **RAM Usage:** Percentage of system memory in use (affects emergency detection)
- **Decision:** Current routing decision affecting task dispatch

---

### Example Conversations

**Session 1: Check System Health**
```
You: "is everything ok"
SOLO ROCK: ✅ System is healthy
  - CPU: 52°C, 45% load
  - RAM: 65%
  - Decision: FULL_RATE (full dispatch)
```

**Session 2: Investigate Thermal Spike**
```
You: "show me trends"
SOLO ROCK: [Analysis for last hour]
  - Temperature: Rising (avg 50°C → peak 68°C)
  - Load: Stable (avg 48%)
  - THROTTLE active 15% of time to manage thermal rise
  - Recommendation: Review workload, verify cooling
```

**Session 3: Generate Full Report**
```
You: "generate a report"
SOLO ROCK: [Detailed report with all metrics, issues, recommendations]
```

---

### Tips

1. **Be specific:** "show trends for the last day" is better than just "trends"
2. **Ask naturally:** Use conversational English, not commands
3. **Ask one thing at a time:** One query per question for best results
4. **Check examples:** Look at "Example Queries" below the input box

---

### Don't Know What to Ask?

Try these starter queries:
- "how is it working"
- "show me a report"
- "analyze the data"
- "what's the status"

Or just type "help" and we'll show this guide again.

---

### Troubleshooting

**Q: "I don't understand that"**
- Try simpler phrasing or one of the example queries above

**Q: No data available**
- System has been monitoring for < 1 hour with no events
- Keep monitoring; data will accumulate over time

**Q: Configuration changes not working**
- Verify you have write access to `config/thresholds.yaml`
- Restart monitoring after config changes

---

For more information, see:
- `/docs/WEB_SETUP.md` — Web dashboard setup
- `/docs/NLU_GUIDE.md` — Natural language query examples
- `/docs/CONFIGURATION.md` — Threshold tuning
- `/README.md` — System overview
"""

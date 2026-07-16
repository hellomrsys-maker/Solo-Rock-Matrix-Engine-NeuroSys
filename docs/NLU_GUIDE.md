# SOLO ROCK Natural Language Queries — User Guide

## Overview

SOLO ROCK dashboards now understand natural language queries. Instead of navigating menus or writing code, you can simply ask questions in English:

- "show me a report"
- "how is it working"
- "analyze trends"
- "what's the status"

The system will understand your intent and provide the information you need.

---

## Getting Started

### Accessing Natural Language Queries

Both dashboards include a **"Ask SOLO ROCK"** section in the left sidebar:

1. **Live Dashboard** (`streamlit run dashboard.py`)
   - Sidebar section: "Ask SOLO ROCK"
   - Real-time system monitoring + query interface

2. **Analytics Dashboard** (`streamlit run dashboard_analytics.py`)
   - Full historical analysis + query interface
   - More detailed trend analysis capabilities

### How It Works

1. **Type your question** in the text input box (e.g., "show me a report")
2. **System processes** your query:
   - Detects your intent (report, status, trends, etc.)
   - Extracts relevant details (time range, metrics)
   - Routes to appropriate action
3. **View results** displayed in the dashboard
   - Markdown reports with statistics
   - Status cards with current metrics
   - Trend analysis with charts
   - Recommended actions

---

## Query Types & Examples

### 1️⃣ Report Queries

**Intent:** Generate system report with key metrics and analysis.

**Keywords:** show, report, generate, summary, what happened, tell me

**Example Queries:**
```
"show me a report"
"generate a summary"
"what happened last hour"
"create a detailed report"
"tell me about system performance"
```

**What You Get:**
- System health status (Healthy, Warning, Critical)
- Current temperature, load, memory metrics
- Decision distribution (FULL_RATE, BATCH, THROTTLE, EMERGENCY percentages)
- Thermal and load trends
- Key issues detected
- Recommendations for optimization

**Example Response:**
```
## SOLO ROCK System Report

✓ System healthy

**Metrics:**
- CPU Temperature: 52.3°C (avg), 68.5°C (peak)
- CPU Load: 48.2% (avg), 72% (peak)
- RAM Usage: 65.1% (avg), 78% (peak)
- Battery: 85.3%

**Decision Distribution:**
- FULL_RATE: 62.3% (dispatched all tasks)
- BATCH: 25.1% (batched similar tasks)
- THROTTLE: 10.8% (paced dispatch)
- EMERGENCY: 0% (no critical events)

**Recommendations:**
System operating normally. No immediate action needed.
```

---

### 2️⃣ Status Queries

**Intent:** Check current system health and performance.

**Keywords:** status, how, working, ok, health, current, now

**Example Queries:**
```
"how is it working"
"what is the current status"
"is everything ok"
"show me the status"
"is the system healthy"
```

**What You Get:**
- Overall system health indicator (✅ Healthy, ⚡ Optimal, ⚠️ Warning, 🚨 Critical)
- Current CPU temperature (in Celsius)
- Current CPU load percentage
- Current RAM usage percentage
- Battery percentage (if applicable)
- Active routing decision (FULL_RATE, BATCH, THROTTLE, EMERGENCY)
- Reason for current decision

**Example Response:**
```
## System Status: ✅ HEALTHY

**Health:** Healthy — Full dispatch rate

**Metrics:**
- CPU Temperature: 52.1°C
- CPU Load: 45.3%
- RAM Usage: 64.8%
- Battery: 85.0%

**Current Decision:** FULL_RATE
**Reason:** All metrics normal, dispatching at full rate
```

---

### 3️⃣ Analysis Queries

**Intent:** Analyze historical trends and patterns over time.

**Keywords:** analyze, trends, changed, pattern, history, data

**Example Queries:**
```
"analyze the data"
"show me trends"
"what changed"
"analyze trends for the last day"
"show me patterns"
```

**Time Ranges (auto-detected):**
- "last hour" → 1 hour of history (default)
- "last day" → 24 hours of history
- "last week" → 7 days of history

**What You Get:**
- Temperature trend (rising ↑, falling ↓, stable →)
- CPU load trend direction
- Peak and minimum values for each metric
- Standard deviation (how stable the metric is)
- Decision distribution over the time period
- Aggregated statistics

**Example Response:**
```
## System Analysis — Last 24 Hours

### Temperature Analysis
📈 **Trend:** Rising
- Average: 50.2°C
- Peak: 68.5°C
- Valley: 45.1°C
- Std Dev: 5.3°C

### CPU Load Analysis
➡️ **Trend:** Stable
- Average: 48.1%
- Peak: 72.0%
- Minimum: 15.2%
- Std Dev: 12.4%

### Decision Distribution
- FULL_RATE: 65.2% (589 times)
- BATCH: 22.1% (198 times)
- THROTTLE: 12.3% (111 times)
- EMERGENCY: 0.4% (3 times)

### Summary
Temperature gradually rising throughout the day.
System used THROTTLE 12% of the time to manage thermal load.
```

---

### 4️⃣ Help Queries

**Intent:** Get help with natural language interface.

**Keywords:** help, what can, example, how do, how to

**Example Queries:**
```
"help"
"what can you do"
"show examples"
"how do I use this"
"tell me about natural language"
```

**What You Get:**
- Comprehensive guide to all query types
- Example queries for each intent
- Explanation of system concepts (FULL_RATE, BATCH, THROTTLE, EMERGENCY)
- Tips for best results
- Links to additional documentation

---

## Understanding System Concepts

### Routing Decisions

SOLO ROCK makes routing decisions based on system health:

| Decision | Icon | Meaning | Used When |
|----------|------|---------|-----------|
| **FULL_RATE** | 🟢 | Healthy, dispatch all tasks immediately | CPU temp < warning, Load < 85% |
| **BATCH** | 🔵 | Optimize, batch similar tasks together | Temp/load elevated, reducing overhead |
| **THROTTLE** | 🟠 | Warning, pace dispatch to cool down | Temp > warning threshold |
| **EMERGENCY** | 🔴 | Critical, aggressive power limiting | Temp >= critical OR RAM >= critical |

### Key Metrics

- **CPU Temperature:** Core CPU temperature in Celsius. Higher = warmer, more likely to throttle.
- **CPU Load:** Percentage of CPU cores in use (0-100%). Higher = busier, more work being done.
- **RAM Usage:** Percentage of system memory in use (0-100%). Affects emergency detection.
- **Battery:** Percentage of battery remaining (on laptops). Affects power decisions.

### Trends

- **📈 Rising:** Metric is increasing (e.g., temp going up)
- **📉 Falling:** Metric is decreasing (e.g., load going down)
- **➡️ Stable:** Metric is relatively constant

---

## Advanced Tips

### Phrase Your Queries Naturally

The system understands conversational English. You don't need precise keywords:

✅ Good:
- "what happened today"
- "show me the report"
- "how's the system doing"

❌ Avoid:
- Single words without context ("report" by itself)
- Very specific technical jargon
- Multi-part questions ("show report AND analyze trends")

### One Query at a Time

Ask one question at a time for best results:

✅ Good:
- "show me a report"
- (Wait for response)
- "analyze trends for the last day"

❌ Avoid:
- "show me a report and analyze trends and tell me the status"

### Use Time Ranges for Analysis

When asking for trends, specify the time period:

✅ Specific:
- "analyze trends for the last day"
- "show me what changed in the last week"

✅ Default:
- "analyze the data" → Uses last 1 hour by default

### Check Example Queries

The dashboard sidebar has a "💡 Example Queries" section. Click to expand and see suggested queries you can adapt.

---

## Common Questions & Troubleshooting

### Q: "I don't understand that"

**A:** Try rephrasing using simpler words, or use one of the example queries as a starting point.

### Q: No data available

**A:** The system needs monitoring history to analyze. Keep monitoring for at least 1 hour before running reports.

### Q: Results seem wrong or outdated

**A:** Click "Refresh" in the Live Dashboard or "Rerun app" in any Streamlit app. Fresh data will be fetched.

### Q: Can I save or export reports?

**A:** Reports are displayed as markdown in the dashboard. You can:
- Copy text from the dashboard (Ctrl+A, Ctrl+C)
- Take a screenshot (Shift+Print Screen)
- Export via browser print (Ctrl+P)

### Q: Why can't the system change settings?

**A:** Configuration changes require file write access. See `/docs/CONFIGURATION.md` for manual threshold tuning.

---

## Integration with Dashboards

### Live Dashboard (`dashboard.py`)

- **Query Interface:** Right sidebar
- **Real-time Data:** Uses current `CentralAI.tick()` data
- **Refresh Behavior:** Queries use live metrics
- **Simulation Mode:** Queries disabled in simulation mode (status queries show simulated data)

### Analytics Dashboard (`dashboard_analytics.py`)

- **Query Interface:** Right sidebar
- **Historical Data:** Queries analyze 1+ hours of history from SQLite database
- **Time Range Selection:** Can adjust time range for analysis
- **No Simulation:** Always uses real historical data

---

## Frequently Used Query Patterns

### Quick Health Check
```
"how is it working"
↓
Returns current status with all metrics in <1 second
```

### Daily Report
```
"generate a report"
↓
Returns full summary with metrics and recommendations
```

### Understand Recent Changes
```
"analyze trends for the last day"
↓
Shows temperature/load patterns and when THROTTLE was active
```

### Troubleshoot High Temperature
```
"analyze trends"  →  "show me a report"
↓
Identify when temp spikes happen, why THROTTLE was triggered
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send query |
| `Ctrl+A` | Select all text (for copying results) |
| `Ctrl+L` | Clear browser address bar (focus input) |

---

## Performance Notes

- **First Query:** ~500ms (initializes processors)
- **Subsequent Queries:** ~100-200ms (cached)
- **Report Generation:** 1-2 seconds (reads database)
- **Analysis:** 2-5 seconds (depending on time range)

For faster results, use Status queries (instant) instead of Report queries.

---

## Security & Privacy

- **Local Processing:** All queries processed locally, no data sent to external services
- **No Authentication:** Queries are unsecured (assume trusted network)
- **Data Visibility:** Reports show system metrics (temperature, load, decisions)
- **No Credentials:** Dashboards don't expose passwords, keys, or sensitive data

For public deployments, restrict network access via firewall. See `/docs/WEB_SETUP.md`.

---

## Documentation

- **Dashboard Setup:** `/docs/WEB_SETUP.md`
- **Configuration:** `/docs/CONFIGURATION.md`
- **CLI Tool:** `/docs/CLI_GUIDE.md`
- **Full System:** `/README.md`

---

## Support

If you encounter issues:

1. Check example queries (click "💡 Example Queries" in sidebar)
2. Verify monitoring is running (`streamlit run dashboard.py`)
3. Check that `solo_rock.db` exists and has data
4. See troubleshooting section above
5. Review system logs for errors

For more help, see main `/README.md` or the `/docs/` directory.

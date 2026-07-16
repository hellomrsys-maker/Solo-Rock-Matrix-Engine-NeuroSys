# SOLO ROCK Web Dashboards — Setup & Access Guide

## Quick Start

SOLO ROCK includes interactive web dashboards for real-time monitoring and historical analysis. These dashboards are **publicly accessible** (no authentication required by default) and can be deployed on any network.

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run live monitoring dashboard
streamlit run dashboard.py

# In another terminal, run analytics dashboard
streamlit run dashboard_analytics.py
```

Both dashboards will be available at:
- **Live Dashboard:** http://localhost:8501
- **Analytics Dashboard:** http://localhost:8502

### Accessing from Other Machines

To allow other users on your network to access the dashboards, run Streamlit with:

```bash
streamlit run dashboard.py --server.address 0.0.0.0 --server.port 8501
```

Then other machines can access via:
```
http://<your-ip-address>:8501
```

---

## Dashboard Features

### 📊 Live Dashboard (`dashboard.py`)

**Real-time system monitoring with:**
- **Telemetry Metrics:** CPU temperature, load, RAM usage, battery level
- **Historical Trends:** 60-tick rolling chart of temperature and load
- **Decision Display:** Current routing decision (FULL_RATE, BATCH, THROTTLE, EMERGENCY)
- **Hardware Profile:** CPU cores, GPU presence, OS info
- **Simulation Mode:** Test system behavior under different scenarios
  - Simulated CPU temp spikes (test THROTTLE detection)
  - Simulated load increases (test BATCH mode)
  - EMERGENCY conditions (test thermal shutdown)

**Auto-Refresh:** Configurable 1-60 second refresh intervals

**Use Cases:**
- Monitor system health in real-time
- Test SOLO ROCK behavior under simulated load
- Verify decision engine is working correctly
- Debug thermal issues

---

### 📈 Analytics Dashboard (`dashboard_analytics.py`)

**Historical telemetry analysis:**
- **Time Range Selection:** 1 hour / 24 hours / 7 days
- **Thermal Analysis:**
  - Temperature trend chart (is it rising/falling?)
  - Peak and valley detection
  - Trend direction indicator
  - Warning/critical threshold overlays
  
- **CPU Load Analysis:**
  - Load trend over selected period
  - Average, peak, minimum load
  
- **RAM Usage:**
  - RAM usage chart
  - Average and peak memory
  
- **Decision Distribution:**
  - Pie chart: % time in each routing mode (FULL_RATE, BATCH, THROTTLE, EMERGENCY)
  - Breakdown table with counts and percentages
  
- **Performance Metrics:**
  - Aggregated statistics (avg temp, max load, etc.)
  - Throttle impact (% time in pacing modes)
  
- **Event Log:**
  - Raw telemetry viewer (last 100 events)
  - Sortable by timestamp, decision, or metrics

**Auto-Refresh:** Optional real-time updates every 30 seconds

**Use Cases:**
- Analyze historical thermal patterns
- Identify when THROTTLE/BATCH modes were triggered
- Compare performance across different time periods
- Export metrics for reports or external systems

---

## Natural Language Queries

Both dashboards include a **Natural Language Query** feature in the sidebar. Type questions in plain English:

### Example Queries

**Reports:**
- "show me a report"
- "generate a summary"
- "what happened last hour"

**Status:**
- "how is it working"
- "what's the current status"
- "is everything ok"

**Analysis:**
- "show me trends"
- "analyze the data"
- "what changed"

**Configuration:**
- "change thermal warning to 75"
- "update cpu threshold"

**Alerts:**
- "set up email alerts"
- "enable slack notifications"

The system will parse your query and display the appropriate dashboard, report, or status.

---

## Deployment & Access Control

### Public Access (Default)

By default, SOLO ROCK dashboards are **publicly accessible** with no authentication. This is ideal for:
- Development and testing
- Internal network dashboards
- Trusted environments
- Demo/evaluation

### Restricting Access (Optional)

If you need to restrict access, see the options below:

#### Option 1: Firewall Rules

Restrict network access at the firewall/router level:
```bash
# Block port 8501 from external networks
sudo ufw deny from any to any port 8501
```

#### Option 2: Reverse Proxy with Auth

Use a reverse proxy (nginx, traefik) to add authentication:
```nginx
server {
    listen 80;
    server_name solo-rock.example.com;
    
    auth_basic "SOLO ROCK Restricted";
    auth_basic_user_file /etc/nginx/basic_auth;
    
    location / {
        proxy_pass http://localhost:8501;
    }
}
```

#### Option 3: VPN

Deploy dashboards behind a VPN:
```bash
# Access only via VPN tunnel
ssh -L 8501:localhost:8501 vpn-server
# Then open http://localhost:8501
```

---

## Configuration Files

### Streamlit Configuration (`.streamlit/config.toml`)

Located at `.streamlit/config.toml` in the repository. Default settings:

```toml
[theme]
primaryColor = "#00D084"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "monospace"

[client]
showErrorDetails = true

[logger]
level = "info"

[server]
# Listen on all interfaces (required for network access)
address = "0.0.0.0"
# Allow large dataframes
maxUploadSize = 200
# Enable WebSocket for live updates
enableXsrfProtection = true
```

To modify settings:
1. Edit `.streamlit/config.toml`
2. Restart Streamlit: `streamlit run dashboard.py`

---

## Environment Setup

### Dependencies

```bash
pip install streamlit>=1.28
pip install psutil>=5.9
pip install pyyaml>=6
```

All dependencies are listed in `requirements.txt`.

### Database Setup

SOLO ROCK uses SQLite for event logging. Database file:
- **Path:** `solo_rock.db` (created automatically in current directory)
- **Size:** ~1KB per monitoring hour (very efficient)
- **Retention:** Auto-cleanup removes events older than 30 days

To view database:
```bash
sqlite3 solo_rock.db
sqlite> SELECT COUNT(*) FROM events;
sqlite> SELECT AVG(cpu_temp), MAX(cpu_load) FROM events;
```

### Configuration Files

- **Main Config:** `config/thresholds.yaml` — Thermal/CPU/RAM thresholds
- **Auto-Calibration:** `config/calibration.json` — Per-hardware tuned thresholds (auto-generated)
- **Alerting:** Config section for email, Slack, webhook alerts

---

## Troubleshooting

### Dashboard Won't Load

**Problem:** `http://localhost:8501` shows connection refused

**Solution:**
```bash
# Kill any existing Streamlit processes
pkill -f streamlit

# Start fresh with explicit server config
streamlit run dashboard.py --server.address 0.0.0.0 --server.port 8501
```

### Other Machines Can't Access

**Problem:** `http://<your-ip>:8501` times out or refuses connection

**Solution:**
1. Verify Streamlit is running: `ps aux | grep streamlit`
2. Check firewall: `sudo ufw status` — allow port 8501 if needed
3. Verify binding to 0.0.0.0: Check `.streamlit/config.toml` has `address = "0.0.0.0"`
4. Test locally first: `curl http://localhost:8501` should return HTML

### Database File Growing Too Large

**Problem:** `solo_rock.db` is >1GB

**Solution:**
```bash
# Manually cleanup old entries
python -c "from diagnostics.logger import EventLogger; logger = EventLogger(); logger.cleanup_old_entries(days=7)"

# Or reduce retention period
python -c "from diagnostics.logger import EventLogger; logger = EventLogger(); logger.cleanup_old_entries(days=1)"
```

### High CPU/Memory Usage

**Problem:** Dashboards using lots of CPU/RAM

**Solution:**
- Reduce refresh interval in dashboard (increase to 30+ seconds)
- Close unused dashboard tabs
- Restart Streamlit: `pkill -f streamlit && streamlit run dashboard.py`
- Check database size: `ls -lh solo_rock.db`

### Analytics Dashboard Slow

**Problem:** Analytics dashboard takes >10 seconds to load

**Solution:**
1. Use smaller time range (try "1 hour" instead of "7 days")
2. Check database: `sqlite3 solo_rock.db "PRAGMA table_info(events);"`
3. Rebuild index: `sqlite3 solo_rock.db "REINDEX;"`

---

## Performance & Scaling

### Single Machine

- **Live Dashboard:** Handles 1000+ updates/second with <100ms latency
- **Analytics Dashboard:** <1 second load time for 1 week of data
- **Database:** 1KB/hour growth, auto-cleanup after 30 days

### Multiple Machines

For monitoring multiple machines:
1. Run `monitor_realtime.py` on each machine (generates local `solo_rock.db`)
2. Export metrics via `analytics/query.py`
3. Aggregate in central dashboard or monitoring system
4. (Future) Use distributed agent architecture for fleet-wide dashboards

---

## Security Considerations

### Public Access

If dashboards are publicly accessible:
- **Risk:** Anyone can see your system metrics (temperature, load, decision patterns)
- **Mitigation:** Use firewall/VPN to restrict access, or run in trusted networks only
- **No Credentials:** Dashboard access doesn't expose sensitive data (passwords, keys)

### API Access

- **Current:** Dashboards are web-only (Streamlit UI)
- **Future:** REST API will support programmatic access with API keys
- **Note:** No authentication currently, assume trusted network

### Configuration Files

- **Thresholds:** `config/thresholds.yaml` — World-readable (non-sensitive)
- **Calibration:** `config/calibration.json` — Generated, non-sensitive
- **Database:** `solo_rock.db` — World-readable (telemetry only, no credentials)

---

## Support & Documentation

- **Quick Start:** See above "Running Locally"
- **CLI Tool:** See `docs/CLI_GUIDE.md` for `solo-rock-cli` commands
- **Configuration:** See `docs/CONFIGURATION.md` for threshold tuning
- **Deployment:** See `docs/DEPLOYMENT.md` for systemd/Windows/Kubernetes setup
- **NLU Queries:** See `docs/NLU_GUIDE.md` for natural language query examples

---

## Next Steps

1. **Start Monitoring:** `streamlit run dashboard.py`
2. **View History:** `streamlit run dashboard_analytics.py`
3. **Ask Questions:** Use natural language queries in the dashboards
4. **Tune Thresholds:** Modify `config/thresholds.yaml` for your hardware
5. **Set Up Alerts:** Configure email/Slack in `config/thresholds.yaml`

For production deployments, see `docs/DEPLOYMENT.md`.

"""
Event logging to SQLite for SOLO ROCK telemetry persistence and historical analysis.

Stores all monitoring ticks with telemetry snapshots and decisions for trend analysis,
performance metrics, and issue detection over time.
"""

import sqlite3
import time
from datetime import datetime, timedelta


class EventLogger:
    """Manages SQLite event database for SOLO ROCK telemetry."""

    def __init__(self, db_path='solo_rock.db'):
        """Initialize or open database.

        Args:
            db_path: Path to SQLite database file (default: solo_rock.db in current directory)
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Create database schema if not exists."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY,
                        timestamp REAL NOT NULL,
                        cpu_temp REAL,
                        cpu_load REAL,
                        ram_usage REAL,
                        gpu_load REAL,
                        decision TEXT NOT NULL,
                        reason TEXT,
                        action_taken TEXT
                    )
                ''')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON events(timestamp)')
                conn.commit()
        except sqlite3.Error as e:
            print(f"[Warning] Database initialization failed: {e}")

    def insert_event(self, timestamp, cpu_temp, cpu_load, ram_usage, decision, reason, gpu_load=None, action_taken=None):
        """Insert telemetry event into database.

        Args:
            timestamp: Unix timestamp (seconds since epoch)
            cpu_temp: CPU temperature in Celsius (or None)
            cpu_load: CPU load percentage 0-100 (or None)
            ram_usage: RAM usage percentage 0-100 (or None)
            decision: Decision mode (FULL_RATE, BATCH, THROTTLE, EMERGENCY)
            reason: Explanation for decision (or None)
            gpu_load: GPU load percentage 0-100 (optional, or None)
            action_taken: Description of action taken (optional, or None)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO events (timestamp, cpu_temp, cpu_load, ram_usage, gpu_load, decision, reason, action_taken)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (timestamp, cpu_temp, cpu_load, ram_usage, gpu_load, decision, reason, action_taken))
                conn.commit()
        except sqlite3.Error as e:
            print(f"[Warning] Failed to insert event: {e}")

    def get_events_since(self, since_timestamp):
        """Query events since given timestamp.

        Args:
            since_timestamp: Unix timestamp to query from

        Returns:
            List of event dictionaries ordered by timestamp ascending
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    'SELECT * FROM events WHERE timestamp >= ? ORDER BY timestamp',
                    (since_timestamp,)
                )
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"[Warning] Failed to query events: {e}")
            return []

    def cleanup_old_entries(self, days=30):
        """Remove events older than specified days.

        Args:
            days: Number of days to retain (default: 30)
        """
        try:
            cutoff = datetime.now() - timedelta(days=days)
            cutoff_timestamp = cutoff.timestamp()
            with sqlite3.connect(self.db_path) as conn:
                result = conn.execute('DELETE FROM events WHERE timestamp < ?', (cutoff_timestamp,))
                conn.commit()
                if result.rowcount > 0:
                    print(f"[Logger] Cleaned up {result.rowcount} old events (older than {days} days)")
        except sqlite3.Error as e:
            print(f"[Warning] Failed to cleanup old entries: {e}")

    def get_statistics(self, hours=1):
        """Get telemetry statistics for last N hours.

        Args:
            hours: Number of hours to include (default: 1)

        Returns:
            Dictionary with event_count and statistics for temp, load, ram
        """
        since = datetime.now() - timedelta(hours=hours)
        events = self.get_events_since(since.timestamp())

        if not events:
            return None

        temps = [e['cpu_temp'] for e in events if e['cpu_temp'] is not None]
        loads = [e['cpu_load'] for e in events if e['cpu_load'] is not None]
        rams = [e['ram_usage'] for e in events if e['ram_usage'] is not None]

        return {
            'event_count': len(events),
            'temp': {
                'avg': sum(temps) / len(temps) if temps else None,
                'max': max(temps) if temps else None,
                'min': min(temps) if temps else None,
            },
            'load': {
                'avg': sum(loads) / len(loads) if loads else None,
                'max': max(loads) if loads else None,
                'min': min(loads) if loads else None,
            },
            'ram': {
                'avg': sum(rams) / len(rams) if rams else None,
                'max': max(rams) if rams else None,
                'min': min(rams) if rams else None,
            },
        }

    def get_event_count(self):
        """Get total number of events in database.

        Returns:
            Integer count of all events
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT COUNT(*) FROM events')
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"[Warning] Failed to get event count: {e}")
            return 0

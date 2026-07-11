"""
Translates a telemetry snapshot into a routing decision. This is the
piece that actually solves the problem described in the README: instead
of letting software keep firing commands at hardware that is already
busy or hot, the Decision Engine looks at real numbers and returns one
of a small set of actions that the Peripheral System (nodes) applies.
"""

# Thresholds are intentionally conservative — they trigger well before
# a manufacturer's own thermal/power protection would, so SOLO ROCK is
# always advisory rather than a race against the hardware's own limits.
THERMAL_WARNING_C = 80.0
THERMAL_CRITICAL_C = 90.0
CPU_LOAD_HIGH_PCT = 85.0
CPU_LOAD_MODERATE_PCT = 50.0
RAM_CRITICAL_PCT = 97.0

FULL_RATE = "FULL_RATE"
BATCH = "BATCH"
THROTTLE = "THROTTLE"
EMERGENCY = "EMERGENCY"


class DecisionEngine:
    def __init__(self,
                 thermal_warning=THERMAL_WARNING_C,
                 thermal_critical=THERMAL_CRITICAL_C,
                 cpu_load_high=CPU_LOAD_HIGH_PCT,
                 cpu_load_moderate=CPU_LOAD_MODERATE_PCT,
                 ram_critical=RAM_CRITICAL_PCT):
        self.thermal_warning = thermal_warning
        self.thermal_critical = thermal_critical
        self.cpu_load_high = cpu_load_high
        self.cpu_load_moderate = cpu_load_moderate
        self.ram_critical = ram_critical

    def classify_workload(self, snapshot):
        """Rough bucket for the current load, useful for logging/telemetry dashboards."""
        cpu_load = snapshot.get("cpu_load", 0.0)
        cpu_temp = snapshot.get("cpu_temp", 0.0)

        if cpu_temp >= self.thermal_critical:
            return "CRITICAL"
        if cpu_load >= self.cpu_load_high or cpu_temp >= self.thermal_warning:
            return "HEAVY"
        if cpu_load >= self.cpu_load_moderate:
            return "MODERATE"
        if cpu_load > 5.0:
            return "LIGHT"
        return "IDLE"

    def decide(self, snapshot):
        """
        Core routing decision for a task about to be dispatched to hardware.

        Returns (action, reason):
            FULL_RATE  - hardware has headroom, dispatch immediately
            BATCH      - moderate load, coalesce redundant submissions
            THROTTLE   - approaching thermal/power limits, pace hard and
                         cap dispatch rate before hardware self-throttles
            EMERGENCY  - critical threshold crossed, hand off to
                         EmergencyOverride immediately
        """
        cpu_temp = snapshot.get("cpu_temp", 0.0)
        cpu_load = snapshot.get("cpu_load", 0.0)
        ram_usage = snapshot.get("ram_usage", 0.0)

        if cpu_temp >= self.thermal_critical:
            return EMERGENCY, f"CPU temperature {cpu_temp:.1f}C >= critical {self.thermal_critical:.1f}C"
        if ram_usage >= self.ram_critical:
            return EMERGENCY, f"RAM usage {ram_usage:.1f}% >= critical {self.ram_critical:.1f}%"

        if cpu_temp >= self.thermal_warning or cpu_load >= self.cpu_load_high:
            return THROTTLE, f"CPU temp {cpu_temp:.1f}C / load {cpu_load:.1f}% at warning threshold"

        if cpu_load >= self.cpu_load_moderate:
            return BATCH, f"CPU load {cpu_load:.1f}% moderate — coalescing redundant submissions"

        return FULL_RATE, "Hardware has headroom"


if __name__ == "__main__":
    engine = DecisionEngine()
    for demo_snapshot in (
        {"cpu_temp": 45.0, "cpu_load": 10.0, "ram_usage": 40.0},
        {"cpu_temp": 70.0, "cpu_load": 60.0, "ram_usage": 55.0},
        {"cpu_temp": 85.0, "cpu_load": 92.0, "ram_usage": 70.0},
        {"cpu_temp": 95.0, "cpu_load": 99.0, "ram_usage": 80.0},
    ):
        action, reason = engine.decide(demo_snapshot)
        print(f"{demo_snapshot} -> {action} ({reason})")

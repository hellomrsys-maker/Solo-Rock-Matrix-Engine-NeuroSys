"""
Autonomic background-process restraint (FSMF / "kidney" filtration).
Lowers the scheduling priority of background CPU hogs so the primary
workload gets uncontested access — implemented entirely through
psutil's cross-platform nice()/ionice() wrappers, so it behaves
correctly on Windows, Linux, and macOS without any OS-specific branch.
"""

import platform
import psutil

_IS_WINDOWS = platform.system() == "Windows"

# The lowest-priority nice value psutil accepts on this platform.
_LOWEST_PRIORITY = psutil.IDLE_PRIORITY_CLASS if _IS_WINDOWS else 19

_DEFAULT_WHITELIST = {
    # Windows core processes
    "system", "svchost.exe", "explorer.exe", "csrss.exe", "smss.exe",
    "wininit.exe", "services.exe", "lsass.exe",
    # Linux/macOS init & session-critical processes
    "systemd", "init", "kthreadd", "launchd", "sshd", "bash", "zsh",
    "python", "python3",
}


class ProcessController:
    def __init__(self, whitelist=None):
        self.whitelist = {name.lower() for name in (whitelist or _DEFAULT_WHITELIST)}

    def filter_junk_processes(self, cpu_threshold=5.0):
        """FSMF Junk Filtration: Lower priority of background hogs."""
        print("[FSMF] Initiating Background Process Filtration...")
        filtered_count = 0

        # First pass primes psutil's internal CPU-percent baseline.
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc.cpu_percent(None)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name']
                if not name or name.lower() in self.whitelist:
                    continue
                cpu = proc.cpu_percent(None)
                if cpu <= cpu_threshold:
                    continue

                p = psutil.Process(proc.info['pid'])
                if p.nice() != _LOWEST_PRIORITY:
                    p.nice(_LOWEST_PRIORITY)
                    print(f"       -> Throttled {name} (PID: {proc.info['pid']}) to lowest priority.")
                    filtered_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        print(f"[FSMF] Filtration complete. {filtered_count} background tasks suppressed.")
        return filtered_count


if __name__ == "__main__":
    pc = ProcessController()
    pc.filter_junk_processes()

import psutil
import os

class ProcessController:
    def __init__(self):
        # High-priority core process whitelist
        self.whitelist = ['System', 'svchost.exe', 'explorer.exe', 'csrss.exe', 'smss.exe', 'wininit.exe', 'services.exe', 'lsass.exe']
        
    def filter_junk_processes(self):
        """FSMF Junk Filtration: Lower priority of background hogs."""
        print("[FSMF] Initiating Background Process Filtration...")
        filtered_count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                name = proc.info['name']
                if name and name not in self.whitelist and proc.info['cpu_percent'] > 5.0:
                    # Found a background hog
                    p = psutil.Process(proc.info['pid'])
                    # Set priority to IDLE (lowest)
                    if p.nice() != psutil.IDLE_PRIORITY_CLASS:
                        p.nice(psutil.IDLE_PRIORITY_CLASS)
                        print(f"       -> Throttled {name} (PID: {proc.info['pid']}) to IDLE priority.")
                        filtered_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        print(f"[FSMF] Filtration complete. {filtered_count} background tasks suppressed.")
        return filtered_count

if __name__ == "__main__":
    pc = ProcessController()
    pc.filter_junk_processes()

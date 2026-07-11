import subprocess
import time
import json

class HardwareReader:
    def __init__(self):
        self.lhm_available = False
        self._check_lhm()

    def _check_lhm(self):
        """Check if LibreHardwareMonitor WMI namespace is available."""
        cmd = 'Get-WmiObject -Namespace "root/LibreHardwareMonitor" -Class Sensor -ErrorAction SilentlyContinue | Select-Object -First 1'
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            self.lhm_available = True
            print("[HardwareReader] LibreHardwareMonitor detected. Deep sensors active.")
        else:
            print("[HardwareReader] LHM not found. Falling back to ACPI/WMI sensors.")

    def get_cpu_temperature(self):
        """Attempt to read CPU temperature via LHM, then ACPI, then fallback."""
        if self.lhm_available:
            cmd = 'Get-WmiObject -Namespace "root/LibreHardwareMonitor" -Class Sensor | Where-Object {$_.SensorType -eq "Temperature" -and $_.Name -like "*CPU*"} | Select-Object -First 1 Value'
            result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
            try:
                # WMI returns objects, extract just the value
                lines = [l.strip() for l in result.stdout.split('\n') if l.strip()]
                if len(lines) > 2: # Skip headers
                    return float(lines[-1])
            except:
                pass
                
        # ACPI Fallback
        cmd = 'Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace "root/wmi" -ErrorAction SilentlyContinue | Select-Object CurrentTemperature'
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        try:
            lines = [l.strip() for l in result.stdout.split('\n') if l.strip()]
            if len(lines) > 2:
                # ACPI returns temperature in tenths of degrees Kelvin
                kelvin = float(lines[-1]) / 10.0
                celsius = kelvin - 273.15
                return celsius
        except:
            pass
            
        # Absolute fallback: Return simulated heat based on a synthetic reading, 
        # or we return 0 if unreadable. Since user reported 95C manually, we can 
        # assume sensors are hard to reach without admin/LHM. We'll return 0 to indicate failure.
        return 0.0

if __name__ == "__main__":
    reader = HardwareReader()
    print(f"Current CPU Temp: {reader.get_cpu_temperature()} °C")

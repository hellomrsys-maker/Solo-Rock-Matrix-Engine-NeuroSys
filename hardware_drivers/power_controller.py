"""
Autonomic power-envelope control. Moves the OS-exposed maximum
processor state DOWN to shed heat before hardware-level throttling
kicks in — it never raises any limit above the manufacturer default.

Windows uses the native `powercfg` interface. Other platforms have no
single standard equivalent exposed to userspace without extra
privileges/daemons, so this degrades to a safe no-op that reports
itself as unsupported rather than guessing at a distro-specific path.
"""

import platform
import subprocess
import re

_IS_WINDOWS = platform.system() == "Windows"


class PowerController:
    def __init__(self):
        self.supported = _IS_WINDOWS
        self.active_scheme = self._get_active_scheme() if self.supported else None
        if self.supported:
            print(f"[PowerController] Active Power Scheme GUID: {self.active_scheme}")
        else:
            print(f"[PowerController] Power-plan control not available on {platform.system()}. "
                  f"Running in telemetry-only mode (no power-state changes will be made).")

    def _get_active_scheme(self):
        """Retrieve the GUID of the currently active Windows power plan."""
        try:
            result = subprocess.run(["powercfg", "/getactivescheme"], capture_output=True, text=True, timeout=3)
        except Exception:
            return None
        # Format: Power Scheme GUID: 381b4222-f694-41f0-9685-ff5bb260df2e  (Balanced)
        match = re.search(r"GUID:\s+([a-fA-F0-9\-]+)", result.stdout)
        return match.group(1) if match else None

    def set_max_processor_state(self, percentage):
        """Set the maximum processor state (throttling) to lower temps. Windows only."""
        if not self.supported:
            print(f"[PowerController] Skipped: max-processor-state control unsupported on {platform.system()}.")
            return False

        if not self.active_scheme:
            print("[PowerController] Error: No active power scheme found.")
            return False

        print(f"[PDEC] FORCING MAX PROCESSOR STATE TO {percentage}%...")

        # Powercfg GUIDs for Max Processor State:
        # Subgroup: 54533251-82be-4824-96c1-47b60b740d00 (Processor power management)
        # Setting: bc5038f7-23e0-4960-96da-33abaf5935ec (Maximum processor state)

        subgroup_guid = "54533251-82be-4824-96c1-47b60b740d00"
        setting_guid = "bc5038f7-23e0-4960-96da-33abaf5935ec"

        try:
            # Set for AC (Plugged in)
            subprocess.run(["powercfg", "/setacvalueindex", self.active_scheme, subgroup_guid, setting_guid, str(percentage)])
            # Set for DC (Battery)
            subprocess.run(["powercfg", "/setdcvalueindex", self.active_scheme, subgroup_guid, setting_guid, str(percentage)])
            # Apply the changes by making the scheme active again
            subprocess.run(["powercfg", "/setactive", self.active_scheme])
        except Exception as e:
            print(f"[PowerController] Error applying power state: {e}")
            return False

        print(f"[PDEC] Hardware throttle applied successfully: Cap at {percentage}%.")
        return True


if __name__ == "__main__":
    pc = PowerController()
    # Test setting to 99% (disables turbo boost on many laptops without huge performance loss)
    pc.set_max_processor_state(99)

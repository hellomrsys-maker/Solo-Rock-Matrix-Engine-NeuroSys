import ctypes
import time
import subprocess
import os

# Define necessary Windows API functions
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Get Screen Dimensions
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

def set_hardware_brightness(level=100):
    print(f"[PDEC] Adjusting hardware backlight brightness to {level}%...")
    # Use WMI via PowerShell to directly set the hardware brightness level
    ps_command = f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {level})'
    subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
    print("[PDEC] Brightness locked.")

def check_and_stimulate_pixels():
    print(f"[PPVO] Intercepting Desktop Graphics Device Context (HDC)...")
    # Get the Device Context for the entire screen (0 = Desktop)
    hdc = user32.GetDC(0)
    
    if not hdc:
        print("[PPVO] Failed to intercept HDC.")
        return

    print(f"[PPVO] Direct pixel access granted. Resolution: {screen_width}x{screen_height}")
    print("[PPVO] Stimulating pixels to verify active state...")

    # Define RGB macro
    def RGB(r, g, b):
        return r | (g << 8) | (b << 16)

    # We will draw a raw visual sweep directly into the frame buffer
    # This bypasses all UI frameworks, talking directly to the Windows Graphics Device Interface
    
    colors = [
        RGB(255, 0, 0),   # Red check
        RGB(0, 255, 0),   # Green check
        RGB(0, 0, 255),   # Blue check
        RGB(255, 255, 255) # White check
    ]

    try:
        # We can't safely SetPixel 2 million times in Python (it's too slow and would freeze),
        # so we will draw thick lines/rectangles sweeping down the screen to test the pixels.
        for color in colors:
            # Create a solid brush of the color
            hbrush = gdi32.CreateSolidBrush(color)
            
            # Sweep down the screen in chunks
            for y in range(0, screen_height, 100):
                # Define a RECT structure
                class RECT(ctypes.Structure):
                    _fields_ = [("left", ctypes.c_long),
                                ("top", ctypes.c_long),
                                ("right", ctypes.c_long),
                                ("bottom", ctypes.c_long)]
                
                rect = RECT(0, y, screen_width, y + 100)
                user32.FillRect(hdc, ctypes.byref(rect), hbrush)
                time.sleep(0.01) # Small delay to see the sweep
            
            gdi32.DeleteObject(hbrush)
            time.sleep(0.2)
            
    finally:
        # Release the DC so Windows can take it back
        user32.ReleaseDC(0, hdc)
        print("[PPVO] Pixel stimulation complete. Releasing HDC back to Windows.")

if __name__ == "__main__":
    print("==================================================")
    print("  ABSOLUTE PIXEL & BRIGHTNESS CONTROL OVERRIDE    ")
    print("==================================================")
    
    # 1. Take control of the hardware backlight
    set_hardware_brightness(100)
    
    # 2. Check and stimulate pixels directly via GDI
    check_and_stimulate_pixels()
    
    # 3. Reset brightness back to normal (e.g., 70%) after test
    print("\n[PDEC] Resetting brightness to 75% for comfort...")
    set_hardware_brightness(75)
    
    print("==================================================")
    print("  OVERRIDE COMPLETE.                              ")
    print("==================================================")

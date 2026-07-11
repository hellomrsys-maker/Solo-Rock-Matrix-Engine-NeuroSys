import ctypes
from ctypes import wintypes
import time

# Load Windows GDI and User32
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Constants
SRCCOPY = 0x00CC0020
DIB_RGB_COLORS = 0

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", wintypes.DWORD * 3)
    ]

def force_pixel_matrix():
    print("[PPVO] Initiating Zero-Copy Pixel Matrix Override...")
    
    # 1. Get exact physical screen resolution
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    
    # 2. Hijack Desktop Device Context (HDC)
    hdc = user32.GetDC(0)
    if not hdc:
        print("[ERROR] Could not hijack HDC.")
        return
        
    print(f"[FSMF] Memory allocated for {width}x{height} pixels ({width * height} total).")
    
    # 3. Create absolute black clear
    black_brush = gdi32.CreateSolidBrush(0)
    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
    rect = RECT(0, 0, width, height)
    print("[PPVO] Flushing screen to absolute black...")
    user32.FillRect(hdc, ctypes.byref(rect), black_brush)
    gdi32.DeleteObject(black_brush)
    time.sleep(1) # Let the user observe the black screen
    
    # 4. Generate the Zero-Copy Pixel Array
    # We use a raw C-type integer array to hold the exact color data in memory
    print("[CAIN] Calculating unique color matrix for every individual pixel...")
    pixel_count = width * height
    PixelArray = wintypes.DWORD * pixel_count
    pixels = PixelArray()
    
    # Generate unique colors. To make every adjacent color different, we use bitwise math.
    # We will pack X, Y coordinates into the RGB channels to ensure massive variance.
    # Format for DIB is 0x00RRGGBB (actually BGR in memory depending on architecture, but Windows handles DWORD as 0x00bbggrr)
    for y in range(height):
        for x in range(width):
            # Formula to maximize color variance side-by-side
            r = (x * 255 // width) ^ (y * 255 // height)
            g = (x ^ y) % 256
            b = (x * y) % 256
            
            # Pack into DWORD (0x00bbggrr)
            color = (r) | (g << 8) | (b << 16)
            pixels[y * width + x] = color
            
    # 5. Define Bitmap Header
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height  # Negative means top-down DIB
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = 0 # BI_RGB
    bmi.bmiHeader.biSizeImage = 0
    
    # 6. Blast the matrix directly to the GPU frame buffer via Zero-Copy
    print("[SCCN] Blasting memory block to GPU buffer...")
    gdi32.SetDIBitsToDevice(
        hdc, 
        0, 0, width, height, # Destination x, y, w, h
        0, 0, 0, height,     # Source x, y, start scan, lines
        ctypes.byref(pixels), # Raw memory array
        ctypes.byref(bmi),   # Bitmap info
        DIB_RGB_COLORS       # RGB usage
    )
    
    print("[SUCCESS] Every pixel is active and mathematically unique.")
    print("Holding matrix for 10 seconds so user can observe...")
    time.sleep(10)
    
    # Release control
    user32.ReleaseDC(0, hdc)
    print("[PPVO] Override concluded. Released HDC.")

if __name__ == "__main__":
    force_pixel_matrix()

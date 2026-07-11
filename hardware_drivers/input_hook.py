import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from infrastructure.amsv import amsv_block

class PhysicalInputHook:
    def __init__(self):
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # Keycode mapping for bitmask
        self.key_map = {
            'w': 1 << 0,
            'a': 1 << 1,
            's': 1 << 2,
            'd': 1 << 3,
            'space': 1 << 4,
            'shift': 1 << 5,
        }
        
    def on_click(self, x, y, button, pressed):
        """Intercept physical mouse click and write directly to AMSV C-Memory."""
        if pressed:
            amsv_block.coord_x = float(x)
            amsv_block.coord_y = float(y)
            # Bit 0 for left click, Bit 1 for right click
            if str(button) == "Button.left":
                amsv_block.mouse_state |= (1 << 0)
            elif str(button) == "Button.right":
                amsv_block.mouse_state |= (1 << 1)
        else:
            if str(button) == "Button.left":
                amsv_block.mouse_state &= ~(1 << 0)
            elif str(button) == "Button.right":
                amsv_block.mouse_state &= ~(1 << 1)

    def on_press(self, key):
        try:
            k = key.char.lower()
        except AttributeError:
            if key == key.space: k = 'space'
            elif key == key.shift: k = 'shift'
            else: return
            
        if k in self.key_map:
            # Set the specific bit in the 32-bit integer
            amsv_block.keyboard_state |= self.key_map[k]

    def on_release(self, key):
        try:
            k = key.char.lower()
        except AttributeError:
            if key == key.space: k = 'space'
            elif key == key.shift: k = 'shift'
            else: return
            
        if k in self.key_map:
            # Clear the specific bit in the 32-bit integer
            amsv_block.keyboard_state &= ~self.key_map[k]

    def start_listening(self):
        """Starts the physical hardware hook in a background thread."""
        try:
            from pynput import mouse, keyboard
            self.mouse_listener = mouse.Listener(on_click=self.on_click)
            self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            
            self.mouse_listener.start()
            self.keyboard_listener.start()
            print("[InputHook] Real-time Keyboard & Mouse intercept ACTIVE.")
        except ImportError:
            print("[InputHook] ERROR: pynput not installed.")
            
    def stop_listening(self):
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

if __name__ == "__main__":
    hook = PhysicalInputHook()
    hook.start_listening()
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        hook.stop_listening()

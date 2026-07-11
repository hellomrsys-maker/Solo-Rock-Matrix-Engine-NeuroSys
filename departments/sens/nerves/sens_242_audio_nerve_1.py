import threading
import time
import ctypes
import os
import sys

from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

SND_ASYNC = 0x0001
SND_FILENAME = 0x00020000

class SENS_242_AudioNerve(NerveBase):
    """
    AUDIO NERVE (Sensory)
    Monitors AMSV state and plays procedurally generated .wav files asynchronously via winmm.dll
    """
    NERVE_ID = "SENS_242"
    DEPARTMENT = "SENS"
    DIVISION = "audio_feedback"
    PIPELINE = "runtime"
    WIRE_COLOR = "yellow"

    def __init__(self):
        super().__init__()
        
        self.winmm = ctypes.windll.winmm
        self.PlaySoundW = self.winmm.PlaySoundW
        self.PlaySoundW.argtypes = [ctypes.c_wchar_p, ctypes.c_void_p, ctypes.c_uint32]
        self.PlaySoundW.restype = ctypes.c_int
        
        # Determine base path for PyInstaller or Dev mode
        if hasattr(sys, '_MEIPASS'):
            self.base_path = os.path.join(sys._MEIPASS, 'assets', 'audio')
        else:
            self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../assets/audio'))
            
        self.audio_thread = threading.Thread(target=self._audio_loop, daemon=True)
        self.audio_thread.start()

    def _play(self, filename):
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            self.PlaySoundW(path, None, SND_FILENAME | SND_ASYNC)

    def fire(self):
        pass
        
    def _audio_loop(self):
        print("[SENS_242] Procedural Audio Nerve ACTIVE.")
        
        # State tracking
        last_bullets = [0.0] * 11
        last_enemies = [1.0] * 91
        last_emp = 0.0
        last_state = 0
        
        while True:
            # Check Lasers
            for i in range(1, 11):
                z = amsv_block.entities[i].z
                if z > 0 and last_bullets[i] == 0:
                    self._play("shoot.wav")
                last_bullets[i] = z
                
            # Check Enemy Deaths (61 to 90)
            for i in range(61, 91):
                h = amsv_block.entities[i].health
                if h <= 0 and last_enemies[i] > 0:
                    self._play("explosion.wav")
                last_enemies[i] = h
                
            # Check EMP
            emp = amsv_block.entities[180].z
            if emp > 0 and last_emp == 0:
                self._play("glitch.wav")
            last_emp = emp
            
            # Check Game State (Victory/Win/Powerup)
            current_state = amsv_block.state
            if current_state == 2 and last_state != 2:
                # Win
                self._play("powerup.wav")
            if current_state == 3 and last_state != 3:
                # Keycard
                self._play("powerup.wav")
            if current_state == 4 and last_state != 4:
                # Extraction
                self._play("powerup.wav")
            last_state = current_state
            
            time.sleep(0.05)

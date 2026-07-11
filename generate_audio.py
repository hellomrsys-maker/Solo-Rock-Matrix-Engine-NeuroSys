import wave
import struct
import math
import random
import os

os.makedirs("assets/audio", exist_ok=True)

def save_wav(filename, samples, sample_rate=44100):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for s in samples:
            # Clamp and pack
            val = max(-32767, min(32767, int(s * 32767)))
            wav_file.writeframesraw(struct.pack("<h", val))

def generate_shoot():
    samples = []
    duration = 0.15
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Frequency sweeps down from 880Hz to 220Hz
        freq = 880 - (880 - 220) * (t / duration)
        # Square wave for retro feel
        val = 0.5 if math.sin(2 * math.pi * freq * t) > 0 else -0.5
        # Exponential decay envelope
        env = math.exp(-t * 20)
        samples.append(val * env * 0.5) # Reduced volume
    save_wav("assets/audio/shoot.wav", samples)

def generate_explosion():
    samples = []
    duration = 0.4
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # White noise
        val = random.uniform(-1, 1)
        # Exponential decay envelope
        env = math.exp(-t * 10)
        samples.append(val * env * 0.8)
    save_wav("assets/audio/explosion.wav", samples)

def generate_powerup():
    samples = []
    duration = 0.3
    sample_rate = 44100
    # Arpeggio: C4, E4, G4, C5
    notes = [261.63, 329.63, 392.00, 523.25]
    segment = int(duration * sample_rate / len(notes))
    
    for note in notes:
        for i in range(segment):
            t = i / sample_rate
            val = 0.5 if math.sin(2 * math.pi * note * t) > 0 else -0.5
            env = 1.0 - (i / segment)
            samples.append(val * env * 0.4)
    save_wav("assets/audio/powerup.wav", samples)

def generate_glitch():
    samples = []
    duration = 0.5
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Fast modulating frequency
        mod = math.sin(2 * math.pi * 50 * t)
        freq = 1000 + 500 * mod
        # Noise mixed with square wave
        val = 0.5 if math.sin(2 * math.pi * freq * t) > 0 else -0.5
        noise = random.uniform(-0.2, 0.2)
        env = math.exp(-t * 5)
        samples.append((val + noise) * env * 0.6)
    save_wav("assets/audio/glitch.wav", samples)

if __name__ == "__main__":
    print("Generating Procedural Audio...")
    generate_shoot()
    generate_explosion()
    generate_powerup()
    generate_glitch()
    print("Audio generation complete.")

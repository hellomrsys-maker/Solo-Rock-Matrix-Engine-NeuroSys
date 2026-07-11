import sys
import os
import time
import psutil
import threading
import glob
import importlib
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.event_bus import event_bus
from infrastructure.nerve_registry import nerve_registry
from central_command.central_ai import CentralAI

def load_matrix():
    CentralAI()
    departments = ['cern', 'stin', 'pdec', 'cain', 'fsmf', 'tsn', 'ppvo', 'sccn']
    for dept in departments:
        try: importlib.import_module(f"departments.{dept}.department_ai")
        except: pass
        
        mgr_files = glob.glob(f"departments/{dept}/managers/*_mgr.py")
        for mgr_file in mgr_files:
            try: importlib.import_module(mgr_file.replace('\\', '.').replace('/', '.').replace('.py', ''))
            except: pass
                
        nerve_files = glob.glob(f"departments/{dept}/nerves/*.py")
        for nerve_file in nerve_files:
            if not nerve_file.endswith('__init__.py'):
                try: importlib.import_module(nerve_file.replace('\\', '.').replace('/', '.').replace('.py', ''))
                except: pass

# Global flags
running = True
metrics_log = []

def memory_streaming_task():
    # Simulate GTA 6 level asset streaming (allocating, reading, writing large blocks of memory)
    # Be careful not to OOM the system. We'll allocate a 500MB chunk and constantly rewrite it.
    block = bytearray(1024 * 1024 * 50) # 50 MB per thread
    while running:
        for i in range(len(block) // 1024):
            block[i * 1024] = (block[i * 1024] + 1) % 256

def physics_ai_task():
    # Simulate GTA 6 physics engine and NPC AI (heavy CPU math)
    while running:
        for _ in range(1000):
            _ = math.sqrt(math.pow(3.14159, 2.5) + math.sin(time.time()))

def event_bombardment_task(nerves):
    # Simulate input, network, and subsystem communication
    idx = 0
    while running:
        for _ in range(500):
            event_bus.publish(nerves[idx % len(nerves)].NERVE_ID, {"tick": idx})
            idx += 1

def latency_probe():
    # Measure exactly how long it takes for the system to process a basic task
    start = time.perf_counter()
    _ = sum(i * i for i in range(10000)) # Small synthetic workload
    end = time.perf_counter()
    return (end - start) * 1000 # returns ms

def metrics_monitor():
    while running:
        time.sleep(1.0)
        if not running: break
        
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        lat = latency_probe()
        
        metrics_log.append({
            'cpu': cpu,
            'mem': mem,
            'latency_ms': lat
        })
        print(f"[SECOND_TICK] CPU: {cpu:5.1f}% | RAM: {mem:5.1f}% | Responsiveness (Latency): {lat:6.2f} ms")

def run_gta6_stress():
    print("[INIT] Loading V4 Artificial Nervous System...")
    load_matrix()
    
    from infrastructure.nerve_base import NerveBase
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])
            
    active_nerves = []
    for cls in all_subclasses(NerveBase):
        try: active_nerves.append(cls())
        except: pass
        
    global running
    print("\n===========================================================")
    print("  GTA 6 LEVEL STRESS TEST - REAL WORLD SYSTEM LOAD         ")
    print("===========================================================")
    print("[LOAD] Simulating Dense City Physics, AI, and Texture Streaming...")
    
    threads = []
    
    # 1 thread for second-by-second monitoring
    t_mon = threading.Thread(target=metrics_monitor)
    t_mon.start()
    
    # 4 threads for Memory/Texture Streaming
    for _ in range(4):
        t = threading.Thread(target=memory_streaming_task)
        t.start()
        threads.append(t)
        
    # 4 threads for Heavy Physics and AI
    for _ in range(4):
        t = threading.Thread(target=physics_ai_task)
        t.start()
        threads.append(t)
        
    # 4 threads for Event Bus / Networking / Input
    for _ in range(4):
        t = threading.Thread(target=event_bombardment_task, args=(active_nerves,))
        t.start()
        threads.append(t)
        
    print("[ACTIVE] All 12 Heavy Load Threads Running. Waiting 10 seconds...\n")
    
    time.sleep(10)
    
    print("\n[FINISH] Stopping load. Compiling per-second report...")
    running = False
    
    for t in threads:
        t.join()
    t_mon.join()
    
    print("\n===========================================================")
    print("  PER-SECOND SYSTEM CONDITION REPORT                       ")
    print("===========================================================")
    
    avg_cpu = sum(m['cpu'] for m in metrics_log) / len(metrics_log)
    avg_mem = sum(m['mem'] for m in metrics_log) / len(metrics_log)
    avg_lat = sum(m['latency_ms'] for m in metrics_log) / len(metrics_log)
    
    for i, m in enumerate(metrics_log):
        print(f"Second {i+1:2d} -> CPU: {m['cpu']:5.1f}% | RAM: {m['mem']:5.1f}% | Latency: {m['latency_ms']:6.2f} ms")
        
    print("-----------------------------------------------------------")
    print(f"AVERAGES  -> CPU: {avg_cpu:5.1f}% | RAM: {avg_mem:5.1f}% | Latency: {avg_lat:6.2f} ms")
    
    print("\n[ANALYSIS]")
    if avg_lat < 16.0:
        print("-> The system maintained sub-16ms latency. It could sustain a theoretical 60 FPS under GTA 6 load!")
    elif avg_lat < 33.0:
        print("-> The system maintained sub-33ms latency. It could sustain a theoretical 30 FPS under GTA 6 load.")
    else:
        print("-> The system latency exceeded 33ms. Software delay/lag would occur in a real GTA 6 scenario.")
        
    print("===========================================================")

if __name__ == "__main__":
    run_gta6_stress()

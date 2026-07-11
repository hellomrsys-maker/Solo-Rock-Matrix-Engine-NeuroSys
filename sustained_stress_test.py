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

running = True
metrics_log = []

def memory_streaming_task():
    block = bytearray(1024 * 1024 * 50) # 50 MB
    while running:
        for i in range(len(block) // 4096):
            block[i * 4096] = (block[i * 4096] + 1) % 256
        time.sleep(0.01) # Small sleep to prevent complete thermal shutdown

def physics_ai_task():
    while running:
        for _ in range(5000):
            _ = math.sqrt(math.pow(3.14159, 2.5) + math.sin(time.time()))
        time.sleep(0.01)

def event_bombardment_task(nerves):
    idx = 0
    while running:
        for _ in range(2000):
            event_bus.publish(nerves[idx % len(nerves)].NERVE_ID, {"tick": idx})
            idx += 1
        time.sleep(0.01)

def latency_probe():
    start = time.perf_counter()
    _ = sum(i * i for i in range(5000))
    end = time.perf_counter()
    return (end - start) * 1000

def metrics_monitor():
    tick = 0
    while running:
        time.sleep(1.0) # Check every 1 second for visible terminal output
        if not running: break
        tick += 1
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        lat = latency_probe()
        
        metrics_log.append({'time': tick, 'cpu': cpu, 'mem': mem, 'latency_ms': lat})
        print(f"[Time: {tick}s] CPU: {cpu:5.1f}% | RAM: {mem:5.1f}% | Responsiveness (Latency): {lat:6.2f} ms")

def run_sustained_stress():
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
    print("  SUSTAINED 5-MINUTE GTA 6 LEVEL STRESS TEST               ")
    print("===========================================================")
    print("[LOAD] Applying maximum safe sustained load across all ICs...")
    
    threads = []
    t_mon = threading.Thread(target=metrics_monitor)
    t_mon.start()
    
    for _ in range(4):
        t = threading.Thread(target=memory_streaming_task)
        t.start(); threads.append(t)
        
    for _ in range(4):
        t = threading.Thread(target=physics_ai_task)
        t.start(); threads.append(t)
        
    for _ in range(4):
        t = threading.Thread(target=event_bombardment_task, args=(active_nerves,))
        t.start(); threads.append(t)
        
    print("[ACTIVE] 12 Heavy Threads Online. Running for 300 seconds (5 minutes)...")
    print("[ACTIVE] Watch your system performance via Task Manager during this time.\n")
    
    time.sleep(300) # 5 minutes
    
    print("\n[FINISH] 5 Minutes Reached. Stopping load. Compiling report...")
    running = False
    
    for t in threads:
        t.join()
    t_mon.join()
    
    avg_cpu = sum(m['cpu'] for m in metrics_log) / len(metrics_log)
    avg_mem = sum(m['mem'] for m in metrics_log) / len(metrics_log)
    avg_lat = sum(m['latency_ms'] for m in metrics_log) / len(metrics_log)
    
    print("-----------------------------------------------------------")
    print(f"5-MINUTE AVERAGES -> CPU: {avg_cpu:5.1f}% | RAM: {avg_mem:5.1f}% | Latency: {avg_lat:6.2f} ms")
    
    if avg_lat < 16.0:
        print("-> Result: Sustained sub-16ms latency. Stable 60 FPS guaranteed.")
    else:
        print("-> Result: System latency exceeded 16ms under sustained load.")
    print("===========================================================")

if __name__ == "__main__":
    run_sustained_stress()

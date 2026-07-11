import os

departments = {
    'cern': ['os_isolation', 'cache_control', 'thread_dispatch', 'interrupt_authority', 'clock_governance', 'thermal_prediction', 'error_containment', 'memory_mapping', 'process_priority', 'global_coordination'],
    'stin': ['pain_reception', 'reactive_preamp', 'pump_execution', 'touch_coordinate', 'gesture_tracking', 'haptic_feedback', 'input_debounce', 'peripheral_routing', 'pressure_mapping', 'collision_prediction'],
    'pdec': ['vrm_regulation', 'battery_chemistry', 'transient_defense', 'power_routing', 'thermal_throttle', 'rail_voltage', 'capacitor', 'efficiency', 'display_power', 'motherboard_trace'],
    'cain': ['instruction_routing', 'cpu_thread', 'gpu_pipeline', 'tpu_tensor', 'cache_coherency', 'noc_fabric', 'dma_arbitration', 'register_pipeline', 'high_end_mapping', 'execution_lock'],
    'fsmf': ['junk_filtration', 'nvme_storage', 'vram_allocation', 'ram_bus', 'cache_pollution', 'decompression', 'bandwidth', 'page_prefetch', 'zero_copy', 'garbage_collection'],
    'tsn': ['chassis_telemetry', 'die_temperature', 'fan_control', 'voltage_monitoring', 'acoustic_filter', 'network_latency', 'peripheral_power', 'display_status', 'wireless_filter', 'clock_stability'],
    'ppvo': ['physics_prediction', 'frame_generation', 'display_sync', 'ray_tracing', 'texture_streaming', 'resolution_scaling', 'culling_lod', 'audio_spatial', 'ui_overlay', 'shadow_lighting'],
    'sccn': ['pink_loop', 'blue_loop', 'teal_loop', 'magenta_loop', 'orange_loop', 'green_loop', 'purple_loop', 'permutation_sync', 'coherency_lock', 'total_closure']
}

base_dir = 'departments'

def to_camel_case(snake_str):
    return "".join(x.title() for x in snake_str.split('_'))

for dept, managers in departments.items():
    dept_dir = os.path.join(base_dir, dept)
    mgr_dir = os.path.join(dept_dir, 'managers')
    nerves_dir = os.path.join(dept_dir, 'nerves')
    
    os.makedirs(mgr_dir, exist_ok=True)
    os.makedirs(nerves_dir, exist_ok=True)
    
    # Init files
    open(os.path.join(dept_dir, '__init__.py'), 'w').close()
    open(os.path.join(mgr_dir, '__init__.py'), 'w').close()
    open(os.path.join(nerves_dir, '__init__.py'), 'w').close()
    
    # Department AI
    dept_class = dept.upper() + "DepartmentAI"
    with open(os.path.join(dept_dir, 'department_ai.py'), 'w') as f:
        f.write(f'''from infrastructure.department_base import DepartmentAI

class {dept_class}(DepartmentAI):
    DEPARTMENT_ID = "{dept.upper()}"
    
    def autonomous_decision(self, local_state):
        pass
''')

    nerve_counter = 1
    
    for mgr in managers:
        # Create manager file
        mgr_class = to_camel_case(mgr) + "Manager"
        with open(os.path.join(mgr_dir, f'{mgr}_mgr.py'), 'w') as f:
            f.write(f'''from infrastructure.manager_base import ManagerBase

class {mgr_class}(ManagerBase):
    MANAGER_ID = "{dept.upper()}_{mgr.upper()}"
    DEPARTMENT = "{dept.upper()}"
    DIVISION = "{mgr}"
''')
        
        # Create 30 nerves for this manager
        for i in range(30):
            nerve_id_str = f"{dept.upper()}_{nerve_counter:03d}"
            nerve_name = f"{mgr}_nerve_{i+1}"
            nerve_file = f"{dept}_{nerve_counter:03d}_{nerve_name}.py"
            nerve_class = f"{dept.upper()}_{nerve_counter:03d}_{to_camel_case(nerve_name)}"
            
            with open(os.path.join(nerves_dir, nerve_file), 'w') as f:
                f.write(f'''from infrastructure.nerve_base import NerveBase

class {nerve_class}(NerveBase):
    NERVE_ID = "{nerve_id_str}"
    DEPARTMENT = "{dept.upper()}"
    DIVISION = "{mgr}"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
''')
            nerve_counter += 1

print("Generated 8 departments, 80 managers, and 2400 nerves.")

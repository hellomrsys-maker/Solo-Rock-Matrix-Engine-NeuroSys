import time
from .event_bus import event_bus
from .pipeline_registry import pipeline_registry
from .wire_registry import wire_registry
from .nerve_registry import nerve_registry

class NerveBase:
    NERVE_ID = "UNKNOWN"
    DEPARTMENT = "UNKNOWN"
    DIVISION = "UNKNOWN"
    PIPELINE = "UNKNOWN"          # input_comm | timing_comm | performance | runtime | output
    WIRE_COLOR = "UNKNOWN"        # yellow | teal | dark_red | pink | orange | green | purple | blue | magenta
    SOURCE_NODE = "UNKNOWN"       # node1 | node2 | node3 | node4 | ai_core
    TARGET_NODE = "UNKNOWN"
    PRIORITY = 0                  # 0=normal, 1=high, 2=critical, 3=emergency

    def __init__(self):
        self.is_alive = True
        self.fire_count = 0
        self.last_fire_ns = 0
        
        # Biological Properties (Phase 3 & 4: Action Potentials & Synapses)
        self.synaptic_weight = 1.0
        self.membrane_potential = -75.0      # Resting Potential
        self.action_potential_threshold = -55.0
        self.Na_channels_open = False
        self.K_channels_open = False
        self.ap_state = "RESTING"            # RESTING | RISING | FALLING | UNDERSHOOT
        self.chemical_inbox = []             # List of {"type": "EPSP" | "IPSP", "amount": float}
        
        # Cytology (Organelles)
        self.mitochondria_count = 10   # Controls max ATP and regen efficiency
        self.ribosome_count = 50       # Controls protein synthesis (healing)
        self.nucleus_active = True     # Controls gene expression
        
        # Neurites (Structure)
        self.dendrite_count = 5        # Number of input connections it can form
        self.axon_length = 1.0         # Golgi Type I (long) vs Type II (short)
        self.is_myelinated = False     # Myelin sheath increases conduction speed
        
        # Metabolic Properties (Phase 2: Respiration)
        self.atp = self.mitochondria_count * 10.0
        self.blood_flow_rate = 1.0
        self.glucose_level = 100.0     # Required for Glycolysis & Krebs
        self.oxygen_level = 100.0      # Required for Krebs
        self.lactate_level = 0.0       # Toxic byproduct of anaerobic Glycolysis
        self.proton_gradient = 0.0     # Chemiosmosis: converts to ATP
        
        # Auto-register on EventBus
        event_bus.subscribe(self.NERVE_ID, self._on_signal)
        # Auto-register in Pipeline
        pipeline_registry.register(self)
        # Auto-register in Wire
        wire_registry.register(self)
        # Auto-register in global nerve list
        nerve_registry.register(self)

    def _on_signal(self):
        self.fire_count += 1
        self.last_fire_ns = time.time_ns()
        self.fire()

    def fire(self):
        """Override this. This is the ONE thing this nerve does."""
        raise NotImplementedError("Nerves must implement the fire() method.")

    def receive_neurotransmitter(self, ntype, amount):
        """Phase 4: Chemical Synapses (EPSP/IPSP)"""
        self.chemical_inbox.append({"type": ntype, "amount": amount})

    def process_action_potential(self):
        """Processes the 4 Phases of an Action Potential and Sodium-Potassium Pump."""
        
        # Process Spatial/Temporal Summation of Neurotransmitters
        for packet in self.chemical_inbox:
            if packet["type"] == "EPSP":
                self.membrane_potential += packet["amount"]
            elif packet["type"] == "IPSP":
                self.membrane_potential -= packet["amount"]
        self.chemical_inbox.clear()
        
        # 1. RESTING PHASE (Sodium-Potassium Pump maintains -75mV)
        if self.ap_state == "RESTING":
            if self.membrane_potential < -75.0:
                if self.atp >= 0.1:
                    self.atp -= 0.1
                    self.membrane_potential += 1.0  # Pump forces voltage back up
                if self.membrane_potential > -75.0:
                    self.membrane_potential = -75.0
                    
            if self.Na_channels_open:
                # Direct excitation (from player perception)
                self.membrane_potential += (2.0 * self.synaptic_weight)
                
            # Check for threshold after EPSPs and perception
            if self.membrane_potential >= self.action_potential_threshold:
                self.ap_state = "RISING"
            elif self.membrane_potential > -75.0 and not self.Na_channels_open:
                # Decay back to resting if sub-threshold
                self.membrane_potential -= 1.0
                
        # 2. RISING PHASE (Depolarization Spike)
        elif self.ap_state == "RISING":
            self.membrane_potential += 20.0
            if self.membrane_potential >= 35.0:
                self.membrane_potential = 35.0
                self._on_signal() # <--- THE NERVE FIRES ITS PAYLOAD HERE!
                self.ap_state = "FALLING"
                self.Na_channels_open = False
                self.K_channels_open = True
                
        # 3. FALLING PHASE (Repolarization)
        elif self.ap_state == "FALLING":
            self.membrane_potential -= 15.0
            if self.membrane_potential <= -75.0:
                self.ap_state = "UNDERSHOOT"
                self.K_channels_open = False
                
        # 4. UNDERSHOOT PHASE (Refractory Period)
        elif self.ap_state == "UNDERSHOOT":
            # Voltage crashes down to -90mV, paralyzing the nerve!
            self.membrane_potential -= 5.0
            if self.membrane_potential <= -90.0:
                self.membrane_potential = -90.0
                self.ap_state = "RESTING" # Returns to resting, where the Pump will fix it.

    def get_health(self):
        return {
            "id": self.NERVE_ID,
            "alive": self.is_alive, 
            "fires": self.fire_count,
            "last_fire_ns": self.last_fire_ns,
            "synaptic_weight": self.synaptic_weight,
            "membrane_potential": self.membrane_potential,
            "ap_state": self.ap_state,
            "atp": self.atp,
            "blood_flow_rate": self.blood_flow_rate
        }

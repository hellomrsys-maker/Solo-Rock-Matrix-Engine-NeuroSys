with open("realtime_boot.py", "r") as f:
    content = f.read()

for i in range(31, 61):
    id_str = f"{i:03d}"
    old_import = f"from departments.cain.nerves.cain_{id_str}_instruction_routing_nerve_{i} import CAIN_{id_str}_InstructionRoutingNerve{i}"
    new_import = f"from departments.cain.nerves.cain_{id_str}_glial_cell_nerve_{i} import CAIN_{id_str}_GlialCellNerve{i}"
    content = content.replace(old_import, new_import)
    
    old_inst = f"n{i} = CAIN_{id_str}_InstructionRoutingNerve{i}()"
    new_inst = f"n{i} = CAIN_{id_str}_GlialCellNerve{i}()"
    content = content.replace(old_inst, new_inst)

with open("realtime_boot.py", "w") as f:
    f.write(content)
print("Patched realtime_boot.py for Glial Cells.")

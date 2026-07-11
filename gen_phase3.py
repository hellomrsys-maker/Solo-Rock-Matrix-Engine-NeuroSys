import os

nodes = [
    'node1_software',
    'node2_executive',
    'node3_balance',
    'node4_hardware',
    'ai_hub'
]

def create_scaffold(dir_path, names):
    with open(os.path.join(dir_path, '__init__.py'), 'w') as f:
        pass
    for name in names:
        file_path = os.path.join(dir_path, f'{name}.py')
        class_name = ''.join(word.capitalize() for word in name.split('_'))
        content = f'''class {class_name}:
    """
    Node class for {name}
    """
    def __init__(self):
        self.connected_departments = []

    def route_payload(self, payload):
        pass
'''
        with open(file_path, 'w') as f:
            f.write(content)

create_scaffold('nodes', nodes)
print('Phase 3 files created.')

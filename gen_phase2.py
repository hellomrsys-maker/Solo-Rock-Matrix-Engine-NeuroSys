import os

pipelines = [
    'input_comm_pipeline',
    'timing_comm_pipeline',
    'performance_pipeline',
    'runtime_pipeline',
    'output_pipeline'
]

wires = [
    'yellow_wire',
    'teal_wire',
    'dark_red_wire',
    'pink_wire',
    'orange_wire',
    'green_wire',
    'purple_wire',
    'blue_wire',
    'magenta_wire'
]

def create_scaffold(dir_path, names, category):
    with open(os.path.join(dir_path, '__init__.py'), 'w') as f:
        pass
    for name in names:
        file_path = os.path.join(dir_path, f'{name}.py')
        class_name = ''.join(word.capitalize() for word in name.split('_'))
        content = f'''class {class_name}:
    """
    {category} class for {name}
    """
    def __init__(self):
        self.active_nerves = []

    def route_payload(self, payload):
        pass
'''
        with open(file_path, 'w') as f:
            f.write(content)

create_scaffold('infrastructure/pipelines', pipelines, 'Pipeline')
create_scaffold('infrastructure/wiring', wires, 'Wire')
print('Phase 2 files created.')

from .func_wrapper import file_property
from .instances_store import InstancesStore
import os

class Component(metaclass=InstancesStore):
    py = file_property('component.py')
    template = file_property('template.vue')
    css = file_property('css.vue')
    js = file_property('js.vue')
    prompt = file_property('prompt.conv')  # New property for .conv files
    user_stories = file_property('user_stories.md')  # New property for .md files
    test_cases = file_property('test_cases.md')  # New property for .md files
    tests = file_property('tests.py')  # New property for .py files
    mock = file_property('mock.py')  # New property for .py files
    vars = file_property('vars.py')  # New property for .py files
    
    def __init__(self, name: str):
        self.name = name
        cwd = os.getcwd()
        self.dir_path = os.path.join(cwd, "bricks/components", name)
        self.out_path = os.path.join(cwd, f"front/pages/{name}.vue")
        os.makedirs(self.dir_path, exist_ok=True)
        
        # Initialize Python file with a basic structure if it does not exist
        if not os.path.exists(os.path.join(self.dir_path, 'component.py')):
            self.py = f"""from agentix import component as c
c('{name}')
"""#TODO add logger


component = Component

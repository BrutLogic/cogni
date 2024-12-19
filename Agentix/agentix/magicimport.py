import glob
import importlib.util
import os
import sys
from rich import print

def dynamic_import(directory_name):
    target_dir = os.getcwd()
    """Dynamically imports all Python files from a specified directory and its subdirectories.

    Args:
        target_dir (str): The base directory to search for Python files.
        directory_name (str): The name of the directory to specifically target for imports.
    """
    if target_dir not in sys.path:
        sys.path.append(target_dir)

    target_files = glob.glob(target_dir + f'/**/{directory_name}/**/*.py', recursive=True)
    
    for file_path in target_files:
        if 'AgentixAgents' in file_path:
            continue
        module_name = os.path.splitext(os.path.relpath(file_path, target_dir))[0].replace(os.sep, '.')
        if module_name not in sys.modules:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            #print(f"Dynamically imported [orange]`{module_name}`[/] from [red]`{file_path}`")

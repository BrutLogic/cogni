import glob
import importlib.util
import os
import sys
from typing import List

def dynamic_import(directory_name: str) -> None:
    """Dynamically imports all Python files from a specified directory and its subdirectories.
    
    Args:
        directory_name: The name of the directory to specifically target for imports
    """
    target_dir = os.getcwd()
    if target_dir not in sys.path:
        sys.path.append(target_dir)

    target_files = glob.glob(target_dir + f'/**/{directory_name}/**/*.py', recursive=True)
    
    for file_path in target_files:
        module_name = os.path.splitext(os.path.relpath(file_path, target_dir))[0].replace(os.sep, '.')
        if module_name not in sys.modules:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

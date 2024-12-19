from .magicimport import dynamic_import
from .wrappers.tool import Tool, tool

# Dynamically import all modules
dynamic_import('wrappers')
dynamic_import('tools')
dynamic_import('agents')

from agentix import func, Func, Tool, Conf, ModuleInfo
from typing import Optional
from pydantic import BaseModel
import os
import yaml
from agentix import func, Func, Tool, Conf, ModuleInfo
from typing import Optional
from pydantic import BaseModel
import os
import yaml
from pathlib import Path


def create_widget(module_info: ModuleInfo):
    widget_path = Path(module_info.module_path) / "widget"
    # Create directory structure
    for directory in "src,assets,templates".split(','):
        Tool['shell'](f"mkdir -p {widget_path}/{directory}")
        
    Tool['shell'](f"""
cd {widget_path};
npm init -y && npm pkg set \
  name="{module_info.name}" \
  version="{module_info.version}" \
  description="{module_info.description}" \
  main="src/index.js" \
  scripts.build="webpack --mode production" \
  scripts.start="webpack serve --mode development" \
  scripts.dev="webpack serve --mode development" && \
npm install --save-dev webpack webpack-cli webpack-dev-server html-webpack-plugin html-webpack-inline-source-plugin style-loader css-loader
                  """)
        
    

    # Create index.js
    with open(widget_path / "src/index.js", 'w') as f:
        f.write("""// Default widget implementation
console.log('Widget loaded');
""")

    # Create package.json
    package_json = {
        "name": module_info.name,
        "version": "1.0.0",
        "description": f"Widget for {module_info.name} module",
        "main": "src/index.js",
        "scripts": {
            "build": "webpack --mode production",
            "dev": "webpack --mode development --watch"
        },
        "author": module_info.author,
        "license": "ISC"
    }

    with open(widget_path / "package.json", 'w') as f:
        yaml.dump(package_json, f)

    # Install webpack
    Tool['shell'](
        f"cd {widget_path} && npm install --save-dev webpack webpack-cli")

    # Create webpack config
    webpack_config = """
const path = require('path');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist'),
    },
};
"""

    with open(widget_path / "webpack.config.js", 'w') as f:
        f.write(webpack_config)


def create_endpoints(module_info: ModuleInfo):
    endpoints_path = Path(module_info.module_path) / "endpoints"
    Tool['shell'](f"mkdir -p {endpoints_path}")

    with open(endpoints_path / f"{module_info.name}.py", 'w') as f:
        f.write(f"""from agentix import endpoint

@endpoint
def {module_info.name}():
    return "Not implemented"
""")


def create_agent(module_info: ModuleInfo):
    agent_path = Path(module_info.module_path) / "agent"
    for directory in "agents,middlewares,prompts,tools,tests".split(','):
        Tool['shell'](
            f"mkdir -p {agent_path}/{directory}")

    with open(agent_path / f"agents/{module_info.name}.py", 'w') as f:
        f.write(f"""from agentix import Agent
Agent('{module_info.name}', 'prompt|gpt4|{module_info.name}_loop')
""")

    with open(agent_path / f"middlewares/{module_info.name}_loop.py", 'w') as f:
        f.write(f"""from agentix import mw, Tool

@mw
def {module_info.name}_loop(ctx, conv):
    return conv
""")

    with open(agent_path / f"prompts/{module_info.name}.conv", 'w') as f:
        f.write(f"""system: You're {module_info.name}.
You're not yet implemented. The only reply you can give for now is:
"Hey there :). My prompt is the default one created by the wizzard. Change it if you want me to do stuff"
""")


def create_manifest(module_info: ModuleInfo):
    manifest_path = Path(module_info.module_path) / "manifest.yml"

    # Determine components
    components = []
    if module_info.agent:
        components.append("agent")
    if module_info.widget:
        components.append("widget")
    if module_info.endpoints:
        components.append("endpoints")

    manifest_content = {
        "name": module_info.name,
        "version": module_info.version,
        # You might want to add this to ModuleInfo
        "description": module_info.description,
        "author": module_info.author,
        "license": "Internal",

        "components": components,

        "dependencies": [],  # You might want to add this to ModuleInfo

        "documentation": {
            "usage": "This module was created using Agentix wizard. Please update this documentation."
        },

        "logo": "assets/logo.png"  # Default value
    }

    with open(manifest_path, 'w') as f:
        yaml.dump(manifest_content, f, sort_keys=False,
                  default_flow_style=False)



@func
def init_module(module_info: ModuleInfo):
    module_info.module_path = str(Path(Conf.GA_modules_dir) / module_info.name)
    Tool['shell'](f"mkdir -p {module_info.module_path}")
    
    create_manifest(module_info)

    if module_info.agent:
        create_agent(module_info)

    if module_info.widget:
        create_widget(module_info)

    if module_info.endpoints:
        create_endpoints(module_info)




@func
def get_all_GA_modules(root_path):
    result = {}

    # Convert to absolute path if not already
    
    # Walk through all directories
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check if manifest.yml exists in current directory
        manifest_path = os.path.join(dirpath, 'manifest.yml')
        if 'manifest.yml' in filenames:
            try:
                # Read and parse the manifest file
                with open(manifest_path, 'r') as f:
                    manifest_content = yaml.safe_load(f)
                
                # Get directory name
                dir_name = os.path.basename(dirpath)
                
                # Add to result dictionary
                result[dir_name] = {
                    "path": '/'.join(dirpath.split('/')[-3:]),
                    "manifest": manifest_content
                }
            except Exception as e:
                raise
                print(f"Error processing {manifest_path}: {str(e)}")
                continue
    
    return result



@func
def list_available_agents():
    ...
    
    
@func
def create_new_agent():
    ...
    
    
@func
def list_available_modules():
    ...
    
    
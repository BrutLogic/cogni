"""CLI interface for Cogni using Fire and Rich."""
import os
import sys
import fire
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.theme import Theme
import subprocess

console = Console(theme=Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold"
}))

if sys.version_info < (3, 8):
    console.print("[error]Python 3.8 or higher is required")
    sys.exit(1)


class CogniCLI:
    """Cogni command line interface."""

    def create(self, name: str):
        """Create a new Cogni project.

        Args:
            name: Name of the project to create
        """
        console.print(Panel(f"Creating new project: [bold blue]{name}[/]"))
        # TODO: Implement project creation

    def init(self):
        """Initialize a Cogni project in the current directory."""
        console.print(Panel("Initializing Cogni project"))
        
        # Get project name
        project_name = Prompt.ask("Enter project name")
        use_boilerplate = Confirm.ask("Create boilerplate ShellAgent?")
        init_git = Confirm.ask("Initialize git repository?")
        
        # Create project directory
        os.makedirs(project_name, exist_ok=True)
        
        # Create main.py
        with open(f"{project_name}/main.py", "w") as f:
            f.write('from cogni import Agent\n\n')
            f.write('def main():\n')
            f.write('    pass\n\n')
            f.write('if __name__ == "__main__":\n')
            f.write('    main()\n')
        
        if use_boilerplate:
            # Create agent directory structure
            agent_base = f"{project_name}/agents/ShellAgent"
            os.makedirs(f"{agent_base}/agents", exist_ok=True)
            os.makedirs(f"{agent_base}/tools", exist_ok=True)
            os.makedirs(f"{agent_base}/prompts", exist_ok=True)
            os.makedirs(f"{agent_base}/middlewares", exist_ok=True)
            
            # Create agent files
            with open(f"{agent_base}/agents/ShellAgent.py", "w") as f:
                f.write('from cogni import Agent\n\n')
                f.write('Agent("ShellAgent", "prompt_histo|gpt4omini|shell_loop")\n')
            
            with open(f"{agent_base}/middlewares/shell_loop.py", "w") as f:
                f.write('from cogni import mw, Tool\n\n')
                f.write('@mw\n')
                f.write('def shell_loop(ctx, conv):\n')
                f.write('    return conv[-1].content\n')
            
            with open(f"{agent_base}/prompts/ShellAgent.conv", "w") as f:
                f.write('system: You are ShellAgent, a helpful assistant.\n\n')
                f.write('user: Hello!\n\n')
                f.write('assistant: Hi! How can I help you today?\n')
            
            with open(f"{agent_base}/tools/shell_tools.py", "w") as f:
                f.write('from cogni import tool\n\n')
                f.write('@tool\n')
                f.write('def echo(text: str) -> str:\n')
                f.write('    """Echo the input text"""\n')
                f.write('    return text\n')
        
        if init_git:
            subprocess.run(['git', 'init', project_name])
            
        console.print(f"[green]✓[/] Created Cogni project: {project_name}")

    def run(self, agent: str, input: str):
        """Run an agent with given input.

        Args:
            agent: Name of the agent to run
            input: Input text for the agent
        """
        console.print(Panel(f"Running agent [bold blue]{agent}[/]"))
        # TODO: Implement agent running

    def __str__(self):
        return """Cogni CLI

Usage:
    cogni create <name>     Create a new project
    cogni init             Initialize project in current directory
    cogni run <agent> <input>  Run an agent"""


def main():
    """Main entry point for the Cogni CLI."""
    try:
        if len(sys.argv) == 1:
            console.print(CogniCLI())
            sys.exit(0)
        fire.Fire(CogniCLI)
    except Exception as e:
        console.print(f"[error]Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

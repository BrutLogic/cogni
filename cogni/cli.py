"""CLI interface for Cogni using Fire and Rich."""
import fire
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

console = Console(theme=Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold"
}))

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
        # TODO: Implement project initialization
        
    def run(self, agent: str, input: str):
        """Run an agent with given input.
        
        Args:
            agent: Name of the agent to run
            input: Input text for the agent
        """
        console.print(Panel(f"Running agent [bold blue]{agent}[/]"))
        # TODO: Implement agent running

def main():
    """Main entry point for the Cogni CLI."""
    try:
        fire.Fire(CogniCLI)
    except Exception as e:
        console.print(f"[error]Error: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    main()

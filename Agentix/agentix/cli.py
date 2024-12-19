import os

from rich.columns import Columns
from rich.panel import Panel
import fire

from rich import print
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

from agentix import Func, Conf, ModuleInfo


class AgentixCLI:
    def create(self):
        console = Console()

        # Display title
        title = "[bold blue]Agentix module creation wizard[/bold blue]"
        console.print(Panel(title, style="green"), justify="center")
        modules_dir = os.path.abspath("./AgentixAgents/modules")
        # Check directory
        if not os.path.isdir(modules_dir):
            console.print(
                "[red]You should run `agentix create` in the root dir of `GoodAssistant` project[/red]")
            return
        Conf.GA_modules_dir = modules_dir

        existing_modules = Func['get_all_GA_modules']()

        # Gather information
        name = None
        while name is None:
            name_input = Prompt.ask("[cyan]Module name")
            if name_input not in existing_modules:
                name = name_input
                break
            console.print(
                f"[green]A module names [red]{name_input}[/red][green] already exists. Please pick another name")

        author = Prompt.ask("[cyan]Author")
        description = Prompt.ask("[cyan]Description")
        version = Prompt.ask("[cyan]version", default='0.0.1')
        # Ask for boilerplates
        create_agent = Confirm.ask(
            "[cyan]Create boilerplate for agent?[/cyan]",
            default=False
        )

        create_endpoints = Confirm.ask(
            "[cyan]Create boilerplate for endpoints?[/cyan]",
            default=False
        )

        create_widget = Confirm.ask(
            "[cyan]Create boilerplate for widget?[/cyan]",
            default=False
        )

        # Check if at least one is selected
        if not any([create_agent, create_endpoints, create_widget]):
            console.print(
                "[red]At least one of `agent`, `endpoint` or `widget` should exist[/red]")
            return

        # Widget framework choice
        if create_widget:
            console.print(
                "\n[yellow]For the following question, `(N)uxt.js/(R)eact.js` will be added later[/yellow]")
            widget_type = Prompt.ask(
                "[cyan]Widget boilerplate?[/cyan]",
                choices=["V"],
                default="V"
            )
        else:
            widget_type = None

        # Create summary table
        table = Table(title="Summary of choices")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Module name", name)
        table.add_row("Author", author)
        table.add_row("Create agent", "✅" if create_agent else "❌")
        table.add_row("Create endpoints", "✅" if create_endpoints else "❌")
        table.add_row("Create widget", "✅" if create_widget else "❌")
        if widget_type:
            table.add_row("Widget type", f"Vanilla JS")

        console.print("\n")
        console.print(table)

        # Final confirmation
        confirm = Confirm.ask(
            "\n[yellow]Do you confirm these choices?[/yellow]")
        if not confirm:
            console.print("[red]Operation cancelled[/red]")
            return

        console.print("[green]Proceeding with module creation...[/green]")

        module_info = ModuleInfo(
            name=name,
            author=author,
            version=version,
            description=description,
            agent=create_agent,
            endpoints=create_endpoints,
            widget=create_widget,
            widget_type=widget_type,
        )
        
        Func['init_module'](module_info)
        print("done")

    def credate(self):
        """Creates a new agent structure."""
        print('ca')
        print(os.getcwd())
        quit()
        base_path = os.path.join('./agents', name)
        directories = ['agents', 'middlewares', 'tools', 'prompts', 'tests',]
        for directory in directories:
            os.makedirs(os.path.join(base_path, directory), exist_ok=True)
        # Create agent, middleware, and test files
        agent_file_path = os.path.join(base_path, 'agents', f'{name}.py')
        middleware_file_path = os.path.join(
            base_path, 'middlewares', f'{name}_loop.py')
        test_file_path = os.path.join(base_path, 'tests', f'test_{name}.py')
        prompt_file_path = os.path.join(base_path, 'prompts', f'{name}.conv')

        for fp, content in zip(
            [agent_file_path,
             middleware_file_path,
             test_file_path,
             prompt_file_path],
            [
                f'''from agentix import Agent
Agent('{name}', 'prompt_histo|gpt4|{name}_loop')''',

                f'''from agentix import mw, Tool

@mw
def {name}_loop(ctx, conv):
    return conv''',
                '''''',
                f'''system:You are {name}, an AGI
__-__
user:hi
__-__
assistant:How can I help you ma bro ?'''
            ]):
            if os.path.isfile(fp):
                continue
            with open(fp, 'w') as f:
                f.write(content)

        print(
            f"[red b]Agentix:[/]Agent structure for [green b]{name}[/] created successfully.")


def main():
    return fire.Fire(AgentixCLI)

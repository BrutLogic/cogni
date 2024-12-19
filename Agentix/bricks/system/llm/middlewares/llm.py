from rich import print
from rich.syntax import Syntax
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from agentix import mw


@mw
def llm(ctx, conv):

    conv.should_infer = ctx['hops'] == 0
    return conv


@mw
def gpt3(ctx, conv):
    conv.should_infer = ctx['hops'] == 0
    conv.llm = 'gpt-3.5-turbo'
    return conv


@mw
def gpt4(ctx, conv):
    conv.should_infer = ctx['hops'] == 0
    conv.llm = 'gpt-4-turbo-preview'
    return conv


@mw
def aider_ask(ctx, conv):
    conv.should_infer = ctx['hops'] == 0
    conv.llm = 'aider_ask'
    return conv


@mw
def aider_code(ctx, conv):
    conv.should_infer = ctx['hops'] == 0
    conv.llm = 'aider_code'
    return conv


@mw
def gpt4o(ctx, conv):
    conv.should_infer = ctx['hops'] == 0
    conv.llm = 'gpt-4o'
    return conv


@mw
def gpt4omini(ctx, conv):
    conv.should_infer = ctx['hops'] == 0
    conv.llm = 'gpt-4o-mini'
    return conv


@mw
def o1mini(ctx, conv):
    conv.should_infer = ctx['hops'] == 0
    conv.llm = 'o1-mini'
    return conv


@mw
def stream(ctx, conv):
    conv._flags['stream'] = True
    return conv


@mw
def debug(ctx, conv):
    console = Console()

    # Header
    header = Panel(
        "[bold red]DEBUG",
        border_style="yellow",
        expand=False,
        padding=(1, 1),
    )
    console.print(header)

    # Context
    ctx_table = Table(title="Context", show_header=True,
                      header_style="bold magenta")
    ctx_table.add_column("Key", style="cyan", no_wrap=True)
    ctx_table.add_column("Value", style="green")

    for key, value in ctx.items():
        ctx_table.add_row(str(key), str(value))

    console.print(Panel(ctx_table, expand=False, border_style="blue"))

    # Conversation
    conv_syntax = Syntax(str(conv), "python",
                         theme="monokai", line_numbers=True)
    console.print(Panel(conv_syntax, title="Conversation",
                  expand=False, border_style="green"))

    # Footer
    footer = Panel(
        "[bold red]End of Debug Output",
        border_style="yellow",
        expand=False,
        padding=(1, 1),
    )
    console.print(footer)

    quit()


@mw
def last_msg_content(ctx, conv):
    return conv[-1].content

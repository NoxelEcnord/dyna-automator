# dyna_automator/cli/shell.py
import typer
import asyncio
from typing_extensions import Annotated
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from ..browser_manager import browser_manager
from ..element_handler import ElementHandler
import shlex
import time
import re

shell_app = typer.Typer()
console = Console()

class DynaShell:
    def __init__(self):
        self.session = PromptSession(history=FileHistory('.dyna_history'))
        self.variables = {}
        self.loop = asyncio.get_event_loop()

    async def run(self, url: str | None, headful: bool):
        console.print("[bold green]Welcome to the Dyna-Automator Interactive Shell![/bold green]")
        console.print("Type 'help' for a list of commands.")
        
        browser_manager.headless = not headful
        browser_manager.start()

        if url:
            browser_manager.go_to(url)

        while True:
            try:
                text = await self.session.prompt_async('> ')
                await self.process_command(text)
            except (KeyboardInterrupt, EOFError):
                break
        
        browser_manager.stop()
        console.print("[bold yellow]Exiting Dyna-Automator Shell.[/bold yellow]")

    async def process_command(self, text: str):
        text = text.strip()
        if not text:
            return
            
        parts = shlex.split(text)
        command = parts[0]
        args = parts[1:]

        # LET command (variable assignment)
        if text.startswith("let "):
            match = re.match(r"let\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)", text)
            if match:
                var_name, expression = match.groups()
                value = await self.evaluate_expression(expression)
                self.variables[var_name] = value
                console.print(f"Stored in variable: [bold cyan]{var_name}[/bold cyan]")
                return
            else:
                console.print("[bold red]Invalid 'let' syntax. Use 'let var_name = expression'.[/bold red]")
                return

        # Simple commands
        if command == "go":
            if args:
                browser_manager.go_to(args[0])
            else:
                console.print("[bold red]Usage: go <url>[/bold red]")
        elif command == "exit" or command == "quit":
            raise EOFError()
        elif command == "help":
            self.print_help()
        elif command == "wait":
            self.handle_wait(args)
        elif command == "find":
            selector = " ".join(args)
            element = self.find_element(selector)
            if element:
                console.print(element)
        else:
            # Evaluate expression (e.g. my_var.click())
            try:
                await self.evaluate_expression(text)
            except Exception as e:
                console.print(f"[bold red]Error: {e}[/bold red]")
                
    async def evaluate_expression(self, expression: str):
        # Direct variable access
        if expression in self.variables:
            return self.variables[expression]

        # Method calls on variables (e.g., my_button.click())
        match = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\.(.*)", expression)
        if match:
            var_name, method_call = match.groups()
            if var_name in self.variables:
                element = self.variables[var_name]
                # This is a simplification. A real implementation would parse the method and args.
                if method_call == "click()":
                    element.click()
                elif method_call.startswith("fill("):
                    value = method_call[len("fill("):-1].strip("'\"")
                    element.fill(value)
                elif method_call == "text":
                    console.print(element.text)
                    return element.text
                # Add more methods here
                else:
                    console.print(f"[bold red]Unknown method: {method_call}[/bold red]")
                return
        
        # 'find' expression
        if expression.startswith("find "):
            selector = expression[len("find "):].strip()
            return self.find_element(selector)
            
        console.print(f"[bold red]Could not evaluate expression: {expression}[/bold red]")

    def find_element(self, selector: str) -> ElementHandler | None:
        if not browser_manager.page:
            console.print("[bold red]Browser not on a page. Use 'go <url>' first.[/bold red]")
            return None
        try:
            smart_selector = self._get_smart_locator(selector)
            locator = browser_manager.page.locator(smart_selector).first
            locator.wait_for(timeout=5000)
            return ElementHandler(locator, selector)
        except Exception as e:
            console.print(f"[bold red]Element not found for selector: '{selector}'[/bold red]")
            return None

    def _get_smart_locator(self, selector: str) -> str:
        selector = selector.strip()
        if selector.startswith('"') and selector.endswith('"'):
            return f'text={selector[1:-1]}'
        # More smart selector logic can be added here later
        return selector

    def handle_wait(self, args):
        if not args:
            console.print("[bold red]Usage: wait <duration> (e.g., 5s) or wait-for <selector>[/bold red]")
            return
        
        if args[0].endswith('s'):
            try:
                duration = float(args[0][:-1])
                console.print(f"Waiting for {duration} seconds...")
                time.sleep(duration)
                console.print("Done.")
            except ValueError:
                console.print("[bold red]Invalid duration.[/bold red]")
        elif args[0] == "for":
            selector = " ".join(args[1:])
            console.print(f"Waiting for element: '{selector}'...")
            element = self.find_element(selector)
            if element:
                console.print("Element found.")
        else:
            console.print("[bold red]Invalid wait command.[/bold red]")


    def print_help(self):
        console.print("""
[bold]Dyna-Automator Shell Commands:[/bold]
  [bold cyan]go <url>[/bold cyan]              - Navigate to a new URL.
  [bold cyan]find <selector>[/bold cyan]     - Find an element and print its representation.
  [bold cyan]let <var> = find ...[/bold cyan] - Store a found element in a variable.
  [bold cyan]<variable>.click()[/bold cyan]   - Click a stored element.
  [bold cyan]<variable>.fill("...")[/bold cyan] - Fill a stored element.
  [bold cyan]print(<variable>.text)[/bold cyan] - Print the text of a stored element.
  [bold cyan]wait <duration>[/bold cyan]       - Wait for a specific duration (e.g., '5s').
  [bold cyan]wait for <selector>[/bold cyan] - Wait for an element to appear.
  [bold cyan]help[/bold cyan]                  - Show this help message.
  [bold cyan]exit / quit[/bold cyan]           - Exit the shell.
        """)

@shell_app.command()
def launch(
    url: Annotated[str, typer.Argument(help="The initial URL to open.")] = None,
    headful: Annotated[bool, typer.Option("--headful", help="Run in non-headless mode.")] = False,
):
    """
    Launches the Dyna-Automator interactive shell.
    """
    shell = DynaShell()
    asyncio.run(shell.run(url, headful))

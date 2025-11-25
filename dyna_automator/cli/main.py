# dyna_automator/cli/main.py
import typer
from typing_extensions import Annotated
from rich.console import Console
from .. import __version__
from .shell import shell_app
from .commands import shot_cli, scrape_cli

# Initialize CLI
app = typer.Typer(
    name="dyna",
    help="[bold cyan]Dyna-Automator 2.0:[/bold cyan] An interactive web automation framework.",
    rich_markup_mode="rich",
)
console = Console()

def version_callback(value: bool):
    if value:
        console.print(f"Dyna-Automator Version: {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show the application version and exit.",
        ),
    ] = False,
):
    """
    Dyna-Automator: An interactive web automation framework.
    """
    pass

# Add the shell command
app.add_typer(shell_app, name="shell", help="Launch the interactive automation shell.")

# Add one-off commands
app.command("shot")(shot_cli)
app.command("scrape")(scrape_cli)

from ..scripting.runner import ScriptRunner

# ... (rest of the file is the same until the end)

# Add one-off commands
app.command("shot")(shot_cli)
app.command("scrape")(scrape_cli)

@app.command("run")
def run_script_cli(
    filepath: Annotated[str, typer.Argument(help="Path to the YAML script file.")],
    headful: Annotated[bool, typer.Option("--headful", help="Run in non-headless mode.")] = False,
):
    """
    Executes an automation workflow from a YAML script file.
    """
    runner = ScriptRunner(headless=not headful)
    runner.run_script(filepath)


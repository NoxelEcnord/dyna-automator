# dyna_automator/cli/commands.py
import typer
from typing_extensions import Annotated
from rich.console import Console
from ..browser_manager import BrowserManager

console = Console()
commands_app = typer.Typer()

@commands_app.command("shot")
def shot_cli(
    url: Annotated[str, typer.Argument(help="The URL of the page to screenshot.")],
    output: Annotated[str, typer.Option("--output", "-o", help="The output filename.")] = "screenshot.png",
    headful: Annotated[bool, typer.Option("--headful", help="Run in non-headless mode.")] = False,
    timeout: Annotated[int, typer.Option("--timeout", "-t", help="Page load timeout in seconds.")] = 60,
):
    """
    Captures a full-page screenshot of a URL.
    """
    browser = BrowserManager(headless=not headful)
    try:
        browser.start()
        browser.go_to(url, timeout=timeout * 1000)
        browser.screenshot(output)
    finally:
        browser.stop()

@commands_app.command("scrape")
def scrape_cli(
    url: Annotated[str, typer.Argument(help="The URL to scrape.")],
    selector: Annotated[str, typer.Option("--selector", "-s", help="The selector for the elements to scrape.")],
    output_file: Annotated[str, typer.Option("--output", "-o", help="File to save scraped content.")] = None,
    headful: Annotated[bool, typer.Option("--headful", help="Run in non-headless mode.")] = False,
    timeout: Annotated[int, typer.Option("--timeout", "-t", help="Page load timeout in seconds.")] = 60,
):
    """
    Extracts text content from elements on a dynamic page.
    """
    # This is a simplified implementation. It will be expanded with the ElementHandler later.
    browser = BrowserManager(headless=not headful)
    try:
        browser.start()
        browser.go_to(url, timeout=timeout * 1000)
        locators = browser.page.locator(selector).all()
        content_list = [loc.text_content() for loc in locators]

        if content_list:
            console.print(f"\n[bold underline]SCRAPED CONTENT ({len(content_list)} element(s)):[/bold underline]")
            full_content = ""
            for i, content in enumerate(content_list):
                line = f"Result {i+1}: {content.strip()}"
                console.print(f"[bold green]{line}[/bold green]")
                full_content += content.strip() + "\n"
            
            if output_file:
                with open(output_file, "w") as f:
                    f.write(full_content)
                console.print(f"\n[bold]Content saved to {output_file}[/bold]")

        else:
            console.print(f"[bold red]No content found for selector:[/bold red] {selector}")

    finally:
        browser.stop()

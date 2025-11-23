# dyna_automator/cli.py
import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.text import Text
from .core import DynamicBrowser

# Initialize CLI
app = typer.Typer(
    name="dyna",
    help="[bold cyan]Dyna-Automator:[/bold cyan] A modern, dynamic web automation CLI (by oxelEcnord).",
    rich_markup_mode="rich",
)
console = Console()

# Helper for selector documentation
SELECTOR_HELP = (
    "The selector for the element. Can be a CSS selector (e.g., #id), "
    "or human-readable text enclosed in quotes (e.g., \"Login button\"). "
    "Advanced users can use explicit selectors like role= or xpath=."
)

# --- COMMANDS ---

@app.command(name="open")
def open_url_cli(
    url: Annotated[str, typer.Argument(help="The full URL to open.")],
    show_html: Annotated[bool, typer.Option("--html", "-h", help="Print the full rendered HTML content.")] = False,
    headful: Annotated[bool, typer.Option("--headful", help="Run the browser with a visible window (for debugging).")] = False,
):
    """
    [bold yellow]Navigates[/bold yellow] to a URL, runs all JavaScript, and confirms page load.
    """
    with DynamicBrowser(headless=not headful) as browser: 
        browser.go_to(url)
        if show_html:
            console.print("\n[bold underline]RENDERED HTML CONTENT:[/bold underline]\n")
            console.print(Text(browser.get_html(), style="dim"))

@app.command(name="scrape")
def scrape_cli(
    url: Annotated[str, typer.Argument(help="The starting URL.")],
    selector: Annotated[str, typer.Option("--selector", "-s", help=SELECTOR_HELP)]
):
    """
    [bold yellow]Extracts[/bold yellow] text content from one or multiple elements on a dynamic page.
    """
    with DynamicBrowser() as browser:
        browser.go_to(url)
        
        content_list = browser.scrape_all(selector)
        
        if content_list:
            console.print(f"\n[bold underline]SCRAPED CONTENT ({len(content_list)} element(s)):[/bold underline]")
            for i, content in enumerate(content_list):
                console.print(f"[bold green]Result {i+1}:[/bold green] {content.strip()}")
        else:
            console.print(f"[bold red]Scraping complete, but no content found for selector:[/bold red] {selector}")

@app.command(name="interact")
def interact_cli(
    url: Annotated[str, typer.Argument(help="The starting URL.")],
    fill: Annotated[list[str], typer.Option("--fill", "-f", help=f"Field-value pair (e.g., 'input#name=John Doe' or '\"Username Field\"=John Doe'). {SELECTOR_HELP}")] = [],
    click_selector: Annotated[str, typer.Option("--click-selector", "-c", help=SELECTOR_HELP)] = "",
    screenshot_path: Annotated[str, typer.Option("--screenshot", "-ss", help="Path to save a screenshot after interaction (e.g., login_result.png).")] = "",
):
    """
    [bold yellow]Automates[/bold yellow] a sequence of user interactions (fill fields, click button) for login or form submission.
    """
    with DynamicBrowser() as browser:
        browser.go_to(url)

        # Handle multiple fill operations
        for fill_pair in fill:
            if '=' not in fill_pair:
                console.print(f"[bold red]Skipping invalid fill pair:[/bold red] '{fill_pair}'. Format is 'selector=value'.", style="dim")
                continue
            selector, value = fill_pair.split('=', 1)
            # Use the smart selector logic here
            browser.fill_field(selector.strip(), value.strip())

        if click_selector:
            browser.click_element(click_selector)

        if screenshot_path:
            browser.screenshot(screenshot_path)
            
@app.command(name="shot")
def shot_cli(
    url: Annotated[str, typer.Argument(help="The URL of the page to screenshot.")],
    output: Annotated[str, typer.Option("--output", "-o", help="The output filename for the screenshot (e.g., homepage.png).", default="screenshot.png")],
):
    """
    [bold yellow]Captures[/bold yellow] a full-page screenshot for visual debugging and verification.
    """
    with DynamicBrowser() as browser:
        browser.go_to(url)
        browser.screenshot(output)

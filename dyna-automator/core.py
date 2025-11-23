# dyna_automator/core.py
from playwright.sync_api import sync_playwright, Page, Locator
from rich.console import Console
import re

console = Console()

class DynamicBrowser:
    """
    Core class for dynamic web automation using Playwright.
    Handles browser state, navigation, element interaction, and data extraction.
    """
    def __init__(self, headless: bool = True):
        self.p = None
        self.browser = None
        self.context = None
        self.page: Page = None
        self.headless = headless

    # ... (Omitted __enter__ and __exit__ for brevity, they are unchanged) ...
    def __enter__(self):
        """Initializes the Playwright context and browser."""
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        console.print("[bold green]Browser initialized.[/bold green]")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the Playwright browser and context."""
        if self.browser:
            self.browser.close()
        if self.p:
            self.p.stop()
        console.print("[bold yellow]Browser closed.[/bold yellow]")


    def _get_smart_locator(self, selector: str) -> str:
        """
        Infers the best Playwright selector type (text, role, or CSS) from the input string.
        """
        selector = selector.strip()
        
        # 1. Direct Playwright Selector (Advanced/Explicit)
        if selector.startswith(("role=", "xpath=", "text=")):
            return selector

        # 2. Plain Text Selector (Human-readable)
        # If the input is wrapped in quotes, treat it as a literal text search.
        if selector.startswith('"') and selector.endswith('"'):
            # Use text= for exact match by visible text content
            return f'text={selector.strip(\'"\')}'
            
        # 3. CSS Selector (Default/Code-based)
        # If no explicit type or quote wrapping, treat as CSS.
        return selector

    def go_to(self, url: str):
        """Navigates to a URL and waits for the page to load all content (including JS)."""
        console.print(f"[bold blue]Navigating to:[/bold blue] {url}...")
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            console.print(f"[bold green]Current URL:[/bold green] {self.page.url}")
        except Exception as e:
            console.print(f"[bold red]Error opening URL:[/bold red] {e}")
            raise

    def scrape_all(self, selector: str) -> list[str]:
        """Extracts text content from all matching elements, waiting for the first one to appear."""
        smart_selector = self._get_smart_locator(selector)
        console.print(f"[bold yellow]Waiting for selector:[/bold yellow] {smart_selector}...")
        try:
            # Playwright automatically waits for the element determined by the smart selector
            elements = self.page.locator(smart_selector).all_text_contents()
            return elements
        except Exception as e:
            console.print(f"[bold red]Error scraping all:[/bold red] Selector '{selector}' failed. {e}")
            return []

    def fill_field(self, selector: str, value: str):
        """Fills a form field identified by a smart selector."""
        smart_selector = self._get_smart_locator(selector)
        console.print(f"[bold yellow]Filling field:[/bold yellow] {smart_selector} with value: '{value}'")
        try:
            self.page.fill(smart_selector, value)
            console.print("[bold green]Fill successful.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error filling form:[/bold red] Selector '{selector}' failed. {e}")
            raise

    def click_element(self, selector: str):
        """Clicks an element identified by a smart selector and waits for any network activity to settle."""
        smart_selector = self._get_smart_locator(selector)
        console.print(f"[bold yellow]Clicking element:[/bold yellow] {smart_selector}")
        try:
            self.page.click(smart_selector, timeout=30000)
            self.page.wait_for_load_state("domcontentloaded") 
            console.print(f"[bold green]Click successful. Current URL:[/bold green] {self.page.url}")
        except Exception as e:
            console.print(f"[bold red]Error clicking element:[/bold red] Selector '{selector}' failed. {e}")
            raise

    # ... (Omitted screenshot and get_html, they are unchanged) ...
    def screenshot(self, path: str):
        """Takes a full-page screenshot."""
        try:
            self.page.screenshot(path=path, full_page=True)
            console.print(f"[bold green]Screenshot saved to:[/bold green] {path}")
        except Exception as e:
            console.print(f"[bold red]Error taking screenshot:[/bold red] {e}")
            raise

    def get_html(self) -> str:
        """Returns the full rendered HTML content."""
        return self.page.content()

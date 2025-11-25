# dyna_automator/browser_manager.py
from playwright.sync_api import sync_playwright, Browser, Page, Playwright
from rich.console import Console

console = Console()

class BrowserManager:
    """
    Manages the Playwright browser instance, context, and page.
    This class is designed to be a singleton to ensure only one browser instance is active.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BrowserManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, headless: bool = True):
        self.p: Playwright | None = None
        self.browser: Browser | None = None
        self.page: Page | None = None
        self.headless = headless

    def start(self):
        """Starts the Playwright browser."""
        if not self.p:
            self.p = sync_playwright().start()
            self.browser = self.p.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()
            console.print("[bold green]Browser initialized.[/bold green]")

    def stop(self):
        """Stops the Playwright browser."""
        if self.browser:
            self.browser.close()
        if self.p:
            self.p.stop()
        self.p = None
        self.browser = None
        self.page = None
        console.print("[bold yellow]Browser closed.[/bold yellow]")

    def go_to(self, url: str, timeout: int = 60000):
        """Navigates to a URL."""
        if not self.page:
            self.start()
        
        console.print(f"[bold blue]Navigating to:[/bold blue] {url}...")
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            console.print(f"[bold green]Current URL:[/bold green] {self.page.url}")
        except Exception as e:
            console.print(f"[bold red]Error opening URL:[/bold red] {e}")
            raise

    def screenshot(self, path: str):
        """Takes a full-page screenshot."""
        if not self.page:
            console.print("[bold red]Browser not started. Cannot take screenshot.[/bold red]")
            return
        
        try:
            self.page.screenshot(path=path, full_page=True)
            console.print(f"[bold green]Screenshot saved to:[/bold green] {path}")
        except Exception as e:
            console.print(f"[bold red]Error taking screenshot:[/bold red] {e}")
            raise

browser_manager = BrowserManager()

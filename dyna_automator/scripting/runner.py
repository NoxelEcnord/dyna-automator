# dyna_automator/scripting/runner.py
import yaml
from rich.console import Console
from ..browser_manager import BrowserManager
from ..element_handler import ElementHandler
import time

console = Console()

class ScriptRunner:
    def __init__(self, headless: bool = True):
        self.browser = BrowserManager(headless=headless)
        self.variables = {}

    def run_script(self, filepath: str):
        console.print(f"[bold]Running script: {filepath}[/bold]")
        try:
            with open(filepath, 'r') as f:
                scripts = yaml.safe_load(f)
            
            self.browser.start()
            for script in scripts:
                self._execute_script_block(script)
        finally:
            self.browser.stop()
        console.print("[bold]Script execution finished.[/bold]")

    def _execute_script_block(self, script: dict):
        console.print(f"\n[bold underline]Executing block: {script.get('name', 'Unnamed')}[/bold underline]")
        steps = script.get("steps", [])
        for step in steps:
            self._execute_step(step)

    def _execute_step(self, step: dict | str):
        if isinstance(step, str):
            command = step
            args = {}
        else:
            command = list(step.keys())[0]
            args = step[command]

        console.print(f"  [yellow]Executing:[/yellow] {command}")

        if command == "go":
            self.browser.go_to(args)
        elif command == "shot":
            self.browser.screenshot(args)
        elif command == "wait":
            self._handle_wait(args)
        elif command == "fill":
            selector = args["selector"]
            value = args["value"]
            element = self._find_element(selector)
            if element:
                element.fill(value)
        elif command == "click":
            element = self._find_element(args)
            if element:
                element.click()
        elif command == "scrape":
            self._handle_scrape(args)
        else:
            console.print(f"  [bold red]Unknown command: {command}[/bold red]")

    def _find_element(self, selector: str) -> ElementHandler | None:
        try:
            locator = self.browser.page.locator(selector).first
            locator.wait_for(timeout=10000)
            return ElementHandler(locator, selector)
        except Exception:
            console.print(f"  [bold red]Element not found: {selector}[/bold red]")
            return None

    def _handle_wait(self, args: str | int):
        if isinstance(args, str) and args.endswith('s'):
            duration = float(args[:-1])
            console.print(f"  Waiting for {duration}s...")
            time.sleep(duration)
        else: # wait-for
            console.print(f"  Waiting for element: {args}...")
            self._find_element(args)

    def _handle_scrape(self, args: dict):
        selector = args["selector"]
        output_file = args.get("output_file")
        
        locators = self.browser.page.locator(selector).all()
        content_list = [loc.text_content().strip() for loc in locators]

        if content_list:
            console.print(f"  Scraped {len(content_list)} items.")
            if output_file:
                with open(output_file, 'w') as f:
                    f.write('\n'.join(content_list))
                console.print(f"  Content saved to {output_file}")
        else:
            console.print(f"  No content found for selector: {selector}")


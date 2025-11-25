# dyna_automator/element_handler.py
from __future__ import annotations
from typing import List
from playwright.sync_api import Locator
from rich.console import Console

console = Console()

class ElementHandler:
    """
    A wrapper around Playwright's Locator to provide a more intuitive,
    BeautifulSoup-like interface for interacting with web elements.
    """
    def __init__(self, locator: Locator, selector: str):
        self._locator = locator
        self._selector = selector

    def __repr__(self) -> str:
        try:
            tag = self._locator.evaluate('el => el.tagName.toLowerCase()')
            attributes = self._locator.evaluate('el => Array.from(el.attributes).map(attr => `${attr.name}="${attr.value}"`).join(" ")')
            return f"<{tag} {attributes}>"
        except Exception:
            return f"<Element found by '{self._selector}'>"

    @property
    def text(self) -> str:
        """Returns the text content of the element."""
        return self._locator.text_content()

    @property
    def html(self) -> str:
        """Returns the inner HTML of the element."""
        return self._locator.inner_html()

    def attr(self, name: str) -> str | None:
        """Returns the value of the specified attribute."""
        return self._locator.get_attribute(name)

    def click(self):
        """Clicks the element."""
        console.print(f"Clicking element: {self}")
        self._locator.click()

    def fill(self, value: str):
        """Fills a form field with the specified value."""
        console.print(f"Filling element: {self} with value: '{value}'")
        self._locator.fill(value)

    def screenshot(self, path: str):
        """Takes a screenshot of the element."""
        self._locator.screenshot(path=path)
        console.print(f"Screenshot of element {self} saved to: {path}")

    def find(self, selector: str) -> ElementHandler:
        """Finds a single descendant element matching the selector."""
        new_locator = self._locator.locator(selector).first
        return ElementHandler(new_locator, selector)

    def find_all(self, selector: str) -> List[ElementHandler]:
        """Finds all descendant elements matching the selector."""
        locators = self._locator.locator(selector).all()
        return [ElementHandler(loc, selector) for loc in locators]

    @property
    def parent(self) -> ElementHandler:
        """Returns the parent element."""
        parent_locator = self._locator.locator("..")
        return ElementHandler(parent_locator, self._selector + " -> parent")

    @property
    def children(self) -> List[ElementHandler]:
        """Returns a list of direct child elements."""
        # Note: This is a simplification. Playwright doesn't have a direct "children" selector.
        # We get all children and then filter. This might be slow on complex DOMs.
        child_locators = self._locator.locator("> *").all()
        return [ElementHandler(loc, self._selector + " -> child") for loc in child_locators]

# Dyna-Automator

<p align="center">
  <a href="https://github.com/NoxelEcnord/dyna-automator"><img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python" alt="Python"></a>
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/Engine-Playwright-brightgreen?style=for-the-badge&logo=playwright" alt="Playwright"></a>
  <a href="https://typer.tiangolo.com/"><img src="https://img.shields.io/badge/CLI-Typer-orange?style=for-the-badge&logo=typer" alt="Typer"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/NoxelEcnord/dyna-automator?style=for-the-badge" alt="License"></a>
</p>

## 🚀 Overview

**Dyna-Automator** is a modern, enterprise-grade Python framework designed for dynamic web automation and scraping. It replaces older, static tools by integrating **Playwright**—a modern browser automation library that natively handles JavaScript-rendered content (SPAs).

It offers a dual approach: a powerful **Command Line Interface (CLI)** for quick tasks and a modular **Python API** for deep integration into larger commercial projects.

**Key Features:**
* **Full JavaScript Support:** Renders pages and handles dynamic content like a real user.
* **Smart Selector Engine:** Allows element targeting using **CSS**, **HTML Roles**, or **Plain Visible Text**.
* **Unified CLI (`dyna`):** Simple, memorable commands for common tasks (`open`, `scrape`, `interact`, `shot`).
* **Resilient Automation:** Built on Playwright, ensuring stable interactions even when website structure changes.

## 🛠️ Installation and Setup

### Prerequisites

1.  **Python 3.8+**
2.  **Git**

### Steps

1.  **Clone the Repository (After Uploading to GitHub):**
    ```bash
    git clone [https://github.com/NoxelEcnord/dyna-automator.git](https://github.com/NoxelEcnord/dyna-automator.git)
    cd dyna-automator
    ```

2.  **Install Dependencies:**
    Using a virtual environment is highly recommended.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # Install the package and its dependencies (using pyproject.toml)
    pip install . 
    ```

3.  **Install Browser Drivers:**
    Playwright requires the actual browser binaries (Chromium, Firefox, WebKit) to function.
    ```bash
    playwright install
    ```

## ⌨️ Detailed CLI Usage (The `dyna` Commands)

The primary way to use the tool is via the installed `dyna` command.

### 🔍 Command: `dyna scrape`

Extracts text content from one or multiple elements.

| Option | Description | Example |
| :--- | :--- | :--- |
| `-s, --selector` | The selector to target the element(s). | `dyna scrape <URL> -s "h1.product-title"` |

**Example:** Scrape the main headline using visible text:
```bash
dyna scrape [https://example.com](https://example.com) -s "More Information..."

🖱️ Command: dyna interact

Performs a sequence of user interactions (fill fields, click button) for automation workflows.
Option	Description	Example Input
-f, --fill	Field-value pair for filling forms. Selector=Value.	-f "input#user=my_name" OR -f '"Username" = my_name'
-c, --click-selector	The selector for the button or link to click.	-c '"Log In Button"' OR -c "#submit-btn"
--screenshot	Path to save a screenshot after interaction.	--screenshot success.png

Example: Logging in using the human-readable text selector:
Bash

dyna interact [https://login.com](https://login.com) \
    -f '"Username Field" = NoxelEcnord' \
    -f '"Password Field" = mysecret' \
    -c '"Submit"' \
    --screenshot login_complete.png

🌐 Other Commands

Command	Function	Example Usage
dyna open <url>	Navigate to a URL. Add --html to see the full rendered source.	dyna open https://github.com/NoxelEcnord --html
dyna shot <url>	Take a full-page screenshot for visual verification.	dyna shot https://my-app.com -o visual_debug.png

💡 The Smart Selector Engine

This project uses an intelligent locator strategy to make your automation resilient. The DynamicBrowser automatically interprets your input:
Input Format	Engine Used	Example
CSS (Default)	Playwright CSS Engine	input[name="user"]
Plain Text (Wrapped in Quotes)	Playwright text= Engine	"Click Me Button"
Explicit Role (Accessibility)	Playwright role= Engine	role=button[name="Submit"]

Benefit: You can mix code-based selectors for highly unique elements (e.g., #user-id-52) with human-readable selectors for common buttons and links (e.g., "Sign Up Now").

📚 Learning Path: From CLI to API

The true commercial power lies in the Python API (dyna_automator.core.DynamicBrowser).

    Master the CLI: Use the dyna commands to quickly prototype and learn how to write resilient selectors.

    Transition to the API: Integrate the DynamicBrowser class into your own Python scripts for complex, multi-step automation jobs and data integration.

Python

from dyna_automator.core import DynamicBrowser

# Example: Using the API directly for a complex task
def run_product_search(term):
    with DynamicBrowser() as browser:
        browser.go_to("[https://search-engine.com](https://search-engine.com)")
        
        # Use Smart Selector for the search field and button
        browser.fill_field('"Search Input"', term) 
        browser.click_element('"Search Button"') 
        
        # Scrape results
        results = browser.scrape_all(".search-result-title")
        return results

print(run_product_search("new monitor"))

⚖️ License

This project is licensed under the MIT License.

Created by NoxelEcnord.

# Dyna-Automator 2.0

<p align="center">
  <img src="https://img.shields.io/badge/Dyna--Automator-v0.3.0-blueviolet?style=for-the-badge" alt="Version">
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/Engine-Playwright-brightgreen?style=for-the-badge&logo=playwright" alt="Playwright"></a>
  <a href="https://typer.tiangolo.com/"><img src="https://img.shields.io/badge/CLI-Typer-orange?style=for-the-badge&logo=typer" alt="Typer"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/NoxelEcnord/dyna-automator?style=for-the-badge" alt="License"></a>
</p>

## 🚀 A New Vision for Web Automation

**Dyna-Automator 2.0** is a complete reimagining of dynamic web automation. It transforms the original CLI wrapper into a powerful, interactive framework for browser control, scraping, and testing. It's designed for both rapid, exploratory tasks and complex, repeatable automation scripts.

**Core Features:**
*   **Interactive Shell (`dyna shell`):** Launch a persistent browser session and control it step-by-step. Perfect for debugging, exploring websites, and developing automation scripts live.
*   **Stateful Variables:** Find an element on a page and store it in a variable. Interact with it directly, access its properties (`.text`, `.html`), and traverse the DOM (`.parent`, `.children`) just like in BeautifulSoup.
*   **Powerful Wait Commands:** Explicitly wait for a duration (`wait 5s`) or for a specific element to appear (`wait-for #id`), eliminating flaky scripts.
*   **YAML-based Scripting (`dyna run`):** Define complex, multi-step automation workflows in simple, easy-to-read YAML files. Perfect for CI/CD and repeatable tasks.
*   **Modern Foundation:** Built on Playwright, Typer, and Rich for a best-in-class developer experience.

## 🛠️ Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/NoxelEcnord/dyna-automator.git
    cd dyna-automator
    ```

2.  **Install Dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install .
    ```

3.  **Install Browser Drivers:**
    ```bash
    playwright install
    ```

## ⌨️ Usage

### 🚀 Interactive Shell

The most powerful feature of Dyna-Automator 2.0. Launch the interactive shell with `dyna shell`.

```bash
$ dyna shell
Welcome to the Dyna-Automator Interactive Shell!
> go https://quotes.toscrape.com
Navigating to https://quotes.toscrape.com... Done.
> let first_quote = find ".quote"
Element stored in variable 'first_quote'.
> print(first_quote.text)
“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”
> let author = first_quote.find ".author"
Element stored in variable 'author'.
> print(author.text)
Albert Einstein
> wait 3s
Waiting for 3 seconds... Done.
> exit
```

### 📜 Automation Scripting

Create a YAML file (e.g., `scrape.yml`) and run it with `dyna run`.

```yaml
# scrape.yml
- name: Scrape authors from quotes.toscrape.com
  steps:
    - go: "https://quotes.toscrape.com"
    - wait-for: ".quote"
    - scrape:
        selector: ".author"
        output_file: "authors.txt"
    - shot: "final_page.png"
```

```bash
dyna run scrape.yml
```

### ⚡ Quick One-Off Commands

Simple commands for quick tasks are still available.

*   `dyna scrape <url> -s <selector>`: Scrape text from a URL.
*   `dyna shot <url> -o <filename>`: Take a screenshot of a URL.

---
Created with ❤️ by NoxelEcnord.

# tests/test_cli.py
from typer.testing import CliRunner
from dyna_automator.cli.main import app
import pytest

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Dyna-Automator Version: 0.3.0" in result.stdout

def test_shot_command_missing_url():
    result = runner.invoke(app, ["shot"])
    assert result.exit_code != 0  # Should fail as URL is a required argument
    assert "Missing argument 'URL'" in result.output

@pytest.mark.skip(reason="This test requires network and a live website, run manually.")
def test_shot_command():
    result = runner.invoke(app, ["shot", "https://example.com", "-o", "test.png"])
    assert result.exit_code == 0
    # In a real scenario, we would check if 'test.png' was created.
    # For now, we just check for successful execution.
    assert "Screenshot saved to: test.png" in result.stdout

@pytest.mark.skip(reason="This test requires network and a live website, run manually.")
def test_scrape_command():
    result = runner.invoke(app, ["scrape", "https://example.com", "-s", "h1"])
    assert result.exit_code == 0
    assert "SCRAPED CONTENT" in result.stdout
    assert "Example Domain" in result.stdout

def test_run_command_file_not_found():
    result = runner.invoke(app, ["run", "non_existent_script.yml"])
    assert result.exit_code != 0 # The script runner will raise an exception

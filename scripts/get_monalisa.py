import sys
import os
import time
from dyna_automator.browser_manager import browser_manager
from dyna_automator.element_handler import ElementHandler

# Add project root to path to allow imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Mechabrowser.py', 'dyna-automator'))
sys.path.insert(0, project_root)

def get_monalisa_screenshots():
    # Target directory
    output_dir = os.path.expanduser("~/dyna-automator")
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the browser manager
    browser_manager.headless = True # Run headless for this automation
    browser_manager.start()

    try:
        url = "https://www.google.com/search?q=Mona+Lisa+Leonardo+da+Vinci&tbm=isch"
        browser_manager.go_to(url)
        
        # Wait for thumbnails to be visible
        browser_manager.page.wait_for_selector("div.islir", timeout=10000)
        
        # Get all thumbnail locators
        thumbnails = browser_manager.page.locator("div.islir").all()
        
        if not thumbnails:
            print("No image thumbnails found on Google Images.")
            return

        print(f"Found {len(thumbnails)} image thumbnails. Capturing the first 10...")

        # Loop through the first 10 thumbnails
        for i, thumb_locator in enumerate(thumbnails[:10]):
            print(f"Processing image {i+1}...")
            try:
                # Click the thumbnail to open the full-size image preview
                thumb_locator.click()
                
                # Wait for the main preview image to appear
                # This selector was determined by inspecting Google Images
                preview_image_selector = 'img.sFlh5c.pT0Scc.iPVvYb'
                browser_manager.page.wait_for_selector(preview_image_selector, timeout=5000)
                
                # Get the locator for the main preview image
                preview_image_element = ElementHandler(browser_manager.page.locator(preview_image_selector).first, preview_image_selector)
                
                # Give it a moment to fully render
                time.sleep(1) 

                # Take screenshot of the element
                screenshot_path = os.path.join(output_dir, f"monalisa_{i+1}.png")
                preview_image_element.screenshot(screenshot_path)
                print(f"  Screenshot saved to {screenshot_path}")

            except Exception as e:
                print(f"  Could not process image {i+1}: {e}")
                # Continue to the next image if one fails
                continue

    finally:
        browser_manager.stop()

if __name__ == "__main__":
    get_monalisa_screenshots()

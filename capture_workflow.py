from playwright.sync_api import sync_playwright
import os

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 800, "height": 1000})
        page.goto(f"file://{os.path.abspath('workflow.html')}")
        page.wait_for_timeout(3000)
        # We find the svg element
        locator = page.locator('svg')
        locator.screenshot(path="workflow_diagram.png")
        browser.close()

if __name__ == '__main__':
    capture()

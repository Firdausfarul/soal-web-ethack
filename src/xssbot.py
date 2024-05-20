from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller

def visit_report(url):
    options = Options()
    # Comment out headless option to run in a regular browser window
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('disable-infobars')
    options.add_argument('disable-background-networking')
    options.add_argument('disable-default-apps')
    options.add_argument('disable-extensions')
    options.add_argument('disable-gpu')
    options.add_argument('disable-sync')
    options.add_argument('disable-translate')
    options.add_argument('hide-scrollbars')
    options.add_argument('metrics-recording-only')
    options.add_argument('mute-audio')
    options.add_argument('no-first-run')
    options.add_argument('dns-prefetch-disable')
    options.add_argument('safebrowsing-disable-auto-update')
    options.add_argument('media-cache-size=1')
    options.add_argument('disk-cache-size=1')
    options.add_argument('user-agent=BugHTB/1.0')
    # Initialize the Chrome browser
    browser = webdriver.Chrome(options=options)

    try:
        # Open initial URL
        browser.get(url)

        # Add a cookie to the browser
        browser.add_cookie({
            'name': 'flag',
            'value': 'Fada{f4k3_fl4g_f0r_t3st1ng}',
        })

        # Visit the target URL
        browser.get(url)

        # Wait until the page is fully loaded
        WebDriverWait(browser, 5).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )

        # Additional logging to verify JavaScript execution
        result = browser.execute_script('return document.body.innerHTML')
        print("Page content:", result)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        browser.quit()


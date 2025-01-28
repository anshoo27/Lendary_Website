import json
import os
import logging
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# Setup directories
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
REPORTS_DIR = BASE_DIR / "reports"
os.environ["BROWSERSTACK_USERNAME"] = "ashishsharma_DYPVeW"
os.environ["BROWSERSTACK_ACCESS_KEY"] = "bhAtALSiW9TuNts"
# Create directories if they don't exist
for directory in [LOGS_DIR, SCREENSHOTS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LendaryLoginTest:
    def __init__(self):
        self.driver = None
        self.test_status = "failed"
        self.test_message = ""

    def setup_driver(self):
        """Setup WebDriver with BrowserStack capabilities"""
        try:
            options = Options()
            
            # BrowserStack capabilities
            browserstack_options = {
                'browserName': 'Chrome',
                'browserVersion': 'latest',
                'os': 'Windows',
                'os_version': '10',
                'name': 'Lendary Login Test',
                'build': os.getenv('GITHUB_SHA', 'local_build'),
                'browserstack.local': 'true',  # Enable for local testing
                'browserstack.debug': 'true',
                'browserstack.networkLogs': 'true',
                'browserstack.console': 'verbose'
            }
            
            # Set capabilities
            options.set_capability('bstack:options', browserstack_options)
            
            # Get BrowserStack credentials
            username = os.getenv('BROWSERSTACK_USERNAME')
            access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')
            
            if not username or not access_key:
                raise ValueError("BrowserStack credentials not found in environment variables")
            
            self.driver = webdriver.Remote(
                command_executor=f'https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub',
                options=options
            )
            logger.info("WebDriver setup successful")
            
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {str(e)}")
            raise

    def take_screenshot(self, name):
        """Take screenshot and save it"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = SCREENSHOTS_DIR / f"{name}_{timestamp}.png"
            self.driver.save_screenshot(str(filename))
            logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")

    def perform_login(self):
        """Perform login operation"""
        try:
            # Navigate to login page
            self.driver.get('https://stage-admin.lendary.xyz/login')
            logger.info("Navigated to login page")
            
            # Wait for page title
            WebDriverWait(self.driver, 10).until(EC.title_contains('Lendary Asia'))
            
            # Find and fill login form
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'email'))
            )
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/form/div[3]/button')
                )
            )
            
            # Get credentials from environment variables
            email = os.getenv('LENDARY_EMAIL', 'admin@lendary.com')
            password = os.getenv('LENDARY_PASSWORD', 'Admin@123')
            
            username_field.send_keys(email)
            password_field.send_keys(password)
            self.take_screenshot('before_login')
            login_button.click()
            logger.info("Login credentials entered and submitted")
            
            # Verify login success
            WebDriverWait(self.driver, 10).until(EC.url_contains('/dashboard'))
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'style_header__FA-9C'))
            )
            self.take_screenshot('after_login')
            
            self.test_status = "passed"
            self.test_message = "Successfully logged in and verified the landing page!"
            logger.info("Login successful")
            
        except Exception as e:
            self.test_status = "failed"
            self.test_message = f"Login failed: {str(e)}"
            logger.error(f"Login failed: {str(e)}")
            self.take_screenshot('login_error')
            raise

    def update_test_status(self):
        """Update test status on BrowserStack"""
        try:
            self.driver.execute_script(
                f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"{self.test_status}", "reason": "{self.test_message}"}}}}'
            )
        except Exception as e:
            logger.error(f"Failed to update test status: {str(e)}")

    def run(self):
        """Run the complete test"""
        try:
            self.setup_driver()
            self.perform_login()
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
        finally:
            if self.driver:
                self.update_test_status()
                self.driver.quit()
                logger.info("WebDriver session ended")

def main():
    """Main function to run the test"""
    test = LendaryLoginTest()
    test.run()

if __name__ == "__main__":
    main()
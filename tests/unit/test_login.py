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
from dotenv import load_dotenv
import warnings

# Suppress warnings about embedding credentials in the URL
warnings.filterwarnings("ignore", category=UserWarning, module="selenium.webdriver.remote.remote_connection")

# Load environment variables
load_dotenv()

# Setup directories (Absolute paths)
BASE_DIR = Path(__file__).parent
LOGS_DIR = Path("/data/Lendary/Lendary_Website/logs")
SCREENSHOTS_DIR = Path("/data/Lendary/Lendary_Website/screenshots")
REPORTS_DIR = Path("/data/Lendary/Lendary_Website/reports")

# Create directories if they *don't* exist
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
            options.set_capability('browserName', 'Chrome')
            options.set_capability('browserVersion', 'latest')
            options.set_capability('platformName', 'Windows')
            options.set_capability('platformVersion', '10')
            options.set_capability('bstack:options', {
                'local': 'false',  # Disable BrowserStack Local
                'debug': 'true',
                'networkLogs': 'true',
                'consoleLogs': 'verbose'
            })
            
            # Get BrowserStack credentials from environment variables
            username = os.environ.get('BROWSERSTACK_USERNAME')
            access_key = os.environ.get('BROWSERSTACK_ACCESS_KEY')
            
            if not username or not access_key:
                raise ValueError("BrowserStack credentials not found in environment variables")
            
            # Initialize WebDriver with BrowserStack
            self.driver = webdriver.Remote(
                command_executor=f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub",
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
            
            # Wait for page title (adjust timeout if needed)
            WebDriverWait(self.driver, 20).until(EC.title_contains('Lendary Asia'))
            
            # Find and fill login form (adjust timeouts as needed)
            username_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, 'email'))
            )
            password_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            login_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/form/div[3]/button')
                )
            )
            
            # Get credentials from environment variables (or use defaults)
            email = os.environ.get('LENDARY_EMAIL', 'admin@lendary.com')
            password = os.environ.get('LENDARY_PASSWORD', 'Admin@123')
            
            username_field.send_keys(email)
            password_field.send_keys(password)
            self.take_screenshot('before_login')
            login_button.click()
            logger.info("Login credentials entered and submitted")
            
            # Verify login success (adjust timeouts and conditions as needed)
            WebDriverWait(self.driver, 20).until(EC.url_contains('/dashboard'))
            # Replace with a more robust locator if possible
            WebDriverWait(self.driver, 20).until(
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
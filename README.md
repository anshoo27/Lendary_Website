# **Selenium Python Browserstack Login Test Automation**

This project automates the login functionality of the Lendary application using Selenium and BrowserStack. It includes comprehensive logging, screenshot capture, and BrowserStack integration for cross-browser testing.

---

## **Table of Contents**
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
4. [Configuration](#configuration)
5. [Running the Tests](#running-the-tests)
6. [Logs and Screenshots](#logs-and-screenshots)
7. [BrowserStack Integration](#browserstack-integration)
8. [Contributing](#contributing)
9. [License](#license)

---

## **Features**
- **Automated Login Testing**: Tests the login functionality of the Lendary application.
- **Cross-Browser Testing**: Runs tests on BrowserStack for multiple browsers and platforms.
- **Comprehensive Logging**: Logs test execution details for debugging and monitoring.
- **Screenshot Capture**: Captures screenshots before and after login, as well as on failure.
- **Environment Variables**: Securely manages sensitive data like credentials.
- **Headless Mode Support**: Allows running tests in headless mode for faster execution in CI/CD pipelines.

---

## **Prerequisites**
Before running the tests, ensure you have the following installed:
- **Python 3.10 or higher**
- **pip** (Python package manager)
- **BrowserStack Account**: Sign up at [BrowserStack](https://www.browserstack.com/) and obtain your `username` and `access_key`.

---

## **Setup**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/Lendary_Website.git
   cd Lendary_Website
Create a Virtual Environment (optional but recommended):

bash
Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Configuration
Environment Variables:
Create a .env file in the root directory and add the following variables:

plaintext
Copy
BROWSERSTACK_USERNAME=your_browserstack_username
BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
LENDARY_EMAIL=your_lendary_email
LENDARY_PASSWORD=your_lendary_password
Replace your_browserstack_username and your_browserstack_access_key with your BrowserStack credentials.

Replace your_lendary_email and your_lendary_password with your Lendary login credentials.

Optional Variables:

HEADLESS=true: Set to true to run the browser in headless mode.

LOG_LEVEL=DEBUG: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

Running the Tests
To run the login test:

bash
Copy
python tests/unit/test_login.py
Running in Headless Mode
To run the test in headless mode:

bash
Copy
export HEADLESS=true
python tests/unit/test_login.py
Logs and Screenshots
Logs: Logs are saved in the logs/ directory with a timestamped filename (e.g., test_20231015_123456.log).

Screenshots: Screenshots are saved in the screenshots/ directory with descriptive names (e.g., before_login_20231015_123456.png).

BrowserStack Integration
This project integrates with BrowserStack for cross-browser testing. To use BrowserStack:

Update the setup_driver method in test_login.py with your desired browser and platform capabilities.

Ensure your BrowserStack credentials are set in the .env file.

Updating Test Status
The test status is automatically updated on BrowserStack using the update_test_status method. This includes:

Status: passed or failed.

Reason: A brief description of the test outcome.

Contributing
Contributions are welcome! If you'd like to contribute:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/your-feature-name).

Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Selenium for browser automation.

BrowserStack for cross-browser testing.

Python for making this project possible.

Contact
For questions or feedback, please contact:

Your Name: Anshoo

Project Repository: Lendary_Website
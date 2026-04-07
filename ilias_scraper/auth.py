import requests
import time
from selenium import webdriver

def get_ilias_session():
    LOGIN_URL = "https://ilias.uni-konstanz.de/login.php?client_id=ILIASKONSTANZ&cmd=force_login&lang=de"

    print("Starting browser...")
    driver = webdriver.Chrome()
    driver.get(LOGIN_URL)

    print("Browser is open! Please type your credentials into the Chrome window.")
    print("Waiting for you to log in... (I will automatically detect when you are done)")

    timeout = 120 
    elapsed = 0

    # Watch the URL to see when you finish logging in
    while "login.php" in driver.current_url and elapsed < timeout:
        time.sleep(2)
        elapsed += 2

    if "login.php" in driver.current_url:
        print("❌ Timeout! You didn't log in within 2 minutes.")
        driver.quit()
        return None
    else:
        print("✅ Login detected! Securing cookies...")
        time.sleep(3) # Give the dashboard 3 seconds to fully load
        
        user_agent = driver.execute_script("return navigator.userAgent;")
        selenium_cookies = driver.get_cookies()

        session = requests.Session()
        session.headers.update({'User-Agent': user_agent})

        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        print("Cookies successfully transferred! Closing Chrome...")
        driver.quit()

        return session
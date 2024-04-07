from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver(path):
# Set the path to your Chrome profile
    # Set up Chrome options
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_argument("--headless")
    options.add_argument("--disable-popup-blocking")
    options.add_argument(f"--user-data-dir=/home/shubharthak/snap/chromium/common/chromium/")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-plugins-discovery")
    if path:
        service = Service(path)
    else:
        service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print('Driver initialized...')
    return driver

def get_views_selenium(driver, url, debug=False):
    if debug:
        print(url)
    driver.get(url)
    print(driver.title)
    #Locate the element containing the view count
    view_count_element = driver.find_element(By.XPATH, '//*[@id="react-target"]/div/div[6]/div/div[2]/div[1]/div[2]/div[3]/div[1]')
    # Extract the text content
    view_count_text = view_count_element.text
    # Print the text for debug
    if debug:
        print(view_count_text)
    # Clean and format the view count
    view_count = int(view_count_text.split()[0].replace(",", ""))
    if debug:
        print(f"Number of views: {view_count:,}")
    return view_count

if __name__ == '__main__':
    pass
    


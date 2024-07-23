# TABGRAB4.PY
# uses Selinium's WebDriver, which has been described to me as
# "a bit of a pain, to put it midly"

# Connects to my Firefox instance
# iterates through all open tabs
# prints the title and URL of each tab

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

def get_tab_info():
    # Set up Firefox options
    options = Options()
    options.add_argument("-profile")
    options.add_argument(r"C:\Users\Cal\AppData\Roaming\Mozilla\Firefox\Profiles\m76qq8d6.default-release")

    # Specify the Firefox binary path explicitly
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Adjust this path as needed

    # Set up the service with the connect-existing argument
    service = Service(executable_path=r'C:\Drivers\geckodriver.exe', service_args=['--connect-existing'])

    # Connect to the existing Firefox instance
    driver = webdriver.Firefox(options=options, service=service)
    
    # Get all tab handles
    tabs = driver.window_handles
    
    for tab in tabs:
        driver.switch_to.window(tab)
        print(f"Title: {driver.title}")
        print(f"URL: {driver.current_url}")
        print("---")
    
    # Don't quit the driver, as we're using an existing instance
    # driver.quit()

if __name__ == "__main__":
    get_tab_info()
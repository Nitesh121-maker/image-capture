import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("Enter Country:")
x = input()
url = "https://www.tradeimex.in/{}-import".format(x.lower())
print("Modified URL:", url)

# Function to take a screenshot of a specific element on a webpage
def take_element_screenshot(url, output_filename):
    # Setup Chrome WebDriver
    driver = webdriver.Chrome()
    
    try:
        # Open the URL
        driver.get(url)
        
        # Wait until the sample div is visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "sample")))
        
        # Find the sample div
        sample_div = driver.find_element(By.ID, "sample")

        # Find the col-6 div within the sample div
        col_6_div = sample_div.find_element(By.CLASS_NAME, "col-lg-6")

        # Find the table within the col-6 div
        table = col_6_div.find_element(By.CLASS_NAME, "table")

        # Take a screenshot of the table
        table.screenshot(output_filename)
        print("Screenshot saved as:", output_filename)
        
    finally:
        # Quit the WebDriver
        driver.quit()

# Take a screenshot of the table inside the "col-6" div on the webpage
output_filename = "{}-import-sample-col-6-table-screenshot.png".format(x.lower())
take_element_screenshot(url, output_filename)

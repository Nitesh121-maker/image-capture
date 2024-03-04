import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def take_element_screenshot(url, output_filename):
    driver = webdriver.Chrome()
    
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "sample")))
        
        sample_div = driver.find_element(By.ID, "sample")
        col_12_divs = sample_div.find_elements(By.CLASS_NAME, "col-lg-12")
        col_12_div = col_12_divs[1] if len(col_12_divs) >= 2 else None
        
        if col_12_div:
            col_6_divs = col_12_div.find_elements(By.CLASS_NAME, "col-lg-6")
            col_6_div = col_6_divs[1] if len(col_12_divs) >= 2 else None
            try:
                table = col_6_div.find_element(By.CLASS_NAME, "table")
                table.screenshot(output_filename)
                print("Screenshot saved as:", output_filename)
            except:
                print("Table not found inside col-lg-6 div.")
        else:
            col_6_div = sample_div.find_element(By.CLASS_NAME, "col-lg-6")
            table = col_6_div.find_element(By.CLASS_NAME, "table")
            table.screenshot(output_filename)
            print("Screenshot saved as:", output_filename)
    finally:
        driver.quit()
        uploadscreenshot(output_filename,datatype)

def uploadscreenshot(output_filename,datatype):
    url = "http://192.168.1.5:8000/country_alldata"
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "alldatamain")))
        if datatype == 'import':
            import_country_elements = driver.find_elements(By.XPATH, f"//td[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{x.lower()}']")
            # country_elements = driver.find_elements(By.XPATH, f"//td[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{x.lower()}']")
            country_element = import_country_elements[0] if len(import_country_elements) >= 2 else None
            if country_element:
                parent_form = country_element.find_element(By.XPATH, "..")
                edit_button = parent_form.find_element(By.XPATH, ".//button[@class='edit-button']")
                edit_button.click()
                
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sample_data_btn")))
                sample_data_btn = driver.find_element(By.CLASS_NAME, "sample_data_btn")
                sample_data_btn.click()
                
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "slider_images_one")))
                file_input = driver.find_element(By.NAME, "slider_images_one")
                
                # Get the absolute path of the file
                abs_output_filename = os.path.abspath(output_filename)
                file_input.send_keys(abs_output_filename)
                
                submit_button = driver.find_element(By.CLASS_NAME, "formsubmission")
                submit_button.click()
                time.sleep(5)
                print("Data uploaded successfully in import!")
                
        elif datatype == 'export':
            export_country_elements = driver.find_elements(By.XPATH, f"//td[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{x.lower()}']")
            print(len(export_country_elements))
            country_element = export_country_elements[1] if len(export_country_elements) >= 2 else None
            print('country_element',export_country_elements[1].text)

            if country_element:
                parent_form = country_element.find_element(By.XPATH, "..")
                edit_button = parent_form.find_element(By.XPATH, ".//button[@class='edit-button']")
                edit_button.click()
                
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sample_data_btn")))
                sample_data_btn = driver.find_element(By.CLASS_NAME, "sample_data_btn")
                sample_data_btn.click()
                
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "slider_images_one")))
                file_input = driver.find_element(By.NAME, "slider_images_one")
                
                # Get the absolute path of the file
                abs_output_filename = os.path.abspath(output_filename)
                file_input.send_keys(abs_output_filename)
                
                submit_button = driver.find_element(By.CLASS_NAME, "formsubmission")
                submit_button.click()
                print("Data uploaded successfully in export!")
                time.sleep(10)
        else:
            print("Both are not working")
    except Exception as e:
        print("Error:", e)

x = input("Enter Country: ")
datatype = input("Enter Datatype: ")
url = "https://www.tradeimex.in/{}-{}".format(x.lower(), datatype.lower())
print("Modified URL:", url)

output_filename = "{}-{}-table-screenshot.png".format(x.lower(), datatype.lower())
take_element_screenshot(url, output_filename)

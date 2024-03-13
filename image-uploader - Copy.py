import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def take_element_screenshot(url, output_filename):
    start_time = time.time()
    driver = webdriver.Chrome()
    
    try:
        driver.get(url)

        sample_div = None
        stats_sample_div = None

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "sample")))
            sample_div = driver.find_element(By.ID, "sample")
        except:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "stats-sample")))
                stats_sample_div = driver.find_element(By.ID, "stats-sample")
            except:
                pass

        if sample_div:
            container_id = "sample"
        elif stats_sample_div:
            container_id = "stats-sample"
        else:
            print("No container with id 'sample' or 'stats-sample' found on the page.")
            return

        print('container_id',container_id)
        container_div = driver.find_element(By.ID, container_id)
        col_12_divs = container_div.find_elements(By.CLASS_NAME, "col-lg-12")
        col_12_div = col_12_divs[1] if len(col_12_divs) >= 2 else None
        col_6_divs = container_div.find_elements(By.CLASS_NAME, "col-lg-6")
        
        if col_12_div:
            col_6_divs = col_12_div.find_elements(By.CLASS_NAME, "col-lg-6")
            col_6_div = col_6_divs[1] if len(col_6_divs) >= 2 else None
            try:
                table = col_6_div.find_element(By.CLASS_NAME, "table")
                # Adjust the window size to a square form
                driver.set_window_size(800, 800)
                table.screenshot(output_filename)
                print("Screenshot saved as:", output_filename)
            except:
                print("Table not found inside col-lg-6 div.")
        elif col_6_divs:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, container_id)))
            if len(col_6_divs) >= 2:
                try:
                    col_6_div = col_6_divs[1] if len(col_6_divs) >= 2 else None
                    table = col_6_div.find_element(By.CLASS_NAME, "table")
                    # Adjust the window size to a square form
                    driver.set_window_size(800, 800)
                    table.screenshot(output_filename)
                    print("Screenshot saved as:", output_filename)
                except:
                    print("Table not found inside col-lg-6 div or col-lg-6 divs are not found.")
            else:
                print("Entered in else")
                try:
                    # Find the container div
                    container_div = driver.find_element(By.ID, container_id)
                    
                    # Find the col-lg-6 div
                    col_6_lg_div = container_div.find_elements(By.CLASS_NAME, "col-lg-6")
                    
                    # Check if col-lg-6 div is found
                    if col_6_lg_div:
                        # Assuming col-lg-6 div has only one element
                        col_6_lg_div = col_6_lg_div[0]
                        
                        try:
                            # Find the table element
                            table_element = col_6_lg_div.find_element(By.CLASS_NAME, "table")
                            
                            # Adjust the window size to a square form
                            driver.set_window_size(800, 800)
                            # Take screenshot of the table
                            table_element.screenshot(output_filename)
                            print("Screenshot saved as:", output_filename)
                        
                        except :
                            print("Table not found inside col-lg-6 div.")
                    
                    else:
                        print("No col-lg-6 div found inside container div.")
                except :
                    print("Container div not found.")   
        else:
            print(f"No divs with id '{container_id}' or class name 'col-lg-12' were found on the page.")
    finally:
        driver.quit()
        uploadscreenshot(output_filename, datatype)
        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time:", execution_time)



def uploadscreenshot(output_filename,datatype):
    url = "http://192.168.1.7:8000/country_alldata"
    uploaddriver = webdriver.Chrome()
    try:
        uploaddriver.get(url)
        WebDriverWait(uploaddriver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "alldatamain")))
        if datatype == 'import':
            import_country_elements = uploaddriver.find_elements(By.XPATH, f"//td[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{x.lower()}']")
            # country_elements = uploaddriver.find_elements(By.XPATH, f"//td[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{x.lower()}']")
            country_element = import_country_elements[0] if len(import_country_elements) >= 2 else None
            if country_element:
                parent_form = country_element.find_element(By.XPATH, "..")
                edit_button = parent_form.find_element(By.XPATH, ".//button[@class='edit-button']")
                edit_button.click()
                
                WebDriverWait(uploaddriver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "sample_data_btn")))
                sample_data_btn = uploaddriver.find_element(By.CLASS_NAME, "sample_data_btn")
                sample_data_btn.click()
                
                WebDriverWait(uploaddriver, 5).until(EC.visibility_of_element_located((By.NAME, "slider_images_one")))
                file_input = uploaddriver.find_element(By.NAME, "slider_images_one")
                
                # Get the absolute path of the file
                abs_output_filename = os.path.abspath(output_filename)
                file_input.send_keys(abs_output_filename)
                
                submit_button = uploaddriver.find_element(By.CLASS_NAME, "formsubmission")
                submit_button.click()
                time.sleep(2)
                print("Data uploaded successfully in import!")
                
        elif datatype == 'export':
            export_country_elements = uploaddriver.find_elements(By.XPATH, f"//td[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{x.lower()}']")
            print(len(export_country_elements))
            country_element = export_country_elements[1] if len(export_country_elements) >= 2 else None
            print('country_element',export_country_elements[1].text)

            if country_element:
                parent_form = country_element.find_element(By.XPATH, "..")
                edit_button = parent_form.find_element(By.XPATH, ".//button[@class='edit-button']")
                edit_button.click()
                
                WebDriverWait(uploaddriver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "sample_data_btn")))
                sample_data_btn = uploaddriver.find_element(By.CLASS_NAME, "sample_data_btn")
                sample_data_btn.click()
                
                WebDriverWait(uploaddriver, 5).until(EC.visibility_of_element_located((By.NAME, "slider_images_one")))
                file_input = uploaddriver.find_element(By.NAME, "slider_images_one")
                
                # Get the absolute path of the file
                abs_output_filename = os.path.abspath(output_filename)
                file_input.send_keys(abs_output_filename)
                
                submit_button = uploaddriver.find_element(By.CLASS_NAME, "formsubmission")
                submit_button.click()
                print("Data uploaded successfully in export!")
              
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

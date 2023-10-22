# import time
#
# import cv2
# from pyzbar.pyzbar import decode
# from selenium import webdriver
# from selenium.common import NoSuchElementException
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from prettytable import PrettyTable
# import os
#
# image_directory = "images"
#
# options = Options()
# options.add_experimental_option("detach", True)
#
#
# def BarcodeReader(image):
#     img = cv2.imread(image)
#     detectedBarcodes = decode(img)
#
#     if not detectedBarcodes:
#         print("Barcode Not Detected or your barcode is blank/corrupted!")
#     else:
#         for barcode in detectedBarcodes:
#             (x, y, w, h) = barcode.rect
#             cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 0, 0), 2)
#
#             if barcode.data != "":
#                 split_code = str(barcode.data).split("'")[1]
#                 print(f"Item {counter}: Barcode.data : {split_code}")
#
#                 driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#                 driver.get("https://barcode-list.com/")
#                 driver.maximize_window()
#
#                 form = driver.find_element(by=By.XPATH, value="//input[@id='barcodeSearchField']")
#                 form.click()
#                 form.send_keys(f"{split_code}")
#                 search = driver.find_element(by=By.XPATH, value="//input[@id='barcodeSearchButton']")
#                 search.click()
#                 time.sleep(3)
#                 try:
#                     table = driver.find_element(by=By.XPATH, value="//table[@class='randomBarcodes']")
#                     table_rows = table.find_elements(by=By.TAG_NAME, value="tr")  # Find all table rows
#                     data = []
#
#                     tic = 0
#                     for row in table_rows:
#                         row_data = row.find_elements(by=By.TAG_NAME, value="td")  # Find the cells in each row
#                         row_values = [cell.text for cell in row_data]
#                         data.append(row_values)
#                         tic += 1
#                         if tic > 1:
#                             break
#
#                     driver.quit()
#
#                     return data[1:]  # Return the data for this image
#                 except NoSuchElementException:
#                     print(f"***  Item {counter}: {split_code} :No available data  ***")
#                     driver.quit()
#
#
# if __name__ == "__main__":
#     counter = 1
#     combined_table = PrettyTable(["-", "Barcode", "Product Name", "Measure", "Rating"])
#
#     for filename in os.listdir(image_directory):
#         if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
#             image_path = os.path.join(image_directory, filename)
#             image_data = BarcodeReader(image_path)
#             if image_data:
#                 for row in image_data:
#                     combined_table.add_row(row)
#             counter += 1
#
#     combined_table.align = "l"
#     combined_table.border = True
#     combined_table.header = True
#     combined_table.title = "Product Table"
#     print(combined_table)
import time
import cv2
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from prettytable import PrettyTable
import os

image_directory = "images"

options = Options()
options.add_experimental_option("detach", True)

def BarcodeReader(image):
    img = cv2.imread(image)
    detectedBarcodes = decode(img)

    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:
        for barcode in detectedBarcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 0, 0), 2)

            if barcode.data != "":
                split_code = str(barcode.data).split("'")[1]
                print(f"Item {counter}: Barcode.data : {split_code}")

                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                driver.get("https://barcode-list.com/")
                driver.maximize_window()

                form = driver.find_element(by=By.XPATH, value="//input[@id='barcodeSearchField']")
                form.click()
                form.send_keys(f"{split_code}")
                search = driver.find_element(by=By.XPATH, value="//input[@id='barcodeSearchButton']")
                search.click()
                time.sleep(3)
                try:
                    table = driver.find_element(by=By.XPATH, value="//table[@class='randomBarcodes']")
                    table_rows = table.find_elements(by=By.TAG_NAME, value="tr")  # Find all table rows
                    data = []

                    tic = 0
                    for row in table_rows:
                        row_data = row.find_elements(by=By.TAG_NAME, value="td")  # Find the cells in each row
                        row_values = [cell.text for cell in row_data]
                        data.append(row_values)
                        tic += 1
                        if tic > 1:
                            break

                    driver.quit()

                    return data[1:]  # Return the data for this image
                except NoSuchElementException:
                    print(f"***  Item {counter}: {split_code} :No available data  ***")
                    driver.quit()

if __name__ == "__main__":
    counter = 1
    combined_table = PrettyTable(["Barcode", "Product Name"])

    for filename in os.listdir(image_directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(image_directory, filename)
            image_data = BarcodeReader(image_path)
            if image_data:
                for row in image_data:
                    # Include only the "Barcode" and "Product Name" columns
                    combined_table.add_row([row[1], row[2]])
            counter += 1

    combined_table.align = "l"
    combined_table.border = True
    combined_table.header = True
    combined_table.title = "Product Table"
    print(combined_table)

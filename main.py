import cv2
from pyzbar.pyzbar import decode
from selenium import webdriver
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

            cv2.rectangle(img, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (255, 0, 0), 2)

            if barcode.data != "":
                split_code = str(barcode.data).split("'")[1]
                print(f"Item {counter}: Barcode.data : {split_code}")
                # print(f"Barcode.type : {barcode.type}")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                driver.get("https://barcode-list.com/")
                driver.maximize_window()

                form = driver.find_element(by=By.XPATH, value="//input[@id='barcodeSearchField']")
                form.click()
                form.send_keys(f"{split_code}")
                search = driver.find_element(by=By.XPATH, value="//input[@id='barcodeSearchButton']")
                search.click()

                # time.sleep(3)
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

                column_headers = ["ID", "Barcode", "Product Name", "Measure", "Rating"]

                table = PrettyTable(column_headers)

                for row in data[1:]:
                    table.add_row(row)
                table.align = "l"
                table.border = True
                table.header = True
                table.title = f"Barcode : {split_code}"
                print(table)
                driver.quit()


if __name__ == "__main__":
    counter = 1
    for filename in os.listdir(image_directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(image_directory, filename)
            BarcodeReader(image_path)
            counter += 1

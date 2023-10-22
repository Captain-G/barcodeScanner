# Importing library
import time

import cv2
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from prettytable import PrettyTable

options = Options()
options.add_experimental_option("detach", True)


# Make one method to decode the barcode
def BarcodeReader(image):
    # read the image in numpy array using cv2
    img = cv2.imread(image)

    # Decode the barcode image
    detectedBarcodes = decode(img)

    # If not detected then print the message
    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:

        # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes:

            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect

            # Put the rectangle in image using
            # cv2 to highlight the barcode
            cv2.rectangle(img, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (255, 0, 0), 2)

            if barcode.data != "":
                # Print the barcode data
                split_code = str(barcode.data).split("'")[1]
                print(f"Barcode.data : {split_code}")
                # print(f"Barcode.type : {barcode.type}")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                driver.get("https://barcode-list.com/")
                driver.maximize_window()

                form = driver.find_element(by=By.XPATH, value="//input[@id='barcodeSearchField']")
                form.click()
                form.send_keys(f"{split_code}")
                search = driver.find_element(by=By.XPATH, value="//input[@id='barcodeSearchButton']")
                search.click()
                time.sleep(3)
                table = driver.find_element(by=By.XPATH, value="//table[@class='randomBarcodes']")
                table_rows = table.find_elements(by=By.TAG_NAME, value="tr")  # Find all table rows
                data = []
                for row in table_rows:
                    row_data = row.find_elements(by=By.TAG_NAME, value="td")  # Find the cells in each row
                    row_values = [cell.text for cell in row_data]
                    data.append(row_values)
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
    # Display the image
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    # Take the image from user
    image = "WhatsApp Image 2023-10-22 at 11.56.09.jpeg"
    BarcodeReader(image)
import json
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def searchOnTable(cedula,tipo):
# Initialize the WebDriver (assuming Chrome in this case)
    
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    # Initialize the WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)

    # URL of the website
    url = 'https://serviciosgis.eersa.com.ec:8081/'  # Replace with the actual URL

    # Open the webpage
    driver.get(url)

    # Find the form elements and fill them
    input_element = driver.find_element(By.ID, 'valor')  # Replace 'valor' with the actual ID of the input field
    input_element.send_keys(cedula)

    # Find and select the desired option from the dropdown
    dropdown = driver.find_element(By.ID, 'cboTipo')  # Replace 'cboTipo' with the actual ID of the dropdown
    dropdown.send_keys(tipo)  # Assuming 'Cuenta Contrato' is the visible text of the second option

    # Find and submit the form
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn-square') and contains(@class, 'btn-outline-primary')]")
    submit_button.click()
    # Wait for some time to allow the page to load completely
    time.sleep(5)
    # Get the page source after form submission
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the table
    table = soup.find('table')


    # Extract table contents if table exists
    if table:
        rows = table.find_all('tr')
        
        items = 0
        powerCutSchedule = ""
        for row in rows:
            columns = row.find_all('td')
            for column in columns:
                #print(column.get_text())
                powerCutSchedule+=column.get_text()+ " | "
                items +=1
                if items == 2:
                    return powerCutSchedule

    else:
        return "None"


def save_rows_to_json(rows, filename):
    # Convert rows to a list of dictionaries
    data = []
    for row in rows:
        date, time_range, recipient = row.split(' | ')
        data.append({
            'date': date.strip(),
            'time_range': time_range.strip(),
            'recipient': recipient.strip()
        })

    # Write data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
    

Documents = [
    ["0602245094","Casa"],
    ["0602447005","Julin"],
    ["0600204440","Mami Cuqui"],
    ["0501535603", "Caty"],
    ["0600110589","Mami Fanita"],
    ["0601470636001","Taty"],
    ["0602031932","Pa"],
    ["0602790040","Oscarin"]
    
]        


listOfCuts = []

print("Cortes de luz para los siguientes documentos:")
for docs in Documents:
    listOfCuts.append(searchOnTable(docs[0],'Cédula / RUC') + " " + docs[1])
        
for cut in listOfCuts:
    print(cut)
save_rows_to_json(listOfCuts, 'power_cuts.json')

    
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Create a new ChromeOptions object to configure the Chrome browser
chrome_options = webdriver.ChromeOptions()

# Add the following options to allow automated testing with a real instance of Chrome
chrome_options.add_argument('--no-sandbox')   # Bypass OS security model
# Overcome limited resource problems
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')   # Disable GPU acceleration
# Enable remote debugging
chrome_options.add_argument('--remote-debugging-port=9222')

# Detach the Chrome session to leave it
chrome_options.add_experimental_option("detach", True)

# Create a new instance of Chrome browser using the ChromeOptions object
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the website you want to automate
driver.get("https://app.skatteverket.se/klient-sifu-segmentering/")

# Wait for the form to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, 'year')))


def find_element_by_id(element_id) -> WebElement:
    wait.until(EC.presence_of_element_located((By.ID, element_id)))
    return driver.find_element(By.ID, element_id)


def select_value_in_dropdown(element_id, value):
    dropdown = find_element_by_id(element_id)
    select = Select(dropdown)
    select.select_by_visible_text(value)


def add_entry(row_data):
    # Dividend or interest?
    if row_data[0] =="D":
        find_element_by_id('label-inkomsttyp1').click()
    elif row_data[0] == "I":
        find_element_by_id('label-inkomsttyp2').click()

    # Select land in Swedish
    select_value_in_dropdown('land', row_data[1])

    # Select month
    select_value_in_dropdown('utbetalningsdatum-manad', row_data[2])

    # Select day
    select_value_in_dropdown('utbetalningsdatum-dag', row_data[3])

    # Select currency
    select_value_in_dropdown('beloppUtbetald-currency', row_data[4])

    # Input amount
    find_element_by_id('beloppUtbetald-amount').send_keys(row_data[5])

    # Have I paid for this already? Yes or no.
    if row_data[6] =="Y":
        find_element_by_id('label-isUtlandskSkatt1').click()
        # How much have I paid for this? Currency and amount
        select_value_in_dropdown('utlandskSkatt-currency', row_data[7])
        find_element_by_id('utlandskSkatt-amount').send_keys(row_data[8])
    elif row_data[6] == "N":
        find_element_by_id('label-isUtlandskSkatt2').click()
    

    # Submit this entry
    find_element_by_id('btn-form-submit').click()


with open('tax_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    year = next(reader)[0]
    # Select year
    select_value_in_dropdown('year', year)
    # Iterate over remaining rows
    for row in reader:
        add_entry(row)

driver.execute_script(f"alert('Tax data inserted for year {year}!')")

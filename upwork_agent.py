from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

web = 'https://www.homes.com/real-estate-agents/chicago-il/'
path = Service(executable_path=r"C:\Users\Downloads\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=path)
driver.get(web)

driver.maximize_window()



pagination = driver.find_element(By.XPATH, '//ol[@class="paging-results-container"]')
pages = pagination.find_elements(By.TAG_NAME, 'li')

last_page = int(pages[-2].text)

# last_page = 2

current_page = 1

agent_names = []
agent_companies = []
agent_phone = []
agent_sales = []
agent_deals = []
agent_pricerange = []

# for element in container:
#     name = element.find_element(By.XPATH, './/div[@class="name-container"]').text
#     company = element.find_element(By.XPATH, '//p[@class="company"]').text
#     phone = element.find_element(By.XPATH, '//p[@class="phone"]').text
#     total_sales = element.find_element(By.XPATH, './/p[@class="total-sales"]').text
#     deals = element.find_element(By.XPATH, './/p[@class="deals-area"]').text
#     price_range = element.find_element(By.XPATH, './/p[@class="price-range"]').text

while current_page <= last_page:
    
    time.sleep(10)
    container = driver.find_elements(By.XPATH, '//div[@class="details-container"]')

    for element in container:
        try:
            name = element.find_element(By.XPATH, './/div[@class="name-container"]').text
        except:
            name = 'N/A'
        
        try:
            company = element.find_element(By.XPATH, './/p[@class="company"]').text
        except:
            company = 'N/A'
            
        try:
            phone = element.find_element(By.XPATH, './/p[@class="phone"]').text
        except:
            phone = 'N/A'
            
        try:
            total_sales = element.find_element(By.XPATH, './/p[@class="total-sales"]/span').text
        except:
            total_sales = 'N/A'
            
        try:
            deals = element.find_element(By.XPATH, './/p[@class="deals-area"]/span').text
        except:
            deals = 'N/A'
            
        try:
            price_range = element.find_element(By.XPATH, './/p[@class="price-range"]/span').text
        except:
            price_range = 'N/A'
        
        agent_names.append(name)
        agent_companies.append(company)
        agent_phone.append(phone)
        agent_sales.append(total_sales)
        agent_deals.append(deals)
        agent_pricerange.append(price_range)
        
    current_page = current_page + 1
    if current_page <= last_page:
          try:
              next_page_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-component link next border" and contains(@title, "Next Page")]'))               )
              next_page_button.click()
          except Exception as e:
              print(f"Failed to navigate to the next page: {e}")
              break

# print(agent_names)
# print(agent_companies)
# print(agent_phone)
# print(agent_sales)
# print(agent_deals)
# print(agent_pricerange)

driver.quit()

df_name = pd.DataFrame({'Agent Name': agent_names, 'Company': agent_companies, 'Phone': agent_phone, 'Total Sales': agent_sales, 'Deals in this Location': agent_deals, 'Price range': agent_pricerange})
df_name.to_csv('agents_details.csv', index=False)


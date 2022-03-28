import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import lxml
import requests


FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdMv0_QZb9a5Rui0I578HifMvJrD0AX4jK3EeFHEB8UzInDNA/viewform?pli=1"
chrome_driver_path = "chromedriver.exe"
s= Service(chrome_driver_path)
URL = "https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=1&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment&cityName=Bangalore"
header = {
    "User-Agent": "Defined",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url=URL,headers=header)

driver = webdriver.Chrome(service=s)
driver.get(URL)

address_list = []
price_list =[]
link_list = []

time.sleep(2)
all_address = driver.find_elements(By.CLASS_NAME,value="mb-srp__card--title")
for address in all_address:
    address = address.text
    address_list.append(address)

all_price = driver.find_elements(By.CLASS_NAME,value='mb-srp__card__price--amount')
for price in all_price:
    price = price.text
    price_list.append(price.replace("₹","").replace("\n",""))


url = ""
soup = BeautifulSoup(driver.page_source,'html.parser')
all_link = soup.find_all(name="div",class_="mb-srp__card")

for link in all_link:
    meta = link.find_all('meta')
    for m in meta:
        if m['itemprop'] == 'url':
            url = m['content']
    link_list.append(url)



for n in range(len(address_list)):
    driver.get(FORM_URL)

    time.sleep(2)
    address_input = driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address_input.send_keys(address_list[n])
    price_input.send_keys(price_list[n])
    link_input.send_keys(link_list[n])
    submit.click()

    next_res = driver.find_element(By.LINK_TEXT, "Submit another response")
    next_res.click()
    time.sleep(1)




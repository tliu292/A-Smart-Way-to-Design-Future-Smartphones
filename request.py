import requests
import time
import selenium
from selenium import webdriver
from PIL import Image
import io
import os
import hashlib
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from super_resolution import super_resolve
# from super_resolution import model

# This is the path I use
# DRIVER_PATH = '.../Desktop/Scraping/chromedriver 2'
# Put the path for your ChromeDriver here
def downloadImg(folder_path:str,url:str,dimen:str, phoneName:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path, phoneName + '.jpg')
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb') as f:
            txt_path = os.path.join(folder_path, phoneName + '.txt')
            txtfile = open(txt_path, "w") 
            txtfile.write(dimen) 
            txtfile.close() 
            image.save(f, "JPEG", quality=100)
            super_resolve.resolve(file_path, file_path)
        # print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

def downloadPhone(wd):
    phoneLinks = wd.find_elements_by_css_selector("a[class='item pers']")
    cnt = len(phoneLinks)
    time.sleep(0.08)
    for i in range(cnt):
        retrieveLinks = wd.find_elements_by_css_selector("a[class='item pers']")
        time.sleep(0.08)
        # print("cnt : " + str(len(retrieveLinks)) + " curr: " + str(i))
        phoneLink = retrieveLinks[i]
        phoneName = phoneLink.text
        phoneLink.click()
        time.sleep(0.08)

        actual_image_tag = wd.find_element_by_css_selector('div.df').get_attribute("style")
        subUrl = []
        subUrl.append('https://droidchart.com')
        subUrl.append(str(actual_image_tag.split('background-image:')[-1][6:-3]))
        url = ''.join(list(subUrl))
        yearElement = wd.find_elements_by_xpath("//*[contains(text(), 'Launch')]/following-sibling::dd")
        if len(yearElement) == 1:
            year = str(yearElement[0].text)
        else:
            year = "Unknown"
        dimenElement = wd.find_elements_by_xpath("//*[contains(text(), 'Dimensions')]/following-sibling::dd")
        dimen = ''
        if len(dimenElement) != 0:
            new_chars = filter(str.isdigit, dimen)
            new_string = ''.join(list(new_chars))
            dimen = new_string
            # dimen = str(dimenElement[0].text).split(" x ")
            # for string in dimen:
            #     new_chars = filter(str.isdigit, string)
            #     new_string = ''.join(list(new_chars))
            #     new_dimen.append(new_string)
        else:
            dimen = "Unknown"
            # new_dimen.append(dimen)

        path = './images/'
        path = path + year
        downloadImg(path,url,dimen, phoneName)
        time.sleep(0.5)
        wd.back()
        time.sleep(0.08)

def downloadBrand(wd, link):
    link.click()
    time.sleep(0.08)
    downloadPhone(wd)
        # wd.back()
        # print(str(tests))
    time.sleep(0.08)

    # check if there's next page
    a = wd.find_elements_by_css_selector("a[title='Next page']")
    if len(a) == 1:
        # load next page
        downloadBrand(wd, a[0])
        time.sleep(0.08)
        wd.back()

# image_urls = set()
chrome_options = Options()  
chrome_options.add_argument("--headless")  

wd = webdriver.Chrome(executable_path="/Users/kyle/Downloads/453/chromedriver2", chrome_options=chrome_options)
# wd.get('http://www.google.com/')
wd.get('https://droidchart.com/en/brands')
links = wd.find_elements_by_css_selector("a[class='item pers']")
cnt = len(links)
for i in range(cnt):
    retryLinks = wd.find_elements_by_css_selector("a[class='item pers']")
    link = retryLinks[i]
    downloadBrand(wd, link)
    wd.back()
    



from selenium import webdriver
import os
import time

#Creating chrome options
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument('no-sandbox')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

#Initializing driver

driver = webdriver.Chrome(
        os.path.join(r'/Users/finnbassill/Downloads', 'chromedriver 3'),
        options=chrome_options)


#Function asks user for sku input(s)
def user_input():
    sku_list = []

    #Loops input function for user to check sizes/availability
    run = True
    while run:
        i = input('\nEnter Nike shoe SKU\n==> ')
        #Checking for SKU
        if len(i) == 10:
            sku_list.append(i)
        #Checking invalid SKU
        else:
            print('Invalid SKU or URL')   
            continue
            
        #Asks user if they want to enter another SKU
        check = True
        while check:
            cont = input('\nAdd another SKU? "YES/NO/Y/N"\n==> ')
            cont = cont.lower()
            if 'n' in cont:
                run = False
                check = False
            elif 'y' in cont:
                check = False
            
    return sku_list

#Function collects all urls of shoes on website
def get_urls():
    url_list = []

    #Get html of shoe homepages
    driver.get('https://www.nike.com/w/mens-shoes-nik1zy7ok')
    html = driver.page_source
    time.sleep(3)
    
    if 'CW2288-111' in html:
        url_index = html.index('CW2288-111')
        print(html[url_index-30, url_index + 10])

get_urls()

driver.close()



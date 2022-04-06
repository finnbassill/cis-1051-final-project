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
    
    #Get html of all shoes on nike site
    driver.get('https://www.nike.com/w?q=shoes&vst=shoes')

    #Scrolls to bottom of dynamic loaded page
    #REFERENCED: https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    #Loops until @ bottom of page
    run = True
    while run:

        #Scrolls down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        #Sets new height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        #Compares heights to see if @ bottom
        if new_height == last_height:
            run = False
        last_height = new_height

    
    #Gets page source code
    source = driver.page_source
    time.sleep(5)
    source = source.split('"')

    #Adds urls to list
    for string in source:
        if string[:23] == 'https://www.nike.com/t/':
            url_list.append(string)
    
    #Removes duplicates
    
    for i in range(len(url_list)):
        if i % 2 == 0:
            url_list.pop(i)

    file = open('temp.txt','w')
    for url in url_list:
        file.write(url + '\n')
    file.close()

get_urls()

driver.close()



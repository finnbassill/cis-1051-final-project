'''nike_bot.py CURRENT WORKING VERSION'''

import os
import re
import discord
import time
from selenium import webdriver
from discord.ext import commands
from dotenv import load_dotenv

'''Web Scraper'''

#Creating chrome options
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument('no-sandbox')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

#Scrapes the webpage for the name of the shoe and available sizes
def shoe_sizes(sku):

    #Initializing driver
    driver = webdriver.Chrome(
        os.path.join(r'/Applications', 'chromedriver'),
        options=chrome_options)

    #Searches the website for the sku
    search_url = f'https://www.nike.com/w?q={sku}&vst={sku}'
    driver.get(search_url)

    #Gets page html source code
    source = driver.page_source
    source = source.split('"')

    #Finds link to the shoes page
    for string in source:
        if 'https://www.nike.com/t/' in string:
            driver.get(string)
            break
    
    #Gets name and type of shoe and checks if sku is on website
    shoe_name = ''
    shoe_type = ''
    try:
        shoe_name = driver.find_element_by_xpath("//div[@class='pr2-sm css-1ou6bb2']/h1").get_attribute("textContent")
        shoe_type = driver.find_element_by_xpath("//div[@class='pr2-sm css-1ou6bb2']/h2").get_attribute("textContent")
    except:
        return False


    shoe_sizes = {}
    iterator = 1

    #Loops through each shoe size /div and checks size and if its available
    run = True
    while run:

        #Trys each /div in @class to see if it exists
        try:
            element = driver.find_element_by_xpath(f"//fieldset[@class=' mt5-sm mb3-sm body-2 css-1pj6y87']/div/div[{iterator}]/input")
            size_temp = driver.find_element_by_xpath(f"//fieldset[@class=' mt5-sm mb3-sm body-2 css-1pj6y87']/div/div[{iterator}]").text

            #If elem doesn't have @disabled atribute add size to list
            if element.get_attribute('disabled') is None:
                shoe_sizes[size_temp] = 'In-Stock'
            else:
                shoe_sizes[size_temp] = 'Out-of-Stock'

        except:
            run = False

        iterator += 1

    #Checks to see if shoe is not available

    not_avail_text = ''
    try:
        not_avail_text = driver.find_element_by_xpath("//div[@class='mt8-lg']/div").text
    except:
        pass
    
    url = driver.current_url

    #Closes driver
    driver.close()
    
    return shoe_name, shoe_type, shoe_sizes, url, not_avail_text


def all_skus():

    #Initializing driver
    driver = webdriver.Chrome(
        os.path.join(r'/Applications', 'chromedriver'),
        options=chrome_options)

    sku_list = []
    
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
            if string[-10:] not in sku_list:
                sku_list.append(string[-10:])

    file = open('sku_list.txt', 'w')
    for sku in sku_list:
        file.write(sku + '\n')
    file.close()

    #Closes driver
    driver.close()

    return file

#all_skus()




'''Discord Bot'''

#Defines command prefix
bot = commands.Bot(command_prefix='$')

#Bot command function retrieves sku 
@bot.command(name='nike', help='Enter "$nike [sku]" to find the sizes and size availability for that shoe; EX: $nike CW2288-111\nEnter "$nike skulist" to get a list of all the nike shoe skus on the website')
async def nike_bot(ctx, user_input= None):

    #If nothing is entered
    if input is None:
        await ctx.send('`--Enter A Nike Sku--`')

    #Checks format of sku entered
    size_re = r'\b[a-zA-Z0-9]{2}\d{4}-\d{3}\b'
    sku_re = r'\b[sS][kK][uU][lL][iI][sS][tT]\b'
    if re.match(size_re, user_input):
        await ctx.send('`--Retrieving Size Info--`')

        #Calls the scraper to get shoe name and available sizes
        shoe_info = shoe_sizes(user_input)
        
        #Checks if sku is found
        if shoe_info is False:
            await ctx.send('`--Sku Not Found On Nike--`')
        else:

            #Checking to see if not available
            if shoe_info[4] == '':
                embed = discord.Embed(title=shoe_info[0], url=shoe_info[3], description=shoe_info[1])
            else:
                embed = discord.Embed(title=shoe_info[0], url=shoe_info[3], description=shoe_info[4])
            
            #Adding fields
            for size in shoe_info[2]:
                embed.add_field(name=size, value=shoe_info[2][size], inline=True)
            await ctx.send(embed=embed)

    #Checking for command 'skulist'
    elif re.match(sku_re, user_input):
        await ctx.send('`--Retrieving All Skus--`')
        all_skus()
        await ctx.send(file=discord.File('sku_list.txt'))
        os.remove('sku_list.txt')

    #Checks for invalid command
    else:
        await ctx.send('`--Sku Format Is Incorrect--`')


#Loads .env and runs bot
load_dotenv()
bot.run(os.getenv('BOT_TOKEN'))


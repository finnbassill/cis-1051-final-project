'''nike_bot.py CURRENT WORKING VERSION'''

import os
import re
import discord
from xml.etree.ElementTree import ElementTree
from xmlrpc.server import SimpleXMLRPCDispatcher
from selenium import webdriver
from discord.ext import commands
from dotenv import load_dotenv

'''Web Scraper'''

#Creating chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument('no-sandbox')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

#Initializing driver
driver = webdriver.Chrome(
        os.path.join(r'/Applications', 'chromedriver'),
        options=chrome_options)

#Scrapes the webpage for the name of the shoe and available sizes
def nike_scraper(sku):

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
    
    #Gets name and typeof shoe
    shoe_name = driver.find_element_by_xpath("//div[@class='pr2-sm css-1ou6bb2']/h1").get_attribute("textContent")
    shoe_type = driver.find_element_by_xpath("//div[@class='pr2-sm css-1ou6bb2']/h2").get_attribute("textContent")

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

    url = driver.current_url
    
    return shoe_name, shoe_type, shoe_sizes, url


'''Discord Bot'''

#Defines command prefix
bot = commands.Bot(command_prefix='$')

#Bot command function retrieves sku 
@bot.command(name='nike', help='Temp')
async def nike_bot(ctx, sku= None):

    #If nothing is entered
    if sku is None:
        await ctx.send('`--Enter A Nike Sku--`')

    #Checks format of sku entered
    sku_re = r'\b[a-zA-Z]{2}\d{4}-\d{3}\b'
    if re.match(sku_re, sku):
        await ctx.send('`--Retrieving Size Info--`')

        #Calls the scraper to get shoe name and available sizes
        shoe_info = nike_scraper(sku)
        embed = discord.Embed(title=shoe_info[0], url=shoe_info[3], description=shoe_info[1])
        for size in shoe_info[2]:
            embed.add_field(name=size, value=shoe_info[2][size], inline=True)
        await ctx.send(embed=embed)
        
    else:
        await ctx.send('`--Sku Format Is Incorrect--`')

#Loads .env and runs bot
load_dotenv()
bot.run(os.getenv('BOT_TOKEN'))


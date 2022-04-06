# Proposal

## What will (likely) be the title of your project?

Nike Sneaker Stock Number Discord Bot

## In just a sentence or two, summarize your project. (E.g., "A website that lets you buy and sell stocks.")

An interactive discord bot that when called with a nike shoe SKU, scrapes the nike website and returns available sizes and stock numbers.

## In a paragraph or more, detail your project. What will your software do? What features will it have? How will it be executed?

The first part of the program is a discord bot. The user in the discord calls the bot with the Nike SKU. The discord function then calls the web scraper function. This function is going to either edit the url with the sku to pull up the shoes page or is going to put the sku in the searchbar and find the shoes page from there. Then the bot will find available sizes based on the sizing options on the page and record them. If the stock numbers are accessible, they would also be buried in the html, so selenium will scrape for those as well. After all the information is recorded, the discord bot will send a message with the available sizes and stock numbers.

## If planning to combine 1051's final project with another course's final project, with which other course? And which aspect(s) of your proposed project would relate to 1051, and which aspect(s) would relate to the other course?

N/A

## If planning to collaborate with 1 or 2 classmates for the final project, list their names, email addresses, and the names of their assigned TAs below.

N/A

## In the world of software, most everything takes longer to implement than you expect. And so it's not uncommon to accomplish less in a fixed amount of time than you hope.

### In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?

I have enough experience with selenium and front-end scraping to have a discord bot that can be called with a SKU and returns a list of sizes available.

### In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?

The better outcome is a bot with the ability to find the shoes stock numbers within the html of the page, rather than just finding the shoes available sizes. 

### In a sentence (or list of features), define a BEST outcome for your final project. I.e., what do you HOPE to accomplish before the final project's deadline?

Ideally I will be able to learn how to work with nikes backend or api to find the stock numbers and avilable sizes in a faster more streamlined way, but this seems unrealistic.

## In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research? If working with one of two classmates, who will do what?

Most of the libraries I have worked with before, such as selenium webdriver and the discord.py library. Granted, I'm definitely going to need to refresh on the discord libraries as working with discord bots can get slightly complex. I'm going to look in to working with nikes backend or api to see if i can streamline the project and make it more professional, but probably after the frontend part of the project is done. There may be new html elements that I'll need to understand working with a new website and different dynamis website factors that I haven't worked with before such as dynamic loaded pages. Overall, I have explored web scraping and discord bots enough to feel fairly comfortable with this project.

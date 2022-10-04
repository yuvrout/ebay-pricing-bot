from types import NoneType
from bs4 import BeautifulSoup
from datetime import date
import requests
import pandas as pd
import time

# Testing URL - can be removed
# url1 = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=commercial+refrigeration+equipment&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn=4'

# Parent URL link
url_list_html = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=commercial+refrigeration+equipment&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn='

# The output result location
output_file = '/Users/yrout/internship/output.csv'

#
# Logic: This function gets the list of actual URL based on pagination
# example of URL with page numbers..
# https://www.ebay.com/sch/i.html?_from=R40&_nkw=commercial+refrigeration+equipment&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn=1
# https://www.ebay.com/sch/i.html?_from=R40&_nkw=commercial+refrigeration+equipment&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn=2
# https://www.ebay.com/sch/i.html?_from=R40&_nkw=commercial+refrigeration+equipment&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn=3
# https://www.ebay.com/sch/i.html?_from=R40&_nkw=commercial+refrigeration+equipment&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn=4
# Argument: List of HTML sections
# Returns: URL Links with page number
#
def get_url_list(url_list_html):
   url_list = []
   url_list_section = get_data(url_list_html)
   parts = url_list_section.find_all('a',{'class': 'pagination__item'})
   for part in parts:
      url_list.append(part['href'])
   return url_list

#
# Reads HTML content from the URL Page
# Argument: URL Page
# Returns: HTML page in text content
#
def get_data(url):
   try:
      req =  requests.get(url, timeout=60)
      soup = BeautifulSoup(req.text, 'html.parser')
      return soup
   except requests.exceptions.RequestException as e:
      print (e) 

#
# Parse Product parts based on the requirement 
# Argument: HTML page content
# Return: List of product parts
#
def parse(soup):
   partslist = []
   parts = soup.find_all('div',{'class': 's-item__info clearfix'})
   today = date.today()


   for part in parts:
      
      part_name = part.find('span', {'role': 'heading'}).text

      if part.find('span', {'class': 'POSITIVE'}) is not None:
         sold_date = part.find('span', {'class': 'POSITIVE'}).text.replace('Sold', '')
      else:
         sold_date = ''

      if part.find('span', {'class': 's-item__price'}).find('span', {'class': 'POSITIVE'}) is not None:
         price_sold = part.find('span', {'class': 's-item__price'}).find('span', {'class': 'POSITIVE'}).text
      else:
         price_sold = ''

# Only identifying the detail url if the part name is present.
# 's-item__info clearfix' class returns other part names, so we exclude "Shop by ebay"
      if(len(part_name) != 0 and part_name != 'Shop on eBay'):
         part_detail_url = part.find('a',{'class': 's-item__link'})['href']

         remaining_product_fields = get_remaining_item(part_detail_url)
         #print(remaining_product_fields['product_location'])


         product = {
            'Date Scanned': today,
            'Item Name': part_name, 
            'Date Sold': sold_date, 
            'Price Sold': price_sold,
            'Location of Item': remaining_product_fields['product_location'],
            'Seller': remaining_product_fields['seller_name'],
            'Model Number': remaining_product_fields['model_number']
         }
         # 
         # Create an array with HVAC phrases
         # Read each phrase from array
         # Compare the phrase to the partslist
         # Don't add into output_file if present   
         #
         hvac_phrase_list = ["ventilator", "heater", "compressor", "condenser", "evaporator"]
      
         found = False
         for each_hvac_phrase in hvac_phrase_list:
            if each_hvac_phrase.lower() in part_name.lower():
               found = True
         #If at least one HVAC phrase list is found then include in partlist
         if found == True:
            a = 1
         else:
            partslist.append(product)
               #partslist.append(product)
   return partslist

#
# Parse remaining three fields (Model Number, Seller, Location of Item)
# Argument: detail item url
# Returns: Value of the above three fields
#
def get_remaining_item(part_detail_url):
   item_location = ' '
   remaining_item_soup = get_data(part_detail_url)
   #
   # Parsing Location of Item
   #
   if remaining_item_soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['u-flL']) is not None:
      
      if (remaining_item_soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['u-flL'])).find(lambda tag: tag.name == 'a' and tag.get('class') == ['vi-txt-underline']):
         a=1 #This line was added in order to skip this condition.
      else:
         location_in = remaining_item_soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['u-flL']).text
         if any(map(str.isdigit, location_in)):
            a=1 #This line was added in order to skip this condition.
         else:
            item_location = location_in
   #
   # Parsing Seller
   #
   if remaining_item_soup.find(lambda tag: tag.name == 'span' and tag.get('class') == ['mbg-nw']) is not None:
      seller = remaining_item_soup.find(lambda tag: tag.name == 'span' and tag.get('class') == ['mbg-nw']).text
   else:
      seller = ' '

   #
   # Parsing Model Number
   # 
   if remaining_item_soup.find('span', {'itemprop': 'model'}) is not None:
      model_number = remaining_item_soup.find('span', {'itemprop': 'model'}).text
   else:
      model_number = ' '

   remaining_product_fields = dict()
   remaining_product_fields['product_location'] = item_location 
   remaining_product_fields['seller_name'] = seller
   remaining_product_fields['model_number'] = model_number
 
   return remaining_product_fields

#
# Print the result to the CSV file
# Argument: Product parts information
# Return: nothing
#
def output(partslist):
   partsdf = pd.DataFrame(partslist)
   partsdf.to_csv(output_file, index=False)
   print('Saved to CSV')
   return

#
#
# Main program 
# 
#
final_parts_list = []
url_list = get_url_list(url_list_html) 
for url in url_list:
   soup = get_data(url)
   parts_list = parse(soup)
   final_parts_list.extend(parts_list)

output(final_parts_list)

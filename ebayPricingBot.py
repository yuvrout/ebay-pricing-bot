from types import NoneType
from bs4 import BeautifulSoup
from datetime import date
import requests
import pandas as pd

# Testing URL - can be reomved
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

      product = {
         'Date Scanned': today,
         'Item Name': part_name, 
         'Date Sold': sold_date, 
         'Price Sold': price_sold
      }
      partslist.append(product)
   return partslist

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
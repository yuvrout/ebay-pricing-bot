# eBay Pricing Bot

TESTING SUMMARY: https://docs.google.com/document/d/1NCqYYnQl37EnRn_VOY1PfyICrxqjCWq_vBpCbyASmGo/edit?usp=sharing

## Introduction

The eBay Pricing Bot is designed to assist administrators in tracking commercial refrigeration products sold on eBay. It automates the process of logging into eBay, searching, and extracting sales data for refrigeration equipment and parts sold over the last week, excluding any HVAC equipment. This bot ensures efficient monitoring of market trends and aids in data-driven decision-making.

## Objective

- Allow administrators to understand market dynamics by providing insights into products sold, their prices, and sales dates on eBay.

## Features

- **Automated Login**: Logs into eBay to access required data.
- **Search and Filter**: Searches for sold products in the commercial refrigeration category and filters out unrelated HVAC equipment.
- **Data Extraction**: Gathers detailed information about each product, including sale date, item name, model number, seller details, and prices.
- **Scheduled Runs**: Capable of running weekly or as frequently as required to keep data up-to-date.
- **Output Format**: Outputs data to a Google Sheet for easy viewing and analysis.

## Technologies

- **Beautiful Soup**: Used for web scraping.
- **Python**: Primary programming language.
- **Google Sheets API**: For data output and storage.

## Setup

To run this project locally, follow the steps below:

1. Clone the repository:

git clone https://github.com/yourusername/ebay-pricing-bot.git

2. Install the required packages:

pip install beautifulsoup4 google-api-python-client

3. Set up Google Sheets API according to the [official documentation](https://developers.google.com/sheets/api/quickstart/python).

4. Enter your eBay credentials and target Google Sheet details in `config.py`.

## Usage

To execute the bot:

python run_bot.py

This will start the bot, which will perform the tasks as scheduled. Make sure to configure the scheduler according to your needs.

## Project Structure

- `run_bot.py`: Main script to start the bot.
- `get_url_list.py`: Retrieves list of URLs from eBay.
- `get_data.py`: Extracts HTML content from the pages.
- `parse.py`: Parses product details from HTML.
- `output.py`: Outputs data to a CSV file or Google Sheet.

## Testing

### Strategy

- `Unit Tests`: Individual tests for each function to ensure they perform their intended operations correctly.
- `Integration Tests`: Combined testing of function interactions to ensure the data flow is handled properly from URL generation to data output.
- `Mock Tests`: Utilization of mock objects to simulate eBay API responses for testing under controlled conditions..
- `Error Handling Tests`: Ensures the bot can handle exceptions and errors gracefully, such as connection timeouts or parsing errors.

### Features Tested

- `URL Retrieval and Parsing`: Ensures URLs are generated correctly and that the HTML content is accurately parsed.
- `Data Filtering and Extraction`: Tests the bot's logic in filtering out unwanted items and accurately extracting necessary data.
- `Output Accuracy`: Verifies that the data is correctly formatted and written to the output file or Google Sheet.

### Features Not Tested

- `Internal Workings of Libraries`: Assumes that external libraries such as BeautifulSoup and pandas function as intended without testing their internal mechanisms.

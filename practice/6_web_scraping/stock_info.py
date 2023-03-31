"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""
import requests
from bs4 import BeautifulSoup as soup
import pandas as pd 
import bisect

def get_page(url):
    """Function to return html from specified url."""
    web_page = soup(requests.get(url, headers={'User-Agent': 'Custom'}).content, "html.parser")
    return web_page

def get_active_stock_count():
    """Function to return total number of currently active stocks."""
    stock_page = get_page('https://finance.yahoo.com/most-active')
    stock_container = stock_page.select_one('#fin-scr-res-table div')
    stock_count_container = stock_container.select_one('div > span + span > span').text
    return int(stock_count_container.split('of')[1].replace('results', '').strip())

def generate_sheets():
    """Function to generate sheets."""
    active_stock_count = get_active_stock_count() 
    # body = get_page(f'https://finance.yahoo.com/most-active?offset=0&count={active_stock_count}')
    body = get_page('https://finance.yahoo.com/most-active?offset=0&count=5') # Getting the page with all of the most active stocks

    quote_links = body.select('a[data-test="quoteLink"]') # Making a list of all the stock codes
    stock_symbols = [link.text for link in quote_links]

    # Initializing lists for required fields 
    stock_names = []
    stock_countries = []
    stock_employees = []
    stock_ceo_names = []
    stock_ceo_dobs = []
    stock_ceo_symbols = []

    stock_5_youngest_lst = []
    stats_10_best_change_lst = []

    for symbol in stock_symbols:
        # Selecting profile section and extracting the stock name, country and number of employees
        profile_page = get_page(f"https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}").find('body')
        asset_profile = profile_page.select_one('div[data-test="asset-profile"] [data-test="qsp-profile"]')
    
        stock_name = asset_profile.select_one('h3').text.strip()
        stock_country = asset_profile.select_one('p a').previous_sibling.previous_sibling
        stock_num_employees = asset_profile.select_one('p:last-of-type span:last-of-type').text.replace(',', '')

        stats_page = get_page(f"https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}").find('body')
        stats_table = stats_page.select_one('[data-test="qsp-statistics"] :nth-child(2) > div + div table')
        stats_52_week_change = stats_table.select_one('tbody tr:nth-child(2) td:nth-child(2)').text.replace('%', '')
        stats_cash = stats_page.select_one('#Col1-0-KeyStatistics-Proxy > section > div.Mstart\(a\).Mend\(a\) > div:nth-child(3) > div > div:nth-child(5) > div > div > table > tbody > tr.Bxz\(bb\).H\(36px\).BdY.Bdc\(\$seperatorColor\) > td.Fw\(500\).Ta\(end\).Pstart\(10px\).Miw\(60px\)').text

        # print(f"weekly change: {stats_52_week_change} and cash: {stats_cash}")
        # Getting the table with information about all the CEOs for the stock
        stock_ceo_table = profile_page.select_one('section.quote-subsection table tbody')

        if(len(stats_10_best_change_lst) < 10):
            bisect.insort(stats_10_best_change_lst, (-float(stats_52_week_change), stock_name, symbol, stats_cash))
        elif -stats_52_week_change < stats_10_best_change_lst[-1][0]:
            stats_10_best_change_lst.pop()
            bisect.insort(stats_10_best_change_lst, (-float(stats_52_week_change), stock_name, symbol, stats_cash))

        for stock_ceo in stock_ceo_table.select('tr'):
            stock_ceo_name = stock_ceo.select_one('td:first-child').text
            stock_ceo_dob = stock_ceo.select_one('td:nth-last-child(1)').text
            if stock_ceo_dob != "N/A":
                stock_ceo_dob = int(stock_ceo_dob)
                if len(stock_5_youngest_lst) < 5:
                    bisect.insort(stock_5_youngest_lst, (-stock_ceo_dob, stock_name, symbol, stock_country, stock_num_employees, stock_ceo_name))
                elif -stock_ceo_dob < stock_5_youngest_lst[-1][0]:
                    stock_5_youngest_lst.pop()
                    bisect.insort(stock_5_youngest_lst, (-stock_ceo_dob, stock_name, symbol, stock_country, stock_num_employees, stock_ceo_name))
    print(stats_10_best_change_lst)
    for ceo in stock_5_youngest_lst:
        young_ceo_dob = -ceo[0]
        young_ceo_stk_name = ceo[1]
        young_ceo_symbol = ceo[2]
        young_ceo_country = ceo[3]
        young_ceo_num_empl = ceo[4]
        young_ceo_name = ceo[5]

        stock_names.append(young_ceo_stk_name)
        stock_countries.append(young_ceo_country)
        stock_employees.append(young_ceo_num_empl)

        stock_ceo_names.append(young_ceo_name)
        stock_ceo_dobs.append(young_ceo_dob)
        stock_ceo_symbols.append(young_ceo_symbol)


    youngest_ceos_df = pd.DataFrame({'Name': stock_names, 'Code': stock_ceo_symbols, 'Country': stock_countries, 'Employees': stock_employees, 'CEO Name': stock_ceo_names, 'CEO Year Born':stock_ceo_dobs})

    with open('youngest_ceos_sheet', 'w', encoding="utf-8") as sheet1:
        sheet_title = "5 stocks with the youngest CEOs"
        dash_length = 80+len(sheet_title)
        sheet1.write(sheet_title.center(dash_length, "="))
        sheet1.write("\n")
        sheet1.write("| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |\n")
        sheet1.write("-"*dash_length+"\n")
        for index, row in youngest_ceos_df.iterrows():
            sheet1.write(f"| {row['Name']}{row['Code']} |\n".ljust(dash_length, " "))

if __name__ == "__main__":
    generate_sheets()

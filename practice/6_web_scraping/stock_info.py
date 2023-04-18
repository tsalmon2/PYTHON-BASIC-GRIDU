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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path 


def get_page(url):
    """Function to return html from specified url."""
    web_page = soup(requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'}).content,
                    "lxml")
    return web_page.find('body')


def get_active_stock_count():
    """Function to return total number of currently active stocks."""
    stock_page = get_page('https://finance.yahoo.com/most-active')
    stock_container = stock_page.select_one('#fin-scr-res-table div')
    stock_count_container = stock_container.select_one('div > span + span > span').text
    return int(stock_count_container.split('of')[1].replace('results', '').strip())


def generate_stock_symbols_lst():
    """Function to generate a list of all the stock symbols."""
    active_stock_count = get_active_stock_count()
    body = get_page(
        f'https://finance.yahoo.com/most-active?offset=0&count={active_stock_count}')  # Getting the page with all of the most active stocks
    quote_links = body.select('a[data-test="quoteLink"]')  # Making a list of all the stock codes
    return [link.text for link in quote_links]


def generate_current_best(curr_lst: list, size: int, attrs: tuple):
    """Function to update the specified list with the current best restricted to the specified size."""
    if len(curr_lst) < size:
        bisect.insort(curr_lst, attrs)
    elif attrs[0] < curr_lst[-1][0]:
        curr_lst.pop()
        bisect.insort(curr_lst, attrs)
    return curr_lst

# Initializing variables for sheet generation
stock_symbols = generate_stock_symbols_lst()

required_fields = {
    "youngest_ceos": {"names": [], "symbols": [], "country": [], "employees": [], "ceo_names": [], "ceo_dobs": []},
    "52_week_change": {"names": [], "symbols": [], "52_change": [], "cash": []},
    "largest_holds": {"names": [], "symbols": [], "holders": [], "shares": [], "date_reported": [], "%_out": [],
                      "values": []}}

stock_5_youngest_lst = []
stats_10_best_change_lst = []
holders_10_largest_lst = []

def get_info(symbol):
    # Selecting profile section
    profile_page = get_page(f"https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}")
    asset_profile = profile_page.select_one('div[data-test="asset-profile"] [data-test="qsp-profile"]')

    # Extracting info for the youngest ceos sheet
    stock_name = asset_profile.select_one('h3').text.strip()
    stock_country = asset_profile.select_one('p a').previous_sibling.previous_sibling
    stock_num_employees = asset_profile.select_one('p:last-of-type span:last-of-type').text.replace(',', '')

    # Getting the table with information about all the CEOs for the stock
    stock_ceo_table = profile_page.select_one('section.quote-subsection table tbody')

    # Generating list with info for the current youngest CEOs
    for stock_ceo in stock_ceo_table.select('tr'):
        stock_ceo_name = stock_ceo.select_one('td:first-child').text
        stock_ceo_dob = stock_ceo.select_one('td:nth-last-child(1)').text
        if stock_ceo_dob != "N/A":
            stock_ceo_dob = int(stock_ceo_dob)
            generate_current_best(stock_5_youngest_lst, 5, (
                -stock_ceo_dob, stock_name, symbol, stock_country, stock_num_employees, stock_ceo_name))

    # Extracting info for the 52 week change sheet
    stats_page = get_page(f"https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}")
    stats_table = stats_page.select_one('[data-test="qsp-statistics"] :nth-child(2) > div + div table')
    stats_52_week_change = stats_table.select_one('tbody tr:nth-child(2) td:nth-child(2)').text.replace('%', '')
    stats_cash_table = stats_page.select('[data-test="qsp-statistics"] div:nth-last-child(1) > table tbody')[-2]
    stats_cash = stats_cash_table.select_one('tr td:nth-child(2)').text

    if stats_52_week_change != "N/A":
        stats_52_week_change = float(stats_52_week_change)
        # Generating list with info for the current stocks with the best 52-week change
        generate_current_best(stats_10_best_change_lst, 10,
                              (-float(stats_52_week_change), stock_name, symbol, stats_cash))


with ThreadPoolExecutor() as ex:
    for symbol in stock_symbols:
        ex.submit(get_info, symbol)

# Extracting info for the largest holds of Blackrock Inc. sheet
holders_page = get_page(f"https://finance.yahoo.com/quote/BLK/holders?p=BLK")
holders_tables = holders_page.select('[data-yaft-module="tdv2-applet-Holders"] table')
institutional_holders_table = holders_tables[1].select_one('tbody')
mutual_holders_table = holders_tables[2].select_one('tbody')

# Generating list with info for the current largest holders (both mutual and institutional holders)
for m_holder in mutual_holders_table.select('tr'):
    m_value = m_holder.select_one('td:nth-last-child(1)').text
    m_perc_out = m_holder.select_one('td:nth-last-child(2)').text
    m_date_rep = m_holder.select_one('td:nth-last-child(3) > span').text
    m_shares = int(m_holder.select_one('td:nth-last-child(4)').text.replace(",", ""))
    m_hold_name = m_holder.select_one('td:nth-last-child(5)').text

    generate_current_best(holders_10_largest_lst, 10,
                          (-m_shares, 'BlackRock, Inc.', 'BLK', m_value, m_date_rep, m_perc_out, m_hold_name))

for i_holder in institutional_holders_table.select('tr'):
    i_value = i_holder.select_one('td:nth-last-child(1)').text
    i_perc_out = i_holder.select_one('td:nth-last-child(2)').text
    i_date_rep = i_holder.select_one('td:nth-last-child(3) > span').text
    i_shares = int(i_holder.select_one('td:nth-last-child(4)').text.replace(",", ""))
    i_hold_name = i_holder.select_one('td:nth-last-child(5)').text

    generate_current_best(holders_10_largest_lst, 10,
                          (-i_shares, 'BlackRock, Inc.', 'BLK', i_value, i_date_rep, i_perc_out, i_hold_name))

# Updating required fields dictionary with 5 youngest ceos
for ceo in stock_5_youngest_lst:
    young_ceo_dob = -ceo[0]
    young_ceo_stk_name = ceo[1]
    young_ceo_symbol = ceo[2]
    young_ceo_country = ceo[3]
    young_ceo_num_empl = ceo[4]
    young_ceo_name = ceo[5]

    required_fields["youngest_ceos"]["names"].append(young_ceo_stk_name)
    required_fields["youngest_ceos"]["symbols"].append(young_ceo_symbol)

    required_fields["youngest_ceos"]["country"].append(young_ceo_country)
    required_fields["youngest_ceos"]["employees"].append(young_ceo_num_empl)
    required_fields["youngest_ceos"]["ceo_names"].append(young_ceo_name)
    required_fields["youngest_ceos"]["ceo_dobs"].append(young_ceo_dob)

# Updating required fields dictionary with stocks with 10 best 52-week change
for stat in stats_10_best_change_lst:
    stat_week_change = f"{-stat[0]}%"
    stat_stk_name = stat[1]
    stat_symbol = stat[2]
    stat_cash = stat[3]

    required_fields["52_week_change"]["names"].append(stat_stk_name)
    required_fields["52_week_change"]["symbols"].append(stat_symbol)

    required_fields["52_week_change"]["52_change"].append(stat_week_change)
    required_fields["52_week_change"]["cash"].append(stat_cash)

# Updating required fields dictionary with 10 largest holds of Blackrock Inc.
for hold in holders_10_largest_lst:
    hold_shares = -hold[0]
    hold_stk_name = hold[1]
    hold_symbol = hold[2]
    hold_val = hold[3]
    hold_date = hold[4]
    hold_perc = hold[5]
    holder_name = hold[6]

    required_fields["largest_holds"]["names"].append(hold_stk_name)
    required_fields["largest_holds"]["symbols"].append(hold_symbol)

    required_fields['largest_holds']['shares'].append(hold_shares)
    required_fields['largest_holds']['date_reported'].append(hold_date)
    required_fields['largest_holds']['%_out'].append(hold_perc)
    required_fields['largest_holds']['values'].append(hold_val)
    required_fields['largest_holds']['holders'].append(holder_name)

# Creating dataframes for the sheets
youngest_ceos_df = pd.DataFrame(
    {'Name': required_fields["youngest_ceos"]["names"], 'Code': required_fields["youngest_ceos"]["symbols"],
     'Country': required_fields["youngest_ceos"]["country"], 'Employees': required_fields["youngest_ceos"]["employees"],
     'CEO Name': required_fields["youngest_ceos"]["ceo_names"],
     'CEO Year Born': required_fields["youngest_ceos"]["ceo_dobs"]})
week_change_df = pd.DataFrame(
    {'Name': required_fields["52_week_change"]["names"], 'Code': required_fields["52_week_change"]["symbols"],
     '52-Week Change': required_fields["52_week_change"]["52_change"],
     'Total Cash': required_fields["52_week_change"]["cash"]})
largest_holders_df = pd.DataFrame(
    {'Name': required_fields['largest_holds']['names'], 'Code': required_fields['largest_holds']['symbols'],
     'Holders': required_fields["largest_holds"]["holders"], 'Shares': required_fields["largest_holds"]['shares'],
     'Date Reported': required_fields['largest_holds']['date_reported'],
     '% Out': required_fields['largest_holds']['%_out'], 'Values': required_fields['largest_holds']['values']})

# Generating the sheets as csv files
largest_holders_df.to_csv(Path(Path(__file__).parent / 'largest_holders.csv'), index=False)
youngest_ceos_df.to_csv(Path(Path(__file__).parent / 'youngest_ceos.csv'), index=False)
week_change_df.to_csv(Path(Path(__file__).parent / 'week_change.csv'), index=False)

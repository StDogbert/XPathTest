#!/usr/bin/env python3

from lxml import html
import requests
import datetime

gold_url = "https://www.investing.com/commodities/gold-historical-data"
silver_url = "https://www.investing.com/commodities/silver-historical-data"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrapData(url, comodity):
    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.content)

    entries = tree.xpath('//div[@id="results_box"]/table[@class="genTbl closedTbl historicalTbl"]/tbody/tr')

    with open('{}.csv'.format(comodity), 'w+') as csvfile:
        for entry in entries:
            tds = entry.xpath('td/text()')
            date_string = tds[0]
            price = tds[1].replace(",", "")
            date = datetime.datetime.strptime(date_string, '%b %d, %Y')
            formatted_date = date.strftime('%y-%m-%d')
            csvfile.write("{}\t{}\n".format(formatted_date, price))

scrapData(gold_url, "gold")
scrapData(silver_url, "silver")

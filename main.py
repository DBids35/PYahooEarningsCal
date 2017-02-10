from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


def dateToURL(date):
    return 'https://biz.yahoo.com/research/earncal/20170320.html'

with urllib.request.urlopen('https://biz.yahoo.com/research/earncal/20170320.html') as page:
    soup=BeautifulSoup(page, 'lxml')
    # print(soup.prettify())
    table=soup.find_all('table')[5]

    company=[]
    symbol=[]
    EPS_estimate=[]
    time=[]

    for row in table.findAll('tr'):
        cells = row.findAll('td')
        states = row.findAll('th')  # To store second column data
        if len(cells) == 5:  # Only extract table body not heading
            company.append(cells[0].find(text=True))
            symbol.append(cells[1].find(text=True))
            EPS_estimate.append(cells[2].find(text=True))
            time.append(cells[3].find(text=True))

earnings=pd.DataFrame({company[0]:company[1:],symbol[0]:symbol[1:],EPS_estimate[0]:EPS_estimate[1:],time[0]:time[1:] })
print(earnings.head())
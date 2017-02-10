from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


def dateToURL(month, day, year):
    month=str(month)
    day=str(day)
    year=str(year)
    if len(month)==1:
        month="0"+month
    if len(day)==1:
        day="0"+day
    return 'https://biz.yahoo.com/research/earncal/{}{}{}.html'.format(year, month, day)

def pullEarnings(month, day, year):
    try:
        with urllib.request.urlopen(dateToURL(month, day, year)) as page:
            soup=BeautifulSoup(page, 'lxml')
            # print(soup.prettify())
            table=soup.find_all('table')[5]
            company=[]
            symbol=[]
            EPS_estimate=[]
            time=[]

            for row in table.findAll('tr'):
                cells = row.findAll('td')
                if len(cells) >=5:  # Only extract table body not heading
                    company.append(cells[0].find(text=True))
                    symbol.append(cells[1].find(text=True))
                    EPS_estimate.append(cells[2].find(text=True))
                    time.append(cells[3].find(text=True))
        if company[0]=='\n' or symbol[0]=='\n'or EPS_estimate[0]=='\n'or time[0]=='\n':
            company=company[1:]
            symbol=symbol[1:]
            EPS_estimate=EPS_estimate[1:]
            time=time[1:]
        earnings=pd.DataFrame({company[0]:company[1:],symbol[0]:symbol[1:],EPS_estimate[0]:EPS_estimate[1:],time[0]:time[1:] })
    except urllib.error.HTTPError:
        raise Exception('No data for that date')
    return earnings

if __name__=="__main__":
    print(pullEarnings(2, 10, 2017).head())
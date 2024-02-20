
"""
Xiaotong Wang

code referring to question 1

scraping dataset from website
clean and store data into csv file

"""
import datetime
import io
from itertools import zip_longest
from urllib.request import Request, urlopen
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import ssl
import re

from dateutil.parser import parse

url = 'https://www.tfrrs.org/all_performances/IN_college_m_Indiana_IN.html?list_hnd=4153&season_hnd=608'
output_path = 'Men100meters.csv'
ssl._create_default_https_context = ssl._create_unverified_context


# scraping the info and return raw data
def scrape(url):
    req = Request(url)
    legacy_reviews = urlopen(req)
    soup = BeautifulSoup(legacy_reviews.read(), 'html.parser')
    # only extract the 100 meters table
    table = soup.find('table',class_='tablesorter tablesaw table-striped table-bordered table-hover tablesaw-columntoggle tablesorter-default hasFilters')
    cells = table.find_all('td')
    raw_data = []
    for i in cells:
        cell = i.text
        raw_data.append(cell.strip())
#    print(raw_data)
    return raw_data


#  clean the data as required and store it into csv file
#  find the fastest men and store it into csv file
def clean(raw_data):
    while '' in raw_data:
        raw_data.remove('')
    n = int(len(raw_data)/6)  # get the number of rows in the table to create data frame
    df = pd.DataFrame(np.array(raw_data).reshape(n, 6), columns=['athlete', 'year', 'time', 'meet', 'meet_date', 'wind'])
    # convert athlete name
    df['athlete'] = df['athlete'].apply(lambda x: ' '.join(x.replace('"', '').split(', ')[::-1]))
    # strip the characters so only the digit at the very end is showing
    df['year'] = df['year'].apply(lambda x: re.search(r'\d$', x).group() if re.search(r'\d$', x) else x)
    # convert meet date to epoch date
    df['meet_date'] = df['meet_date'].apply(lambda x: parse(x))
    df['meet_date'] = pd.to_datetime(df['meet_date']).astype('int64') // 10 ** 9
    # store the cleaned data into csv file
    df.to_csv(output_path, index=False)

    fastest_times_df = df.sort_values('time').groupby('athlete', as_index=False).first()
    # store the fastest 100m time that each athlete ran
    fastest_times_df.to_csv('fastest_men100.csv', index=False)

if __name__ == '__main__':
    raw_data = scrape(url)
    clean(raw_data)








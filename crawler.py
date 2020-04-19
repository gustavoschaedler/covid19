import requests
from bs4 import BeautifulSoup
import time
import random

step = 13
all_data = {}

random_number = random.random()
url = 'https://www.worldometers.info/coronavirus/?x='+str(random_number)

headers = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}
res = requests.get(url, headers=headers).text
soup = BeautifulSoup(res, 'html.parser')
soup.encode('utf-8')


last_updated = soup.find('div', {
                         'style': 'font-size:13px; color:#999; margin-top:5px; text-align:center'
                         }).get_text().strip()

main_numbers = soup.findAll('div', {'class': 'maincounter-number'})
cases = main_numbers[0].get_text().strip()
deaths = main_numbers[1].get_text().strip()
recovered = main_numbers[2].get_text().strip()

resume_data = {
    'last_updated': last_updated,
    'cases': cases,
    'deaths': deaths,
    'recovered': recovered
}

table_today = soup.find('table', {'id': 'main_table_countries_today'})

data_title = []
for item_title in table_today.findAll(name='thead'):
    for title in item_title.findAll('th'):
        data_title.append(title.get_text()
                          .replace(u'\xa0', u' ')
                          .replace(u'\n', u'')
                          .replace(u'/', u' ')
                          )

data_today = []
for item_data in table_today.findAll(name='tbody'):
    for data in item_data.findAll('td'):
        data_today.append(data.get_text()
                          .replace(u'\n', u'')
                          .replace(u'\xa0', u' ')
                          .replace(u'/', u' ')
                          # .replace(u' ', u'_')
                          .replace(u':', u'')
                          )

table_yesterday = soup.find('table', {'id': 'main_table_countries_yesterday'})

data_yesterday = []
for item_data in table_yesterday.findAll(name='tbody'):
    for data in item_data.findAll('td'):
        data_yesterday.append(data.get_text()
                              .replace(u'\n', u'')
                              .replace(u'\xa0', u' ')
                              .replace(u'/', u' ')
                              # .replace(u' ', u'_')
                              .replace(u':', u'')
                              )


all_data['title'] = data_title
all_data['resume'] = resume_data

all_data['yesterday'] = {
    ''.join([data_yesterday[i], '_', data_yesterday[step-1+i]]):
    data_yesterday[i:i + step] for i in range(0, len(data_yesterday), step)
}

all_data['today'] = {
    ''.join([data_today[i], '_', data_today[step-1+i]]):
    data_today[i:i + step] for i in range(0, len(data_today), step)
}

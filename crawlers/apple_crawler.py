import json
import requests
import os
from datetime import datetime, timedelta
from tqdm import tqdm
from bs4 import BeautifulSoup

def get_links(board, time_bound):
    result = []
    url = board[1]
    response = requests.get(url)
    links = json.loads(response.text)
    links = links['content_elements']
    for link in links:
        url = 'https://hk.appledaily.com' + link['canonical_url']
        time = link['display_date']
        date = time.split('T')[0].split('-')
        date = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        if date < time_bound:
            break
        title = link['headlines']['basic']
        data_dic = {
            'url': url,
            'time': time,
            'company': '壹傳媒',
            'label': board[0],
            'reporter': None,
            'title': title,
            'article': None,
            'raw_xml': None
        }
        result.append(data_dic)
    return result

def get_data(links):
    result = []
    for link in links:
        url = link['url']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            article = ''.join([i.text for i in soup.find('div', id='articleBody').find_all('p', class_='text--desktop text--mobile article-text-size_md')])
        except:
            continue
        data_dic = {
            'url': url,
            'time': link['time'],
            'company': '壹傳媒',
            'label': link['label'],
            'reporter': None,
            'title': link['title'],
            'article': article,
            'raw_xml': response.text
        }
        result.append(data_dic)
    return result

if __name__ == '__main__':
    boards = [
        ['香港', r'https://hk.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Flocal%5C%22%2BOR%2Btaxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fbreaking%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-24h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A66%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=220&_website=hk-appledaily'],
        ['國際', r'https://hk.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fworld%5C%22%2BOR%2Btaxonomy.primary_section._id%3A%5C%22%2Frealtime%2Finternational%5C%22%2BOR%2Btaxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fchina%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-24h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A56%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=220&_website=hk-appledaily'],
        ['娛樂', r'https://hk.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fentertainment%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-24h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A56%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=220&_website=hk-appledaily'],
        ['財經', r'https://hk.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Ffinance%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-24h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A26%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=220&_website=hk-appledaily'],
        ['體育', r'https://hk.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fsports%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-24h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A46%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=220&_website=hk-appledaily'],
    ]

    for board in tqdm(boards):
        time_bound = datetime.now() - timedelta(days=1)
        links = get_links(board, time_bound)
        data = get_data(links)
        file_path = os.path.join('crawlers', 'data', 'apple', f'{board[0]}.json')
        try:
            json.dump(data, open(file_path, 'w', encoding='utf8'))
        except:
            continue


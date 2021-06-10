import requests
import json
from tqdm import tqdm
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def get_links(board, time_bound):
    links = []
    for i in range(10):
        url = f'https://www.chinatimes.com/{board}/total?page={i+1}&chdtv'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        section_tag = soup.find('section', class_='article-list')
        ul_tag = section_tag.find('ul', class_='vertical-list list-style-none')
        li_tags = ul_tag.find_all('li')
        for li_tag in li_tags:
            div_tag = li_tag.find('div', class_='col')
            time_tag = div_tag.find('div', class_='meta-info').find('time')
            h3_tag = div_tag.find('h3', class_='title')
            a_tag = h3_tag.find('a')
            date = time_tag['datetime'].split(' ')[0].split('-')
            date = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
            if date < time_bound:
                break
            links.append(
                {
                    'url': 'https://www.chinatimes.com' + a_tag['href'],
                    'title': a_tag.text,
                    'time': time_tag['datetime'],
                    'label': board
                }
            )

    return links

def get_data(links):
    result = []
    for link in links:
        url = link['url']
        response = requests.get(url)
        raw_xml = response.text
        soup = BeautifulSoup(response.text, 'html.parser')

        time = link['time']
        company = '中時'
        label = link['label']
        title = link['title']
        try:
            reporter = [i.text for i in soup.find('div', class_='author').find_all('a')]
        except:
            reporter = None
        try:
            article = ''.join([i.text for i in soup.find('div', class_='article-body').find_all('p')])
        except:
            continue
        result.append(
            {
                'url': url,
                'time': time,
                'company': company,
                'label': label,
                'reporter': reporter,
                'title': title,
                'article': article,
                'raw_xml': raw_xml
            }
        )
    return result

if __name__ == "__main__":
    board_list = [
        'politic',
        'opinion',
        'life',
        'star',
        'money',
        'world',
        'chinese',
        'society',
        'armament',
        'technologynews',
        'sports',
        'hottopic',
        'health',
        'fortune',
        'taiwan'
    ]
    for b_name in tqdm(board_list):
        time_bound = datetime.now() - timedelta(days=7)
        links = get_links(b_name, time_bound)
        result = get_data(links)
        with open(f'crawlers/data/chinatimes/{b_name}.json', 'w', encoding='utf8') as output_file:
            json.dump(result, output_file)
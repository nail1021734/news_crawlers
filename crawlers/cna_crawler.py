import os
import json
import requests
from datetime import datetime, timedelta
from tqdm import tqdm
from bs4 import BeautifulSoup


def get_links(board):
    result = []
    url = 'https://www.cna.com.tw/cna2018api/api/WNewsList'
    for pg_index in range(5):
        post_data = {
            'action': 0, 'category': board[1], 'pageidx': pg_index+1, 'pagesize': "20"}
        response = requests.post(url, data=post_data)
        a = json.loads(response.text)
        for link in a['ResultData']['Items']:
            data_dic = {
                'url': link['PageUrl'],
                'time': link['CreateTime'],
                'company': '中央社',
                'label': link['ClassName'],
                'reporter': None,
                'title': link['HeadLine'],
                'article': None,
                'raw_xml': None
            }

            result.append(data_dic)
    return result


def get_data(links, time_bound):
    result = []
    for link in links:
        url = link['url']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            article = ''.join([i.text for i in soup.find('div', class_='paragraph').find_all('p')])
        except:
            continue
        date =  link['time'].split(' ')[0].split('/')
        date = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        if date < time_bound:
            break
        data_dic = {
            'url': url,
            'time': link['time'],
            'company': '中央社',
            'label': link['label'],
            'reporter': None,
            'title': link['title'],
            'article': article,
            'raw_xml': response.text
        }
        result.append(data_dic)
    return result

if __name__ == '__main__':
    board = [
        ['政治', 'aipl'],
        ['國際', 'aopl'],
        ['兩岸', 'acn'],
        ['產經', 'aie'],
        ['證券', 'asc'],
        ['科技', 'ait'],
        ['生活', 'ahel'],
        ['社會', 'asoc'],
        ['地方', 'aloc'],
        ['文化', 'acul'],
        ['運動', 'aspt'],
        ['娛樂', 'amov']
    ]
    for b in tqdm(board):
        time_bound = datetime.now() - timedelta(days=1)
        links = get_links(b)
        data = get_data(links, time_bound)
        json.dump(data, open(f'crawlers/data/cna/{b[0]}_{time_bound.strftime("%Y%m%d")}.json', 'w', encoding='utf8'))
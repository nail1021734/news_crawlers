# -*- coding:utf-8 -*-
import shutil
import sqlite3
import json
import os
from tqdm import tqdm


def create_table():
    instruct = u"""CREATE TABLE IF NOT EXISTS news_table (
        id integer PRIMARY KEY,
        url text,
        time text,
        company text,
        label text,
        reporter text,
        title text,
        article text,
        raw_xml text
    ); """
    conn_db = sqlite3.connect('news.db')
    c = conn_db.cursor()
    c.execute(instruct)
    conn_db.commit()
    conn_db.close()


def write_in_db(data):
    conn_db = sqlite3.connect('news.db')
    c = conn_db.cursor()
    db_url = list(c.execute('SELECT url from news_table'))
    db_url = list(map(lambda x: x[0], db_url))

    preprocessed_data = [tuple(i.values())
                         for i in data if i['url'] not in db_url]

    c.executemany(
        'INSERT INTO news_table(url, time, company, label, reporter, title, article, raw_xml) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', preprocessed_data)
    conn_db.commit()
    conn_db.close()


def chinatimes(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))

    for i in range(len(data)):
        if isinstance(data[i]['reporter'], list):
            data[i]['reporter'] = ' '.join(data[i]['reporter'])
            if data[i]['reporter'] == '':
                data[i]['reporter'] = None
    write_in_db(data)


def setn(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))

    for i in range(len(data)):
        if data[i]['time'] is not None:
            data[i]['time'] = ':'.join(data[i]['time'].split(':')[:-1])
            data[i]['time'] = data[i]['time'].replace('/', '-')
    write_in_db(data)


def uni(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))
    data = [i for i in data if i['article'] is not None]
    write_in_db(data)


def yahoo(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))

    for i in range(len(data)):
        data[i]['label'] = data[i]['label'][0]
        if data[i]['label'] == 'all':
            data[i]['label'] = None
        data[i]['time'] = data[i]['time'].split(
            'T')[0] + ' ' + ':'.join(data[i]['time'].split('T')[1].split(':')[:-1])
    write_in_db(data)


def storm(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))
    write_in_db(data)


def cna(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))
    for i in range(len(data)):
        data[i]['time'] = data[i]['time'].replace('/', '-')
    write_in_db(data)


def ntdtv(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))
    write_in_db(data)


def ltn(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))
    for i in range(len(data)):
        data[i]['time'] = data[i]['time'].replace('/', '-')
    write_in_db(data)


def epochtimes(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))
    for i in range(len(data)):
        data[i]['time'] = data[i]['time'].split(
            'T')[0] + ' ' + ':'.join(data[i]['time'].split('T')[1].split(':')[:-2])
    write_in_db(data)


def apple(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))
    for i in range(len(data)):
        data[i]['time'] = data[i]['time'].split(
            'T')[0] + ' ' + ':'.join(data[i]['time'].split('T')[1].split(':')[:-1])
    write_in_db(data)


def TVBS(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))
    for i in range(len(data)):
        data[i]['time'] = data[i]['time'].replace('/', '-')
    write_in_db(data)


def ettoday(filename):
    data = json.load(open(filename, 'r', encoding='utf8'))
    for i in range(len(data)):
        data[i]['time'] = data[i]['time'].replace('/', '-')
    write_in_db(data)

def clear_dictionarys(dir_path):
    shutil.rmtree(dir_path)
    os.mkdir(dir_path)

if __name__ == '__main__':
    create_table()
    dir_path = [
        'crawlers/data/chinatimes',
        'crawlers/data/setn',
        'crawlers/data/uni',
        'crawlers/data/yahoo',
        'crawlers/data/storm',
        'crawlers/data/cna',
        'crawlers/data/ntdtv',
        'crawlers/data/apple',
        'crawlers/data/epochtimes',
        'crawlers/data/ltn',
        'crawlers/data/TVBS',
        'crawlers/data/ettoday'
    ]
    func = [
        chinatimes,
        setn,
        uni,
        yahoo,
        storm,
        cna,
        ntdtv,
        apple,
        epochtimes,
        ltn,
        TVBS,
        ettoday
    ]
    for i, p in enumerate(dir_path):
        for filename in tqdm(os.listdir(p)):
            file_path = os.path.join(p, filename)
            func[i](file_path)
    for i in dir_path:
        clear_dictionarys(i)

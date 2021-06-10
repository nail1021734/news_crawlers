import multiprocessing as mp
import os
import time
import datetime as dt

def file_run(filename):
    try:
        os.system(f"python crawlers/{filename}")
    except:
        print(f'File `{filename}` run time error.')

def crawler_Runner():
    pool = mp.Pool(None)
    crawler_names = os.listdir("crawlers")
    for filename in crawler_names:
        if filename != 'data':
            pool.apply_async(file_run, args=(filename,))
    pool.close()
    pool.join()

if __name__ == '__main__':
    while True:
        print(dt.datetime.now().strftime('%Y%d%m'), 'Crawlered')
        crawler_Runner()
        os.system("python create_db.py")
        time.sleep(86400)
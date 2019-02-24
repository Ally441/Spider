Author = 'Liu Lei'

import requests
import re
import json
import time
import pymongo
from requests.exceptions import RequestException

def get_one_page(url):#获取页面
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text;
        return None
    except RequestException:
        return None


def parse_one_page(html):#分析获取的页面信息
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S)
    results = re.findall(pattern,html)
    for result in results:
        yield {
           'index': result[0],
            'picture_address': result[1],
            'movie_name': result[2],
            'movie_stars': result[3].strip()[3:],
            'time':result[4].strip()[5:],
             'score':result[5].strip()+result[6].strip()
         }

def write_to_file(content):#写入文件
    with open('result.txt','a',encoding = 'utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')



def main(offset):#获取分页
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
        movie_top_list.insert_one(item)


if __name__ == '__main__':
    client = pymongo.MongoClient('localhost',27017)
    movie_top_100 = client['movie_top_100']
    movie_top_list = movie_top_100['movie_top_list']
    for i in range(10):
        main(offset = i * 10)
        time.sleep(1)
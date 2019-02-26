Author = 'Liu Lei'

import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool


def get_page(offset):#获取json
    params = {
        'aid':'24',
        'app_name':'web_search',
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'en_qc':'1',
        'cur_tab':'1',
        'from':'search_tab',
        'pd':'synthesis'
    }
    url = 'https://www.toutiao.com/api/search/content/?'+urlencode(params)
    try:
        response = requests.get(url)
        if(response.status_code == 200):
            return response.json()
    except requests.ConnectionError:
        return None;

def get_images(json):#分析json,获取图片地址和标题
    if json.get('data'):
        for items in json.get('data'):
            title = items.get('title')
            images = items.get('image_list')
            if images == None:
                pass
            else:
                for image in images:
                    yield{
                        'title':title,
                        'image': image.get('url')
                    }
    else:
        print('none')

def save_image(item):#保存文件
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
            else:
                print('Already Download',file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')



if __name__ == '__main__':
    for i in range(1,11):
        jsons = get_page(i*20)
        groups = get_images(jsons)
        for group in groups:
            save_image(group)




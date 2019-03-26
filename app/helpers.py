# coding:utf-8
import requests
import base64
import os
import json
import random
from datetime import date
from datetime import timedelta
import time
from configparser import ConfigParser


def img_to_base64(full_img):
    if not os.path.exists(full_img):
        return None

    with open(full_img, 'rb') as f:
        return str(base64.b64encode(f.read()), encoding='utf-8')


def match(full_img1, full_img2):
    b1 = img_to_base64(full_img1)
    b2 = img_to_base64(full_img2)
    body = [{'image': b1, 'image_type': 'BASE64', 'face_type': 'CERT', 'quality_control': 'NONE',
             'liveness_control': 'NONE'},
            {'image': b2, 'image_type': 'BASE64', 'face_type': 'LIVE', 'quality_control': 'NONE',
             'liveness_control': 'NONE'}]

    url = 'http://192.168.8.202:8300/face-api/v3/face/match?appid=app01'
    # url = 'http://58.209.250.207:3389/face-api/v3/face/match?appid=app01'
    resp = requests.post(url=url, json=body, headers={'Content-Type': 'application/json'})
    print(resp.text)
    return resp.text


def liveness(full_img):
    b = img_to_base64(full_img)

    body = [{'image': b, 'image_type': 'BASE64', 'face_field': ''}]
    url = 'http://192.168.8.202:8300/face-api/v3/face/liveness?appid=app01'
    # url = 'http://58.209.250.207:3389/face-api/v3/face/liveness?appid=app01'
    resp = requests.post(url=url, json=body, headers={'Content-Type': 'application/json'})
    return resp.text


# 身份证号生成器
def gen_ic_num(gender):
    area_dict = {}
    check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
    id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    file_path = os.path.join(os.getcwd(), 'app', 'area_dict.txt')
    with open(file_path, 'r', encoding='utf-8') as ff:
        temp_str = ff.read()
        area_dict = json.loads(temp_str)

    datestring = str(
        date(date.today().year - random.randrange(18, 70), 1, 1) + timedelta(days=random.randint(0, 364))).replace('-',
                                                                                                                   '')
    rd = random.randint(0, 999)
    gender_num = ''

    if gender == 0:
        gender_num = rd if rd % 2 == 0 else rd + 1
    else:
        gender_num = rd if rd % 2 == 1 else rd - 1
    rnd_area = '%s' % random.choice(list(area_dict.keys()))
    result = str(rnd_area) + datestring + str(gender_num).zfill(3)
    ic_num = result + str(check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in result])]) % 11])

    return ic_num


# 日期转时间戳
def date_to_timestamp(str_date):
    time_arr = time.strptime(str_date, '%Y-%m-%d %H:%M:%S')
    return time_arr


# 读取配置文件
def get_conf(section, item):
    conf = ConfigParser()
    conf.read(os.path.join(os.getcwd(), 'app/application.conf'))
    return conf.get(section, option=item)


# 接口获取的二进制图片转换成base64编码
def get_base64_by_url(url):
    resp = requests.get(url)
    bin_img = resp.content
    b64_img = base64.b64encode(bin_img)

    return str(b64_img, encoding='utf-8')


if __name__ == '__main__':
    url = 'http://192.168.2.212:8080/tce-blobStore/blobStoreApi/getBlob?tableName=image&id=head-023023_1552985164_20190319164604_00000000&store=hbase&dataType=1&space=jsiot'
    ii = get_base64_by_url(url)
    print(ii)

# coding:utf-8
import requests
import base64
import os


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

    url = 'http://58.209.250.207:3389/face-api/v3/face/match?appid=app01'
    resp = requests.post(url=url, json=body, headers={'Content-Type': 'application/json'})
    print(resp.text)
    return resp.text


def liveness(full_img):
    b = img_to_base64(full_img)

    body = [{'image': b, 'image_type': 'BASE64', 'face_field': ''}]
    url = 'http://58.209.250.207:3389/face-api/v3/face/liveness?appid=app01'
    resp = requests.post(url=url, json=body, headers={'Content-Type': 'application/json'})
    return resp.text

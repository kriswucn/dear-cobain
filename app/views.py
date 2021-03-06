from app import app
from flask import render_template
from flask import request
import os
from app.helpers import match as mth
from app.helpers import liveness as lv
from app.helpers import gen_ic_num
from app.helpers import get_conf
from app.helpers import get_base64_by_url
import json
from flask import jsonify
import base64
import time
import datetime
import requests
import uuid


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='首页')


# 人证比对
@app.route('/match', methods=['GET', 'POST'])
def match():
    if request.method == 'GET':
        return render_template('match.html', title='人证比对')
    elif request.method == 'POST':
        return render_template('match.html', title='POST')


# 活体检测
@app.route('/liveness', methods=['GET', 'POST'])
def liveness():
    if request.method == 'GET':
        return render_template('liveness.html', title='活体检测')


# 图片库测试
@app.route('/imglib', methods=['GET', 'POST'])
def imglib():
    if request.method == 'GET':
        return render_template('imglib.html', title='图片库测试')


# base64转图片
@app.route('/b64toimg', methods=['GET', 'POST'])
def b64toimg():
    if request.method == 'GET':
        return render_template('b64toimg.html', title='Base64转图片')
    elif request.method == 'POST':
        b64 = request.form.get('b64')
        # 转换成图片并保存
        try:
            img_name = '%s.jpg' % int(time.time())
            img_path = os.path.join(os.getcwd(), 'app/static/resources', img_name)
            with open(img_path, 'wb') as ff:
                ff.write(base64.b64decode(b64))
            return jsonify({'msg': "transfer successfully.", "img_path": 'static/resources/%s' % img_name})
        except:
            return jsonify({'msg': 'transfer failed.', "img_path": "static/resources/null.jpg"})


# 图片转base64
@app.route('/imgtob64', methods=['GET', 'POST'])
def imgtob64():
    if request.method == 'GET':
        return render_template('imgtob64.html', title="图片转base64")
    elif request.method == 'POST':
        # return jsonify({'msg': "transfer successfully.", "base64": 'BASE64CODE.........'})
        img_file = request.files['file_img']
        img_file_path = os.path.join(os.getcwd(), r'app/static/resources', img_file.filename)
        img_file.save(img_file_path)
        # 转换base64
        b64_code = ''
        with open(img_file_path, 'rb') as ff:
            b64_code = str(base64.b64encode(ff.read()), encoding='utf-8')
        return jsonify({'msg': "transfer successfully.", "base64": b64_code})


# json字符串格式化
@app.route('/format', methods=['GET'])
def format_json():
    if request.method == 'GET':
        return render_template('format.html', title='Json字符串格式化')


# 身份证生成
@app.route('/icnum', methods=['GET', 'POST'])
def ic_num():
    if request.method == 'GET':
        return render_template('icnum.html', title='身份证号生成')
    elif request.method == 'POST':
        gender = request.values.get('sel_gender')
        i_gender = int(gender)
        num = gen_ic_num(i_gender)
        return render_template('icnum.html', title='身份证号生成', ic_num=num)


# 时间时间戳
@app.route('/tsconvert', methods=['GET'])
def ts_convert():
    if request.method == 'GET':
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ts = time.time()
        return render_template('tsconvert.html', title='时间时间戳转换', j={"dt": dt, "ts": ts})


# 图片服务显示
@app.route('/showimg', methods=['GET', 'POST'])
def show_img():
    if request.method == 'GET':
        return render_template('showimg.html', title='图片显示')
    elif request.method == 'POST':
        img_id = request.values.get('img_id')
        url = 'http://192.168.2.210:8081/tce-save2hbase/image/getImage?space=s1&tableName=tce_image&id=%s' % img_id
        resp = requests.get(url)
        save_path = os.path.join(os.getcwd(), 'app/static/resources', img_id + '.jpg')

        with open(save_path, 'wb') as ff:
            ff.write(resp.content)

        rel_path = '/static/resources/%s.jpg' % img_id

        return render_template('showimg.html', title='图片显示', img_path=rel_path)


# 缩略图显示
@app.route('/showthumb', methods=['GET', 'POST'])
def show_thumb():
    if request.method == 'GET':
        return render_template('showthumb.html', title='图片显示')
    elif request.method == 'POST':
        img_id = request.values.get('img_id')
        url = 'http://192.168.2.210:8081/tce-save2hbase/image/getImageSmall?space=s1&tableName=tce_image&id=%s' % img_id
        resp = requests.get(url)
        save_path = os.path.join(os.getcwd(), 'app/static/resources', img_id + '_s.jpg')

        with open(save_path, 'wb') as ff:
            ff.write(resp.content)

        rel_path = '/static/resources/%s_s.jpg' % img_id

        return render_template('showthumb.html', title='图片显示', img_path=rel_path)


# 生成uuid
@app.route('/uuid', methods=['GET'])
def get_uuid():
    if request.method == 'GET':
        str_uuid = str.replace(str(uuid.uuid4()), '-', '')
        return render_template('uuid.html', title='UUID', uid=str_uuid)


@app.route('/blob', methods=['GET', 'POST'])
def get_blob():
    # 获取blob配置文件
    blob_conf = {}
    blob_conf.update({'baseUrl': get_conf('blob', 'base_url')})
    blob_conf.update({'space': get_conf('blob', 'space')})
    blob_conf.update({'tableName': get_conf('blob', 'table_name')})
    blob_conf.update({'dataType': get_conf('blob', 'data_type')})
    blob_conf.update({'store': get_conf('blob', 'store')})
    blob_conf.update({'id': ''})

    if request.method == 'GET':
        return render_template('blob.html', title='大数据查看器', blob_conf=blob_conf)
    elif request.method == 'POST':
        img_id = request.form.get('txt_id')
        blob_conf.update({'id': img_id})

        base_url = get_conf('blob', 'base_url')
        blob_conf.pop('baseUrl')
        resp = requests.get(url=base_url, params=blob_conf)
        b64_img = str(base64.b64encode(resp.content), encoding='utf-8')
        blob_conf.update({'baseUrl': get_conf('blob', 'base_url')})
        return render_template('blob.html', title=img_id, blob_conf=blob_conf,
                               b64_img='data:image/png;base64,%s' % b64_img)
        # pass

    # ========================================================================== #
    # ajax接口
    @app.route('/api/match', methods=['POST'])
    def api_match():
        if request.method == 'POST':
            idcard = request.files['file_idcard']
            live = request.files['file_live']
            idcard_path = os.path.join(os.getcwd(), r'app/static/resources', idcard.filename)
            live_path = os.path.join(os.getcwd(), r'app/static/resources', live.filename)
            idcard.save(idcard_path)
            live.save(live_path)
            # 调用接口，第一个参数是身份证地址，第二个参数是现场图片
            start_time = datetime.datetime.now()
            result = mth(idcard_path, live_path)
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            d_result = json.loads(result)

            # 判断是否比对成功
            error_code = d_result.get('error_code')

            if error_code == 0:
                score = d_result.get('result').get('score')
                return jsonify({'msg': score, 'duration': (duration.microseconds / 1000)})
            else:
                error_msg = d_result.get('error_msg')
                print(error_msg)
                return jsonify({'msg': error_msg})

    @app.route('/api/liveness', methods=['POST'])
    def api_liveness():
        if request.method == 'POST':
            img_file = request.files['file_img']
            img_file_path = os.path.join(os.getcwd(), r'app/static/resources', img_file.filename)
            img_file.save(img_file_path)
            start_time = datetime.datetime.now()
            result = lv(img_file_path)
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            d_result = json.loads(result)
            # 判断是否认证成功
            error_code = d_result.get('error_code')

            if error_code == 0:
                score = d_result.get('result').get('face_liveness')
                return jsonify({'msg': score, 'duration': (duration.microseconds / 1000)})
            else:
                error_msg = d_result.get('error_msg')
                print(error_msg)
                return jsonify({'msg': error_msg})

    @app.route('/api/format', methods=['POST'])
    def json_format():
        if request.method == 'POST':
            src_json = request.form.get('j')
        temp_dict = json.loads(src_json)
        return jsonify({'dest_json': json.dumps(temp_dict, indent=4)})

    @app.route('/api/icnum', methods=["POST"])
    def api_icnum():
        if request.method == 'POST':
            gender = request.values.get('sel_gender')
            i_gender = int(gender)
            num = gen_ic_num(i_gender)
            return jsonify({'ic_num': num})

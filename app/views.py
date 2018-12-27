from app import app
from flask import render_template
from flask import request
import os
from app.helpers import match as mth
from app.helpers import liveness as lv
import json
from flask import jsonify


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='首页')


@app.route('/match', methods=['GET', 'POST'])
def match():
    if request.method == 'GET':
        return render_template('match.html', title='人证比对')
    elif request.method == 'POST':
        return render_template('match.html', title='POST')


@app.route('/liveness', methods=['GET', 'POST'])
def liveness():
    if request.method == 'GET':
        return render_template('liveness.html', title='活体检测')


# 接口
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
        result = mth(idcard_path, live_path)
        d_result = json.loads(result)

        # 判断是否比对成功
        error_code = d_result.get('error_code')

        if error_code == 0:
            score = d_result.get('result').get('score')
            return jsonify({'msg': score})
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
        result = lv(img_file_path)
        d_result = json.loads(result)
        # 判断是否认证成功
        error_code = d_result.get('error_code')

        if error_code == 0:
            score = d_result.get('result').get('face_liveness')
            return jsonify({'msg': score})
        else:
            error_msg = d_result.get('error_msg')
            print(error_msg)
            return jsonify({'msg': error_msg})

from app import app
from flask import render_template
from flask import request
import time
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


# 接口
@app.route('/api/match', methods=['POST'])
def api_match():
    if request.method == 'POST':
        # data = request.get_data().decode('utf-8')
        # uid = json.loads(data).get('file_idcard')
        # print(uid)
        # dd = {'code': 200, 'score': uid, 'time': (time.time() * 1000)}
        # return jsonify(dd)
        f1 = request.files['file']

        return jsonify({'score': 0.97})

from app import app
from flask import render_template
from flask import request


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
    pass

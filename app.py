from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bs4 import BeautifulSoup

app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.dbmemo


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    image_url = request.form['imageURL']
    title = request.form['title']
    title_url = request.form['titleURL']
    content = request.form['content']
    comment = request.form['comment']

    # 2. meta tag를 스크래핑하기

    # 3. mongoDB에 데이터 넣기
    db.articles.insert_one({'image_url': image_url, 'title': title, 'title_url': title_url, 'content': content, 'comment' : comment})
    return jsonify({'result': 'success', 'msg': 'Memo가 등록되었습니다.'})


@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.articles.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'articles': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
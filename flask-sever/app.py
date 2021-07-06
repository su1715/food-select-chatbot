import urllib
import json
import os
from flask import Flask, request, make_response, jsonify, url_for, render_template, redirect
from flask_jwt_extended import *
from models import db
from models import User

# initialize the flask app
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    JWT_SECRET_KEY="food-selector"
)
jwt = JWTManager(app)
# default route


@app.route('/')
def index():
    print("hello")
    return 'Hello World..........'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return "GET으로 입력되었습니다"
    else:
        data = request.get_json(force=True)
        userId = data['userId']
        username = data['username']
        password = data['password']
        repassword = data['repassword']

        if not (userId and username and password and repassword):
            return jsonify(result="fail", error="모두 입력해주세요.")
        elif password != repassword:
            return jsonify(result="fail", error="비밀번호 확인이 일치하지 않습니다.")
            # TODO: 원래 있는 아이디인지 확인하기
        else:  # 모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            cnt = User.query.filter_by(userid=userId).count()
            if(cnt > 0):
                return jsonify(result="fail", error="이미 존재하는 아이디 입니다.")
            else:
                user = User()
                user.password = password  # models의 User 클래스를 이용해 db에 입력한다.
                user.userid = userId
                user.username = username
                db.session.add(user)
                db.session.commit()
                access_token = create_access_token(
                    identity=userId, expires_delta=False)
                return jsonify(result="success", token=access_token)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return "GET으로 입력되었습니다"
    else:
        data = request.get_json(force=True)
        userId = data['userId']
        password = data['password']
        # db에 같은 정보 있는지 확인
        cnt = User.query.filter_by(userid=userId).filter_by(
            password=password).count()
        if cnt:
            access_token = create_access_token(
                identity=userId, expires_delta=False)
            return jsonify(result="success", token=access_token)
        else:
            return jsonify(result="fail", error="계정정보가 일치하지 않습니다.")

# create a route for webhook


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    country = req['queryResult']['parameters']['country']
    ingredient = req['queryResult']['parameters']['ingredient']
    temperature = req['queryResult']['parameters']['temperature']
    spicy = req['queryResult']['parameters']['spicy']
    simple = req['queryResult']['parameters']['simple']
    return {
        "fulfillmentText": country+ingredient+temperature+spicy+simple+' 음식 준비해드리겠습니다',
        "source": 'webhook'
    }


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(
        __file__))  # database 경로를 절대경로로 설정함
    dbfile = os.path.join(basedir, 'db.sqlite')  # 데이터베이스 이름과 경로
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # 여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
    # True하면 warrnig메시지 유발,
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # 초기화 후 db.app에 app으로 명시적으로 넣어줌
    db.app = app
    db.create_all()   # 이 명령이 있어야 생성됨. DB가

    app.run(host='127.0.0.1', port=5000, debug=True)

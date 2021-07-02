import urllib
import json
import os
from flask import Flask, request, make_response, jsonify, url_for, render_template, redirect
from models import db
from models import User

# initialize the flask app
app = Flask(__name__)

# default route


@app.route('/')
def index():
    return 'Hello World..........'


@app.route('/register', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 회원정보 생성
        userid = request.form.get('userid')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password)  # 들어오나 확인해볼 수 있다.

        if not (userid and username and password and re_password):
            return "모두 입력해주세요"
        elif password != re_password:
            return "비밀번호를 확인해주세요"
        # TODO: 원래 있는 아이디인지 확인하기
        else:  # 모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            user = User()
            user.password = password  # models의 User 클래스를 이용해 db에 입력한다.
            user.userid = userid
            user.username = username
            db.session.add(user)
            db.session.commit()
            return "회원가입 완료"

        return redirect('/')


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


@app.route('/structure', methods=['POST'])
def structure():
    """
    if(DB에 없으면)
        DB 생성
    country = req['queryResult']['parameters']['country']
    ingredient = req['queryResult']['parameters']['ingredient']
    temperature = req['queryResult']['parameters']['temperature']
    spicy = req['queryResult']['parameters']['spicy']
    simple = req['queryResult']['parameters']['simple']


    """


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

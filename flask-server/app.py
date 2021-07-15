import urllib
import json
import os
from flask import Flask, request, make_response, jsonify, url_for, render_template, redirect
from flask_jwt_extended import *
from models import db
from models import User
from path import credential_path

# initialize the flask app
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    JWT_SECRET_KEY="food-selector"
)
jwt = JWTManager(app)
project_id = "newagent-rrpl"
session_id = "newagent-rrpl"
#credential_path = 'C:\\Users\\pcrys\\Desktop\\food_git\\food-select-chatbot\\frontend\\newagent-rrpl-cc1bf222c237.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Dialogflow API


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(
            text=text['text'], language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(
            response.query_result.fulfillment_text))

        return jsonify(result="success", reply=response.query_result.fulfillment_text)

# default route


@app.route('/')
def index():
    return "Hello"


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


@app.route('/message', methods=['POST'])
def message():
    texts = []
    data = request.get_json(force=True)
    message = data['message']
    print(message)
    texts.append(message)
    return detect_intent_texts(project_id, session_id, texts, "ko")


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

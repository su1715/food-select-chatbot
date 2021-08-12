import urllib
import json
import os
import sqlite3
from sqlite3.dbapi2 import connect
from flask import Flask, request, make_response, jsonify, url_for, render_template, redirect
from flask_jwt_extended import *
from google.cloud.dialogflow_v2.types import session
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
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Dialogflow API


def detect_intent_texts(project_id, session_id, texts, language_code, location):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text['text'] += " "
        text['text'] += str(location['latitude'])+" " + \
            str(location['longitude'])
        text_input = dialogflow.TextInput(
            text=text['text'], language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        # print("Fulfillment text: {}".format(
        #     response.query_result.fulfillment_text))
        # print("Fulfillment messages: {}".format(
        #     response.query_result.fulfillment_messages))

        reply = []
        for message in response.query_result.fulfillment_messages:
            reply.append(message.text.text[0])

        return jsonify(result="success", reply=reply)

# default route


@app.route('/')
def index():
    return "Hello"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return "GET으로 입력되었습니다"
    else:
        conn = sqlite3.connect("foodDic.db")
        cur = conn.cursor()
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
            cnt = cur.execute(
                "SELECT count(*) From User Where userid=?", (userId,)).fetchone()[0]
            if(cnt > 0):
                conn.commit()
                conn.close()
                return jsonify(result="fail", error="이미 존재하는 아이디 입니다.")
            else:
                cur.execute("Insert into User values (?, ?, ?)",
                            (userId, username, password))
                print("userInfo has been inserted.")
                conn.commit()
                conn.close()
                #access_token = create_access_token(identity=userId, expires_delta=False)
                return jsonify(result="success", token=userId)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return "GET으로 입력되었습니다"
    else:
        conn = sqlite3.connect("foodDic.db")
        cur = conn.cursor()
        data = request.get_json(force=True)
        userId = data['userId']
        password = data['password']
        # db에 같은 정보 있는지 확인
        cnt = cur.execute(
            "SELECT count(*) From User Where userid=? AND password=?", (userId, password,))
        conn.commit()
        conn.close()
        if cnt:
            #access_token = create_access_token(identity=userId, expires_delta=False)
            return jsonify(result="success", token=userId)
        else:
            return jsonify(result="fail", error="계정정보가 일치하지 않습니다.")


@app.route('/message', methods=['POST'])
def message():
    texts = []
    data = request.get_json(force=True)
    message = data['message']
    location = data['location']
    userId = data['userId']
    print("아이디:{} \n메세지: {} \n위치: {}".format(
        userId, message['text'], location))
    texts.append(message)
    session_id = userId
    return detect_intent_texts(project_id, session_id, texts, "ko", location)


# create a route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    from food_filter import filter

    req = request.get_json(force=True)
    userId = req['session'].split('/')[-1]
    country = req['queryResult']['parameters']['country']
    ingredient = req['queryResult']['parameters']['ingredient']
    temperature = req['queryResult']['parameters']['temperature']
    spicy = req['queryResult']['parameters']['spicy']
    simple = req['queryResult']['parameters']['simple']
    latitude = req['queryResult']['parameters']['latitude']
    longitude = req['queryResult']['parameters']['longitude']
    if(isinstance(latitude, list)):
        latitude = latitude[0]
    if(isinstance(longitude, list)):
        longitude = longitude[0]
    print("session:{}".format(userId))
    print("parameter:{} {} {} {} {} {} {}".format(
        country, ingredient, temperature, spicy, simple,  latitude, longitude))
    fulfillmentMessages = filter(country, temperature, spicy, simple,
                                 ingredient, latitude, longitude)
    return {
        "fulfillmentMessages": fulfillmentMessages,
        "source": 'webhook'
    }


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

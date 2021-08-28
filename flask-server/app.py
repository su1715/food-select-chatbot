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


def detect_intent_texts(project_id, session_id, texts, language_code, location):
    # Dialogflow API
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()
    session_id += "+{}+{}".format(location['latitude'], location['longitude'])
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
            "Detected intent: {} (confidence: {})".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )

        reply = []
        for message in response.query_result.fulfillment_messages:
            reply.append(message.text.text[0])

        return jsonify(result="success", reply=reply)


@app.route('/')
def index():
    return "Hello"


@app.route('/delete_info', methods=['GET', 'POST'])
def delete():
    conn = sqlite3.connect("foodDic.db")
    cur = conn.cursor()
    data = request.get_json(force=True)
    userId = data['userId']
    cur.execute("DELETE FROM User_history WHERE userid=?", (userId,))
    conn.commit()
    conn.close()
    return jsonify(result="delete")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
    else:
        cnt = cur.execute(
            "SELECT count(*) From User Where userid=?", (userId,)).fetchone()[0]
        if(cnt > 0):
            conn.commit()
            conn.close()
            return jsonify(result="fail", error="이미 존재하는 아이디 입니다.")
        else:
            cur.execute("Insert into User values (?, ?, ?)",
                        (userId, username, password))
            conn.commit()
            conn.close()
            return jsonify(result="success", token=userId)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
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
        return jsonify(result="success", token=userId)
    else:
        return jsonify(result="fail", error="계정정보가 일치하지 않습니다.")


@app.route('/message', methods=['POST'])
def message():
    data = request.get_json(force=True)
    message = data['message']
    location = data['location']
    userId = data['userId']
    print("=======message=======")
    print("아이디:{} \n메세지: {} \n위치: {}".format(
        userId, message['text'], location))
    texts = []
    texts.append(message)
    session_id = userId
    return detect_intent_texts(project_id, session_id, texts, "ko", location)


@app.route('/webhook', methods=['POST'])
def webhook():
    print("=======webhook=======")
    from food_filter import filter
    conn = sqlite3.connect("foodDic.db")
    cur = conn.cursor()

    req = request.get_json(force=True)

    session = req['session'].split('/')[-1]
    userId = session.split('+')[-3]
    latitude = float(session.split('+')[-2])
    longitude = float(session.split('+')[-1])
    intent = req['queryResult']['intent']['displayName']
    print("intent:{}".format(intent))

    if(intent == "restart"):
        cur.execute("DELETE FROM User_history WHERE userid = ?", (userId,))
        conn.commit()
        conn.close()
        from food_filter import makeDic
        fulfillmentMessages = []
        fulfillmentMessages.append(makeDic("어떤 음식을 먹어볼까요?"))
        return {
            "fulfillmentMessages": fulfillmentMessages,
            "source": 'webhook'
        }

    else:
        if(intent == "food_selector"):
            country = req['queryResult']['parameters']['country']
            ingredient = req['queryResult']['parameters']['ingredient']
            temperature = req['queryResult']['parameters']['temperature']
            spicy = req['queryResult']['parameters']['spicy']
            simple = req['queryResult']['parameters']['simple']
            print("session:{}, userId:{}, latitude:{}, longitude:{}".format(
                session, userId, latitude, longitude))
            print("parameter:{} {} {} {} {} {} {}".format(
                country, ingredient, temperature, spicy, simple, latitude, longitude))

            # parameter를 받는다
            # User_history table에 해당 user가 존재하는지 확인한다
            cnt = cur.execute(
                "SELECT count(*) From User_history Where userid=?", (userId,)).fetchone()[0]
            # 존재하는경우
            if(cnt):
                # sql 문 따로 만들어줘야함
                sql = "Update User_history SET search_index = 0,"
                params = []
                if(country):
                    sql += "country=?,"
                    params.append(country)
                if(ingredient):
                    sql += "ingredient=?,"
                    params.append(ingredient)
                if(temperature):
                    sql += "temperature=?,"
                    params.append(temperature)
                if(spicy):
                    sql += "spicy=?,"
                    params.append(spicy)
                if(simple):
                    sql += "simple=?,"
                    params.append(simple)

                sql = sql[0:-1]  # 쉼표제거
                sql += " WHERE userid = ?"
                params.append(userId)

                # 파라미터 할당 추가
                params_tuple = tuple(params)
                cur.execute(sql, params_tuple)
                conn.commit()

            # 존재하지 않는경우
            else:
                cur.execute(
                    """INSERT INTO User_history VALUES (?,0,?,?,?,?,?)""",
                    (userId, country, ingredient, temperature, spicy, simple,))
                conn.commit()

    # User_history table 이용하여 sql 문 만들기
    cur.execute("""
        SELECT search_index, country, temperature, spicy, simple, ingredient
        FROM User_history
        WHERE userid = ?
    """, (userId,))

    result = cur.fetchone()
    search_index = result[0]
    country = result[1]
    temperature = result[2]
    spicy = result[3]
    simple = result[4]
    ingredient = result[5]

    print("------- User_history 검색결과 -------")
    print("search_index:{}, country:{}, temperature:{}, spicy:{}, simple:{}, ingredient:{}".format(
        search_index, country, temperature, spicy, simple, ingredient))

    conn.commit()
    conn.close()

    fulfillmentMessages = filter(userId, search_index, country, temperature, spicy, simple,
                                 ingredient, latitude, longitude)

    return {
        "fulfillmentMessages": fulfillmentMessages,
        "source": 'webhook'
    }


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

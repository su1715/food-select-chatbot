import sqlite3
import requests
import json


def stringify_where(country, temperature, spicy, simple, ingredient):
    where = ""
    # country
    if(country == "한식"):
        where = where+"korea = 1 AND "
    elif(country == "일식"):
        where = where+"japan = 1 AND "
    elif(country == "중식"):
        where = where+"china = 1 AND "
    elif(country == "양식"):
        where = where+"occident = 1 AND "
    elif(country == "베트남식"):
        where = where+"vietnam = 1 AND "
    elif(country == "대만식"):
        where = where+"taiwan = 1 AND "
    elif(country == "태국식"):
        where = where+"thailand = 1 AND "
    elif(country == "멕시코식"):
        where = where+"mexico = 1 AND "
    elif(country == "터키식"):
        where = where+"turkey = 1 AND "
    elif(country == "동남아식"):
        where = where+"(taiwan=1 or vietnam=1 or thailand=1) AND "

    # temperature
    if(temperature == "따뜻한"):
        where = where + "hot = 1 AND "
    elif(temperature == "차가운"):
        where = where + "cool = 1 AND "

    # spicy
    if(spicy == "매운"):
        where = where + "spicy = 1 AND "
    elif(spicy == "안매운"):
        where = where + "n_spicy = 1 AND "

    # simple
    if(simple == "간단"):
        where = where + "easy = 1 AND "

    # ingredient
    if(ingredient == "빵"):
        where = where + "bread = 1"
    elif(ingredient == "밥"):
        where = where + "rice = 1"
    elif(ingredient == "면"):
        where = where + "noodle = 1"
    elif(ingredient == "떡"):
        where = where + "rice_b = 1"
    elif(ingredient == "고기"):
        where = where + "meat = 1"
    elif(ingredient == "채소"):
        where = where + "veget = 1"
    elif(ingredient == "해물"):
        where = where + "sea_f = 1"
    elif(ingredient == "국"):
        where = where + "soup = 1"

    elif(ingredient == ""):  # AND 자르기
        where = where[0:-4]

    return where


def makeDic(string):  # dialogflow의 fulfillmentMessages 에 맞는 형식(dictionary)으로 바꿈
    dic = {}
    dic["text"] = {}
    dic["text"]["text"] = []
    dic["text"]["text"].append(string)
    return dic


def formatting(placeObj):  # 메시지 형식 (상호명, 주소, url)
    return "\n{}\n{}\n{}\n".format(
        placeObj['place_name'], placeObj['road_address_name'], placeObj['place_url'])


def search(queryString, latitude, longitude):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    params = {
        "category_group_code": "FD6",
        "x": str(longitude),
        "y": str(latitude),
        "radius": "2000",
        "sort": "accuracy",
        "query": queryString
    }
    headers = {"Authorization": "KakaoAK b9c2719470566bad75cd57b575bd57e4"}
    places = requests.get(url, headers=headers, params=params).json()[
        'documents']
    text = "{} 추천해드리겠습니다.\n".format(queryString)
    for i in range(3):
        if(len(places) > i):
            text += formatting(places[i])
        else:
            if(places == 0):
                text += queryString + "에 대한 결과가 없습니다."
            break
    return text


def queryFoodnames(userId, search_index, where, latitude, longitude):
    connection = sqlite3.connect("foodDic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM foodDicTable WHERE " + where)
    names = cursor.fetchall()
    for name in names:  # foodDictable 검색결과 출력
        print(name[0])

    fulfillmentMessages = []
    if (search_index == -1):
        fulfillmentMessages.append(makeDic("새로운 대화를 시작해주세요."))
        connection.close()
        return fulfillmentMessages

    for i in range(search_index, search_index + 3):
        if(i >= len(names)):
            break
        dic = makeDic(search(names[i][0], latitude, longitude))
        fulfillmentMessages.append(dic)

    if(i >= len(names)):
        fulfillmentMessages.append(
            makeDic("더 이상 검색 결과가 없습니다. 새로운 대화를 시작해주세요."))
        search_index = -1
    else:
        search_index += 3
    cursor.execute(
        "UPDATE User_history SET search_index = ? WHERE userid = ?", (search_index, userId,))

    connection.commit()
    connection.close()
    return fulfillmentMessages


def filter(userId, search_index, country, temperature, spicy, simple, ingredient, latitude, longitude):
    where = stringify_where(country, temperature, spicy, simple, ingredient)
    return queryFoodnames(userId, search_index, where, float(latitude), float(longitude))


def searchDirectry(list, latitude, longitude):
    fulfillmentMessages = []
    fulfillmentMessages.append(makeDic("랜덤으로 추천해드릴게요!"))
    connection = sqlite3.connect("foodDic.db")
    cursor = connection.cursor()
    print("searchDirectry")
    for i in list:
        cursor.execute("SELECT name FROM foodDicTable WHERE indexnum=?", (i,))
        name = cursor.fetchone()[0]
        print(name)
        dic = makeDic(search(name, latitude, longitude))
        fulfillmentMessages.append(dic)
    return fulfillmentMessages

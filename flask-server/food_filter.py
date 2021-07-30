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
    # elif(country == "베트남식"):
    #     where = where+"occident = 1 AND "
    # elif(country == "태국식"):
    #     where = where+"occident = 1 AND "
    # elif(country == "멕시코식"):
    #     where = where+"occident = 1 AND "
    # elif(country == "터키식"):
    #     where = where+"occident = 1 AND "

    # temperature
    if(temperature == "따뜻한"):
        where = where + "hot = 1 AND "
    elif(temperature == "차가운"):
        where = where + "cool = 1 AND "

    # spicy
    if(spicy == "매운"):
        where = where + "spicy = 1 AND "
    elif(spicy == "안 매운"):
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


def queryFoodnames(where, latitude, longitude):
    connection = sqlite3.connect("foodDic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM foodDicTable WHERE "+where)
    names = cursor.fetchall()
    # TODO: 해당하는 음식이 없을때 출력고려하기
    for name in names:
        print(name[0])
    # if(len(names) > 3):
    #     for i in range(3):
    #         search(names[i][0], latitude, longitude)
    # else:
    #     for name in names:  # TODO: 우선순위 고려해서 다음테이블로 검색,,,,
    #         search(name[0], latitude, longitude)

    connection.close()


def search(queryString, latitude, longitude):
    latNlon = [latitude, longitude]
    #latNlon = getLocation()
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    params = {
        "category_group_code": "FD6",
        "x": str(latNlon[1]),
        "y": str(latNlon[0]),
        "radius": "2000",
        "sort": "distance",
        "query": queryString
    }
    headers = {"Authorization": "KakaoAK b9c2719470566bad75cd57b575bd57e4"}
    places = requests.get(url, headers=headers, params=params).json()[
        'documents']
    # for place in places:
    #     print(place)
    return places[0]


def filter(country, temperature, spicy, simple, ingredient, latitude, longitude):
    where = stringify_where(country, temperature, spicy, simple, ingredient)
    queryFoodnames(where, float(latitude), float(longitude))
    # 아직은 queryIndexnum 과 상관 없이 족발 검색!
    return search("족발", float(latitude), float(longitude))

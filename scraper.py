import requests
from bs4 import BeautifulSoup
import sqlite3

DB = 'coursework'


def parseWeather():
    session = requests.Session()
    session.headers.update({
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    })

    url_parse = url_list()
    weather = []
    for url in url_parse:
        response = requests.get(url)
        parser = BeautifulSoup(response.text, 'html.parser')
        item = {}
        item['date'] = parser.select('li.swiper-slide.is-active div.swiper-slide__info div.c-swiper-slide--day__date')[0].text.strip()
        item['max_temp'] = parser.select('li.swiper-slide.is-active  div.c-swiper-slide--day__temp-info span.c-swiper-slide--day__temp-max')[0].text.strip()
        item['min_temp'] = parser.select('li.swiper-slide.is-active div.c-swiper-slide--day__temp-info span.u-text-size-extra-small')[1].text.strip()
        item['wind'] = parser.select('ul.c-weather-stats span.u-text-weight-medium')[3].text.strip()
        weather.append(item)
    try:
        with sqlite3.connect(DB) as con:
            cur = con.cursor()
            cur.execute('DROP TABLE IF EXISTS weather')
            cur.execute('CREATE TABLE IF NOT EXISTS weather (date TEXT, max_temp TEXT, min_temp TEXT,  wind TEXT);')
            for item in weather:
                cur.execute("INSERT INTO weather (date,max_temp,min_temp,wind) VALUES (?,?,?,?)",(item['date'],item['max_temp'],item['min_temp'],item['wind']) )
                con.commit()
    except Exception as e:
        con.rollback()
    finally:
        con.close()


    return weather


def url_list():
    url = "https://www.euronews.com/weather/africa/nigeria/kano?p={0}"
    urls= []
    for index in range(1,8):
        urls.append(url.format(index))
    return urls
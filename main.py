# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import csv
import random
from pygeocoder import Geocoder
import googlemaps
from argparse import ArgumentParser

detail=['うんち','うんち','うんち','うんち','うんち']
place=['金閣寺','銀閣寺','清水寺','三十三間堂','伏見稲荷大社']

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, URIAction, MessageAction, PostbackAction
)

# グローバル変数の宣言(最終的には使わないようにしたい)
address=999

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def gethms(duration):
    m,s = divmod(duration.seconds,60)
    h,m =divmod(m,60)
    return h,m,s

#名前から緯度経度をだす
def make_idokedo(spot):
    googleapikey=os.environ["GOOGLE_API_KEY"]
    gmaps = googlemaps.Client(key=googleapikey)
    result = gmaps.geocode(spot)
    lat = result[0]["geometry"]["location"]["lat"]
    lng = result[0]["geometry"]["location"]["lng"]
    return lat,lng

#出発地から目的地までの所要時間および距離
def make_kyori(lat,lng,lat2,lng2):
    googleapikey = os.environ["GOOGLE_API_KEY"]
    gmaps = googlemaps.Client(key=googleapikey)
    result = gmaps.distance_matrix(origins=(lat2,lng2),destinations=(lat,lng),mode='walking')
    distance = result['rows'][0]['elements'][0]['distance']['value']
    #distance += result['rows'][0]['elements'][0]['duration']['value']
    duration = result['rows'][0]['elements'][0]['duration']['value']
    h,m,s=gethms(duration)

    # if distance > 1000:
    #     distance = distance/1000
    #     distance = str(distance) + "km "
    # else:
    #     distance = str(distance) + "m "
    explanation = str(distance) + str(h) + "時" +str(m)+ "分" + str(s)"秒"
    return explanation

#言葉から、areaを探す。（未完）

#案内のurlをつくる（理想、未完）
def create_google_map_url(address,goal):
    google_map_url = 'http://maps.google.com/maps?'
    google_map_url += "saddr={}&daddr={}".format(address,goal)
    return google_map_url

#データを読み込み返す。
#今は全部データを読み込んでいるけど、最終的には、NumPy？やらpandasなどを使って、もうちょっと効率よくやろう。
def read_data():
    data=[]
    csvfile = "DSIGHT.csv"
    fin = open(csvfile, "r",encoding="utf-8")
    reader = csv.reader(fin)
    for row in reader:
        data.append(row)
    fin.close
    return data

def rundum_num():
    num = []
    for j in range(6):
        x = random.randrange(1, 650)
        num.append(x)
    return num

# カルーセルテンプレートメッセージ
#配列[行][列(3:名称,4:よみがな,5:通称名称,6:よみがな,7,内容概要...24:画像urlたぶん)]
#カルーセルテンプレートの段階で、URIActionに地図を乗っけちゃう
def make_carousel_template(address,lat,lng):
    data = read_data()
    num = rundum_num()
    URL = []
    lat2 , lng2 = make_idokedo(data[num[1]][3])
    explanation = make_kyori(lat,lng,lat2,lng2)

    for i in range(6):
        goal = str(data[num[i]][3])
        goal = goal.replace("　","")
        URL.append(create_google_map_url(address,goal))

    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=data[num[1]][24], #data[1][23],　#画像urlは入ってるけどなんか上手くいかない.
                    title=data[num[1]][3],
                    text=explanation,
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=data[num[1]][3]+'に行きたい',#合わせて変えたヨ
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text=data[num[1]][3]
                        ),
                        URIAction(
                            label='ここに行く！直接URL',
                            uri=URL[1]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=data[num[2]][24], #data[1][23],　#画像urlは入ってるけどなんか上手くいかない.
                    title=data[num[2]][3],
                    text=data[num[2]][4],
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=data[num[2]][3]+'に行きたい',#合わせて変えたヨ
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text=data[num[2]][3]
                        ),
                        URIAction(
                            label='ここに行く！直接URL',
                            uri=URL[2]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=data[num[3]][24], #data[1][23],　#画像urlは入ってるけどなんか上手くいかない.
                    title=data[num[3]][3],
                    text=data[num[3]][4],
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=data[num[3]][3]+'に行きたい',#合わせて変えたヨ
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text=data[num[3]][3]
                        ),
                        URIAction(
                            label='ここに行く！直接URL',
                            uri=URL[3]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=data[num[4]][24], #data[1][23],　#画像urlは入ってるけどなんか上手くいかない.
                    title=data[num[4]][3],
                    text=data[num[4]][4],
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=data[num[4]][3]+'に行きたい',#合わせて変えたヨ
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text=data[num[4]][3]
                        ),
                        URIAction(
                            label='ここに行く！直接URL',
                            uri=URL[4]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=data[num[5]][24], #data[1][23],　#画像urlは入ってるけどなんか上手くいかない.
                    title=data[num[5]][3],
                    text=data[num[5]][4],
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=data[num[5]][3]+'に行きたい',#合わせて変えたヨ
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text=data[num[5]][3]
                        ),
                        URIAction(
                            label='ここに行く！直接URL',
                            uri=URL[5]
                        )
                    ]
                )
            ]
        )
    )
    return carousel_template_message


# テキストメッセージイベントの場合の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #if (event.message.text[-1] = "g" :（理想、とりあえずきにしないで）
    #    content = make_guide_url(event.message.latitude,event.message.longitude,event.message.text)
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    global address
    if '近くの観光情報を教えて' in event.message.text:
        content = 'わかりました！位置情報を送ってください！'
        address=999
    elif address != 999 and 'に行きたい' in event.message.text:
        destination = event.message.text
        google_map_url = 'http://maps.google.com/maps?'
        google_map_url += "saddr={}&".format(address)
        google_map_url += "daddr={}".format(destination.rstrip('に行きたい'))
        content = google_map_url
        address=999
    elif 'について教えて！' in event.message.text:
        description = event.message.text
        description = description.rstrip('について教えて！')
        content = description
    else:
        data = read_data()
        for i in range(651):
          if event.message.text in data[i][3]:
                content = data[i][3] + ":" + "\n" + data[i][7]
                break
    line_bot_api.reply_message(
        event.reply_token,
            TextSendMessage(text=content)
    )

# 位置情報メッセージイベントの場合の処理
@handler.add(MessageEvent, message=LocationMessage)
def handle_image_message(event):
    global address
    address=event.message.address[13:]
    messages = make_carousel_template(address,event.message.latitude,event.message.longitude)
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text='近くの観光地はここです！'),
            messages
        ]
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

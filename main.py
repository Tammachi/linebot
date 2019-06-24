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

from argparse import ArgumentParser

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

#とりあえず表示するため、きにしないで
place=['金閣寺','銀閣寺','清水寺','三十三間堂','伏見稲荷大社']
detail=['うんち','うんち','うんち','うんち','うんち']

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

#言葉から、areaを探す。（未完）
def spot_data():
    data = read_data()

#案内のurlをつくる（理想、未完）
def make_guide_url(route_search_latitude,route_search_longitude,placename):
    google_map_url = 'http://maps.google.com/maps?'
    google_map_url += "saddr={},{}&".format(route_search_latitude,route_search_longitude)
    google_map_url += "daddr={}".format(placename)
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

# カルーセルテンプレートメッセージ
#配列[行][列(3:名称,4:よみがな,5:通称名称,6:よみがな,7,内容概要...23:画像url)]
def make_carousel_template():
    data = read_data()
    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://ja.kyoto.travel/resource/tourism/sight/photo/mimon01C/C069.jpg', #data[1][23],　#画像urlは入ってるけどなんか上手くいかない。直接urlを張っても動かないからサイズかな？
                    title=data[1][3],
                    text=data[1][4],
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=data[1][3],
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text='open1'
                        ),
                        URIAction(
                            label='uri1',
                            uri='http://example.com/1'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/3/35/Kiyomizu_Temple_-_01.jpg',
                    title=data[4][3],
                    text=data[4][4],
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=place[1],
                            data='action=buy&itemid=2'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text='open2'
                        ),
                        URIAction(
                            label='uri2',
                            uri='http://example.com/2'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/3/35/Kiyomizu_Temple_-_01.jpg',
                    title=place[2],
                    text=detail[2],
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=place[2],
                            data='action=buy&itemid=3'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text='open3'
                        ),
                        URIAction(
                            label='uri3',
                            uri='http://example.com/3'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/3/35/Kiyomizu_Temple_-_01.jpg',
                    title=place[3],
                    text=detail[3],
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=place[3],
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text='open3'
                        ),
                        URIAction(
                            label='uri3',
                            uri='http://example.com/3'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/d/d3/Kinkaku-ji_2015.JPG',
                    title=place[4],
                    text=detail[4],
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text=place[4],
                            data='action=buy&itemid=2'
                        ),
                        MessageAction(
                            label='詳しく見る。',
                            text='open2'
                        ),
                        URIAction(
                            label='uri2',
                            uri='http://example.com/2'
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
    messages = make_carousel_template()
    global address
    address=event.message.address[13:]
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

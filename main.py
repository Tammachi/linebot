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
import sqlite3
import pandas as pd

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

# グローバル変数の宣言
route_search_longitude =999
route_search_latitude =999
ti1 = 'あああ'

app = Flask(__name__)

#con = sqlite3.connect('DSIGHT.csv')
#cursor = con.cursor()

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


# カルーセルテンプレートメッセージ
def make_carousel_template():
    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/3/35/Kiyomizu_Temple_-_01.jpg',
                    title = '清水寺',
                    text='京都府京都市東山区清水にある寺院。',
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text='清水寺',
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
                    title='清水寺',
                    text='京都府京都市東山区清水にある寺院。',
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text='清水寺',
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
                    title='清水寺',
                    text='京都府京都市東山区清水にある寺院。',
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text='清水寺',
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
                    title='清水寺',
                    text='京都府京都市東山区清水にある寺院。',
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text='清水寺',
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
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/d/d3/Kinkaku-ji_2015.JPG',
                    title='鹿苑寺',
                    text='京都市北区にある臨済宗相国寺派の寺',
                    actions=[
                        PostbackAction(
                            label='ここに行く！',
                            text='鹿苑寺',
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

# メッセージイベントの場合の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global route_search_latitude
    global route_search_longitude
    if '近くの観光情報を教えて' in event.message.text:
        content = 'わかりました！位置情報を送ってください！'
        route_search_latitude=999
        route_search_longitude=999
    elif route_search_latitude != 999 and route_search_longitude != 999:
        google_map_url = 'http://maps.google.com/maps?'
        google_map_url += "saddr={},{}&".format(route_search_latitude,route_search_longitude)
        google_map_url += "daddr={}".format(event.message.text)
        content = google_map_url
        route_search_latitude=999
        route_search_longitude=999
    else:
        content = 'まだその言葉はわかりません。近くの観光情報を知りたいときは、メニューの「観光情報」を押してください。'
    line_bot_api.reply_message(
        event.reply_token,
            TextSendMessage(text=content)
    )

# 位置情報メッセージイベントの場合の処理
@handler.add(MessageEvent, message=LocationMessage)
def handle_image_message(event):
    messages = make_carousel_template()
    global route_search_latitude
    global route_search_longitude
    route_search_latitude=event.message.latitude
    route_search_longitude=event.message.longitude
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

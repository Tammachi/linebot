# インポートするライブラリ
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction, URIAction
)
import os

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)


#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

# MessageEvent

def make_carousel_template():
    message_template = TemplateSendMessage(
        "type": "template",
    "altText": "this is a carousel template",
    "template": {
        "type": "carousel",
        "actions": [],
        "columns": [
            {
                "thumbnailImageUrl": "SPECIFY_YOUR_IMAGE_URL",
                "title": "タイトルです",
                "text": "テキストです",
                "actions": [
                    {
                        "type": "message",
                        "label": "アクション 1",
                        "text": "アクション 1"
                    },
                    {
                        "type": "message",
                        "label": "アクション 2",
                        "text": "アクション 2"
                    }
                ]
            },
            {
                "thumbnailImageUrl": "SPECIFY_YOUR_IMAGE_URL",
                "title": "タイトルです",
                "text": "テキストです",
                "actions": [
                    {
                        "type": "message",
                        "label": "アクション 1",
                        "text": "アクション 1"
                    },
                    {
                        "type": "message",
                        "label": "アクション 2",
                        "text": "アクション 2"
                    }
                ]
            }
        ]
    }
    return message_template

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if '位置情報' in event.message.text:
        messages = make_carousel_template()
    line_bot_api.reply_message(
        event.reply_token,
        messages
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)

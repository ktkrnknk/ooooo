import urllib.request
import os
import sys
import json
import scrape as sc
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

channel_secret = os.getenv('a1147e37fcbfb931131b4da60c4379b8', None)
channel_access_token = os.getenv('gQE1Twgy6eV9n3v18+VBjXDKHYEs5CGGS2inZJ79n+a4vvllFcU4TVCekVDhrGYaqOZKeouvvYEzvkK9Hd9apVO0suoSLmvoJVLxDmhrIaYG1a6TnfafhqZzzAIrg2V477101W8sBfwkHCyzoNyJFwdB04t89/1O/w1cDnyilFU=', None)
if channel_secret is None:
    print('Specify a1147e37fcbfb931131b4da60c4379b8 as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify gQE1Twgy6eV9n3v18+VBjXDKHYEs5CGGS2inZJ79n+a4vvllFcU4TVCekVDhrGYaqOZKeouvvYEzvkK9Hd9apVO0suoSLmvoJVLxDmhrIaYG1a6TnfafhqZzzAIrg2V477101W8sBfwkHCyzoNyJFwdB04t89/1O/w1cDnyilFU= as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)


    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    word = event.message.text
    result = sc.getNews(word)

    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=result)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

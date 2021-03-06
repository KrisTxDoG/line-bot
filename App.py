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

from app import app

app = Flask(__name__)

line_bot_api = LineBotApi('kiSyUsy6NRR9qN+Rab1qZtySRDK0TAdcQDbaizdzET2Mk0rQsv5st6IZV+2IB6HcPYBPA932eS3ADGYQyVAiqNd4Z4TzKdWtkHYwsMz3pN6MSOye+Yic4tQlXrawNXITRUqnyH+9HBJWv9UqTAb+jQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a7e7b45a4a5328f5f790b6664dc201f7')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    msg = event.message.text
    r = '很抱歉，您說什麼'

    if msg == 'hi':
        r = 'hi'
    elif msg == '你吃飯了嗎':
        r = '還沒'


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
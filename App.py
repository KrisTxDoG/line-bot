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

line_bot_api = LineBotApi('0RLrzyKOc65Eg1ejcmg8J9F1kYc59hHWAEvVqvaNzV+d8o7VhW3pOAxOgLxcxZTzPYBPA932eS3ADGYQyVAiqNd4Z4TzKdWtkHYwsMz3pN4Pfplomg27+z+Pc2NaQfY5sqCddXDMk7Neq7nUXGAHLQdB04t89/1O/w1cDnyilFU=')
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
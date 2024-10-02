from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
import json

app = Flask(__name__)

with open('username_line.txt', 'r') as file:
    lines = file.readlines()
    channel_access_token = lines[0].strip()
    channel_secret = lines[1].strip()

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# ---- Quick Reply Function ----
def quick_reply_menu(line_bot_api, tk, user_id, msg):
    quick_reply_button = QuickReplyButton(
        action=MessageAction(label="เมนู", text="เมนู")
    )
    quick_reply = QuickReply(
        items=[quick_reply_button]
    )
    line_bot_api.reply_message(tk, [TextSendMessage(text="เลือกเมนูที่ต้องการ", quick_reply=quick_reply)])

# ---- End of Quick Reply ----

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)

        msg = json_data['events'][0]['message']['text']
        tk = json_data['events'][0]['replyToken']
        uid = json_data['events'][0]['source']['userId']

        # Check for quick reply menu request
        if msg in ["เมนู", "menu", "Menu"]:
            quick_reply_menu(line_bot_api, tk, uid, msg)
        else:
            # Default response when no quick reply is triggered
            line_bot_api.reply_message(tk, TextSendMessage(text="ขอโทษครับ ไม่เข้าใจคำถาม กรุณาลองใหม่"))

    except InvalidSignatureError:
        print("Invalid signature.")
    except Exception as e:
        print("Error:", e)
        print(body)
    return 'OK'

if __name__ == "__main__":
    app.run(port=5000)
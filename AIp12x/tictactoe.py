
###=== (5.1) 載入軟件包 與自製函數(initialY,computeAB,updateY,centerY,judgeX) ===###  
from linebot import ( LineBotApi, WebhookHandler )
from linebot.exceptions import( InvalidSignatureError )
from linebot.models import *    
from flask import Flask, request, abort 
#---------- 下述是加入 ABgame
from flask import url_for, redirect, render_template, Markup
import numpy as np
import pandas as pd
import random


###=== (5.2) 設定對話(kk,openF,answerF) ===###
Xactual = np.array([1,2,3,4])   
openF1 = "ooxx game" 
openF2 = "ooxx game"                              #-- openF: 會話啟始(opening)
app = Flask(__name__)  # __name__ 代表目前執行的模組

###=== (5.3) LINE介面密碼 ===### (參考3.3)
##== (1) Channel Access Token
line_bot_api = LineBotApi("zX5wosMZDhR00JwpEwCtKCrOGZc/y90rFLsJFv9qhwNEvR29DtFmWUlLzVSDHIeYc09TJ3AIh7XwmV9eduCViUAIgWAC9NMEFWvxU/nlFUg1jPjKLbEAH5p/gNHTBKJIjuZKbf5m5HgVw4rFkSu9vwdB04t89/1O/w1cDnyilFU=")  #-- YOUR_CHANNEL_ACCESS_TOKEN
##== (2) Channel Secret
handler = WebhookHandler("d744d023067e2c4d4717a61d8081ac18")  #-- YOUR_CHANNEL_SECRET

###=== (5.4) 監聽來自 /callback 的 Post Request  ===###
@app.route("/callback", methods=['POST']) 
def callback():
    print(">>>>>>>>> 1.testing")  # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print(">>>>>>>>> 2.testing")  # get request body as text
    body = request.get_data(as_text=True)
    print(">>>>>>>>> 3.testing"+body)
    app.logger.info("Request body: " + body)
    print(">>>>>>>>> 4.testing-body:"+body)
    # handle webhook body
    try:
        print(">>>>>>>>> 5.testing-try:...")
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

###=== (5.5) 處理訊息  ===###
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global Xactual
    print(event)
    if event.message.id == "100001":
        return
    text = event.message.text
    print(">>>>>>>>>> TEXT = "+text)
    if (text=="Hi"):      reply_text = "Hello"
    elif(text=="機器人"):  reply_text = "有！我是game機器人"
    elif(text=="你好"):    reply_text = "你好啊..."
    elif(text.upper()=="H"):
        reply_text = "ooxx game"
    elif(text=="介紹"):    reply_text = openF1
    elif(text=="game"):
        print("game")


###=== (5.6) 執行程式  ===###
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

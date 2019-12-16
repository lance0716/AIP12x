


###=== (5.1) 載入軟件包 ===###  
from flask import Flask, request, abort
from linebot import ( LineBotApi, WebhookHandler )
from linebot.exceptions import( InvalidSignatureError )
from linebot.models import *
import random
from random import randint




###=== (5.2) 程式宣告 ===###  
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
    print(event)
    if event.message.id == "100001":
        return
    text = event.message.text
    if (text=="Hi"):
        reply_text = "Hello"
        #Your user ID
    elif(text=="你好"): 
        reply_text = "你好啊..."
    elif(text=="機器人"):
        reply_text = "有！我是game機器人"
    elif(text=="game"):
        board = []
        for x in range(3):
            board.append(["[ ]"] * 3)
        def print_board(board):
            for row in board:
                reply_text = " ".join(row)
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
        reply_text = "Let's play Tic Tac Toe!"
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)
        print_board(board)

        for turn in range(10):
            turn = turn + 1
            guess_row = int(raw_input("Row:"))
            guess_col = int(raw_input("Col:"))
        
            if (guess_row < 0 or guess_row > 2) or (guess_col < 0 or guess_col > 2):
                reply_text = "Oops, that's not even on the board."
                line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
            elif (board[guess_row][guess_col] == "[O]") or (board[guess_row][guess_col] == "[X]"):
                reply_text = "Spot not available."
                line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
            else:
                board[guess_row][guess_col] = "[X]"
                print_board(board)
                xwins = (board[0][0] == "[X]" and board[0][1] == "[X]" and board[0][2] == "[X]") or (board[1][0] == "[X]" and board[1][1] == "[X]" and board[1][2] == "[X]") or (board[2][0] == "[X]" and board[2][1] == "[X]" and board[2][2] == "[X]") or (board[0][0] == "[X]" and board[1][0] == "[X]" and board[2][0] == "[X]") or (board[0][0] == "[X]" and board[1][0] == "[X]" and board[2][0] == "[X]") or (board[1][0] == "[X]" and board[1][1] == "[X]" and board[1][2] == "[X]") or (board[2][0] == "[X]" and board[2][1] == "[X]" and board[2][2] == "[X]") or (board[0][0] == "[X]" and board[1][1] == "[X]" and board[2][2] == "[X]") or (board[2][0] == "[X]" and board[1][1] == "[X]" and board[0][2] == "[X]") or (board[0][2] == "[X]" and board[1][1] == "[X]" and board[2][0] == "[X]")
                owins = (board[0][0] == "[O]" and board[0][1] == "[O]" and board[0][2] == "[O]") or (board[1][0] == "[O]" and board[1][1] == "[O]" and board[1][2] == "[O]") or (board[2][0] == "[O]" and board[2][1] == "[O]" and board[2][2] == "[O]") or (board[0][0] == "[O]" and board[1][0] == "[O]" and board[2][0] == "[O]") or (board[0][0] == "[O]" and board[1][0] == "[O]" and board[2][0] == "[O]") or (board[1][0] == "[O]" and board[1][1] == "[O]" and board[1][2] == "[O]") or (board[2][0] == "[O]" and board[2][1] == "[O]" and board[2][2] == "[O]") or (board[0][0] == "[O]" and board[1][1] == "[O]" and board[2][2] == "[O]") or (board[2][0] == "[O]" and board[1][1] == "[O]" and board[0][2] == "[O]") or (board[0][2] == "[O]" and board[1][1] == "[O]" and board[2][0] == "[O]")
                
                if xwins is True:
                    reply_text =  "You win!"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
                    break
                elif owins is True:
                    reply_text = "You lose!"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
                    break
                else:
                    reply_text = "My turn!"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
                    
                    def random_row(board):
                        return randint(0, len(board) - 1)
                    def random_col(board):
                        return randint(0, len(board[0]) - 1)
                    comp_row = random_row(board)
                    comp_col = random_col(board)
                    while board[comp_row][comp_col] == "[O]" or board[comp_row][comp_col] == "[X]":
                        def random_row(board):
                            return randint(0, len(board) - 1)
                        def random_col(board):
                            return randint(0, len(board[0]) - 1)
                        
                        comp_row = random_row(board)
                        comp_col = random_col(board)
                    
                    else:
                        board[comp_row][comp_col] = "[O]"
                        print_board(board)

###=== (5.6) 執行程式  ===###
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #main()
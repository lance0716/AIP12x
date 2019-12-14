


###=== (5.1) 載入軟件包 ===###  
from flask import Flask, request, abort
from linebot import ( LineBotApi, WebhookHandler )
from linebot.exceptions import( InvalidSignatureError )
from linebot.models import *
import random


def drawBoard(board):

    print(board[7] + '|' + board[8] + '|' + board[9])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[1] + '|' + board[2] + '|' + board[3])

def inputPlayerLetter():

    letter = ''
    while not (letter == 'O' or letter == 'X'):
        #print('Do you want to be O or X?')
        reply_text = "Do you want to be O or X?"
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)
        letter = input().upper()

    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():

    print('Do you want to go first?')
    gofirstornot = input().upper()
    if gofirstornot != 'Y':
        return 'computer'
    else:
        return 'player'

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):

    return ((bo[7] == le and bo[8] == le and bo[9] == le) or #  top
    (bo[4] == le and bo[5] == le and bo[6] == le) or #  middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or #  bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopy(board):

    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy

def isSpaceFree(board, move):

    return board[move] == ' '

def getPlayerMove(board):

    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)

def chooseRandomMoveFromList(board, movesList):

    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter):

    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # AI:
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, computerLetter, i)
            if isWinner(boardCopy, computerLetter):
                return i


    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, playerLetter, i)
            if isWinner(boardCopy, playerLetter):
                return i

    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    if isSpaceFree(board, 5):
        return 5

    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):

    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

def game():
    #print('Welcome to Tic Tac Toe!')
    reply_text = "Welcome to Tic Tac Toe!"
    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

    while True:

        theBoard = [' '] * 10
        playerLetter, computerLetter = inputPlayerLetter()
        turn = whoGoesFirst()
        #print('The ' + turn + ' will go first.')
        reply_text = "The " + turn + " will go first.!"
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)
        gameIsPlaying = True

        while gameIsPlaying:
            if turn == 'player':
                
                drawBoard(theBoard)
                move = getPlayerMove(theBoard)
                makeMove(theBoard, playerLetter, move)

                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    #print('You have won the game!')
                    reply_text = "You have won the game!"
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        #print('The game is a tie!')
                        reply_text = "The game is a tie!"
                        message = TextSendMessage(reply_text)
                        line_bot_api.reply_message(event.reply_token, message)
                        break
                    else:
                        turn = 'computer'

            else:
                
                move = getComputerMove(theBoard, computerLetter)
                makeMove(theBoard, computerLetter, move)

                if isWinner(theBoard, computerLetter):
                    drawBoard(theBoard)
                    #print('You have lose the game!')
                    reply_text = "You have lose the game!"
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        #print('The game is a tie!')
                        reply_text = "The game is a tie!"
                        message = TextSendMessage(reply_text)
                        line_bot_api.reply_message(event.reply_token, message)
                        break
                    else:
                        turn = 'player'

       # print('Do you want to play again? (yes or no)')
        reply_text = "Do you want to play again? (yes or no)!"
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)
        if not input().lower().startswith('y'):
            break





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
        #game()
        #print('Welcome to Tic Tac Toe!')
        reply_text = "Welcome to Tic Tac Toe!"
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)

        while True:
            reply_text = "while"
            message = TextSendMessage(reply_text)
            line_bot_api.reply_message(event.reply_token, message)
            theBoard = [' '] * 10
            playerLetter, computerLetter = inputPlayerLetter()
            turn = whoGoesFirst()
            #print('The ' + turn + ' will go first.')
            reply_text = "The " + turn + " will go first.!"
            message = TextSendMessage(reply_text)
            line_bot_api.reply_message(event.reply_token, message)
            gameIsPlaying = True

            while gameIsPlaying:
                if turn == 'player':
                    
                    drawBoard(theBoard)
                    move = getPlayerMove(theBoard)
                    makeMove(theBoard, playerLetter, move)

                    if isWinner(theBoard, playerLetter):
                        drawBoard(theBoard)
                        #print('You have won the game!')
                        reply_text = "You have won the game!"
                        message = TextSendMessage(reply_text)
                        line_bot_api.reply_message(event.reply_token, message)
                        gameIsPlaying = False
                    else:
                        if isBoardFull(theBoard):
                            drawBoard(theBoard)
                            #print('The game is a tie!')
                            reply_text = "The game is a tie!"
                            message = TextSendMessage(reply_text)
                            line_bot_api.reply_message(event.reply_token, message)
                            break
                        else:
                            turn = 'computer'

                else:
                    
                    move = getComputerMove(theBoard, computerLetter)
                    makeMove(theBoard, computerLetter, move)

                    if isWinner(theBoard, computerLetter):
                        drawBoard(theBoard)
                        #print('You have lose the game!')
                        reply_text = "You have lose the game!"
                        message = TextSendMessage(reply_text)
                        line_bot_api.reply_message(event.reply_token, message)
                        gameIsPlaying = False
                    else:
                        if isBoardFull(theBoard):
                            drawBoard(theBoard)
                            #print('The game is a tie!')
                            reply_text = "The game is a tie!"
                            message = TextSendMessage(reply_text)
                            line_bot_api.reply_message(event.reply_token, message)
                            break
                        else:
                            turn = 'player'

            # print('Do you want to play again? (yes or no)')
            reply_text = "Do you want to play again? (yes or no)!"
            message = TextSendMessage(reply_text)
            line_bot_api.reply_message(event.reply_token, message)
            if not input().lower().startswith('y'):
                break
    else:  # 如果非以上的選項，就會學你說話
        reply_text = text
    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

###=== (5.6) 執行程式  ===###
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

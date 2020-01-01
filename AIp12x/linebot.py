# $ heroku login              // 登入 Heroku
# $ git init                  // 初始化專案
# $ heroku git:remote -a 專案名稱  // 專案名稱 = aip12x

# $ git add .                // 更新專案 
# $ git commit -m “更新的訊息”
# $ git push heroku master

# 偵錯(如下行指令)
# $ heroku logs --tail

import os
import configparser
from flask import Flask, request, abort
from linebot import ( LineBotApi, WebhookHandler )
from linebot.exceptions import( InvalidSignatureError )
from linebot.models import *
import re
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'zX5wosMZDhR00JwpEwCtKCrOGZc/y90rFLsJFv9qhwNEvR29DtFmWUlLzVSDHIeYc09TJ3AIh7XwmV9eduCViUAIgWAC9NMEFWvxU/nlFUg1jPjKLbEAH5p/gNHTBKJIjuZKbf5m5HgVw4rFkSu9vwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d744d023067e2c4d4717a61d8081ac18')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'Hi':
        reply_text = "Hello"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
        print("Hello")

    elif event.message.text == '你好': 
        reply_text = "你好啊..."
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))

    elif re.search(r"(機器人|bot)", event.message.text):
        reply_text = "有！我是Job機器人"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))

    elif re.search(r"((正在追蹤|追蹤中|追蹤)的(職缺|缺額))", event.message.text):
        line_bot_api.reply_message(event.reply_token, follow())
    
    elif event.message.text == '線上真人諮詢':
        line_bot_api.reply_message(event.reply_token, onlineHumanContact())

    elif event.message.text == '我的履歷':
        line_bot_api.reply_message(event.reply_token, myResume())

    elif event.message.text == '瀏覽履歷庫':
        line_bot_api.reply_message(event.reply_token, viewMyResume())
    elif event.message.text.upper() == 'LOGO':
        url = "https://docsplayer.com/docs-images/50/26156972/images/1-0.png"
        #line_bot_api.push_message(to, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
        #line_bot_api.push_message(to, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
        image_message = ImageSendMessage(original_content_url=url, preview_image_url=url)    
        line_bot_api.reply_message(event.reply_token, image_message)

    elif re.search(r"(MOVIE|影片|求職技巧)", event.message.text):
        url = "https://i.imgur.com/cZcuWu2.mp4"
        line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url=url, preview_image_url=url))

    elif re.search(r"(MUSIC|音樂|(我想聽|聽)音樂)", event.message.text):
        url = "https://sampleswap.org/mp3/artist/5101/Peppy--The-Firing-Squad_YMXB-160.mp3"
        line_bot_api.reply_message(event.reply_token,AudioSendMessage(original_content_url=url, duration=100000))
    
    elif re.search(r"(夢想|不想工作)", event.message.text):
        reply_text = dream()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        print(reply_text)

    else:
        reply_text = "可以輸入...\n1.追蹤...職缺\n2.線上真人諮詢\n3.我的履歷\n4.瀏覽履歷庫\n5.logo\n6.movie\影片\n7.music\音樂"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
    

def follow():
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title='Backend Engineer 後端工程師',
                    text='地點：台北市中正區\n（追蹤中）',
                    actions=[
                        URIAction(
                            label='直接應徵',
                            uri ='https://www.1111.com.tw/job/85971957/?ks=%E5%B7%A5%E7%A8%8B%E5%B8%AB'
                        ),
                        MessageAction(
                            label='線上真人諮詢',
                            text='線上真人諮詢'
                        ),
                        PostbackAction(
                            label='取消追蹤',
                            display_text='取消追蹤',
                            data='action=buy&itemid=1'
                        ),
                    ]
                ),
                CarouselColumn(
                    title='誠徵 軟體工程師 Software Engineer',
                    text='地點：新北市汐止區\n（追蹤中）',
                    actions=[
                        URIAction(
                            label='直接應徵',
                            uri ='https://www.1111.com.tw/job/91244617/?ks=%E5%B7%A5%E7%A8%8B%E5%B8%AB'
                        ),
                        MessageAction(
                            label='線上真人諮詢',
                            text='線上真人諮詢'
                        ),
                        PostbackAction(
                            label='取消追蹤',
                            display_text='取消追蹤',
                            data='action=buy&itemid=1'
                        ),
                    ]
                ),
                CarouselColumn(
                    title='誠徵 PE Engineer 製程工程師',
                    text='地點：新北市新店區\n（FA聯繫中）',
                    actions=[
                        URIAction(
                            label='直接應徵',
                            uri ='https://www.1111.com.tw/job/85859810/?ks=%E5%B7%A5%E7%A8%8B%E5%B8%AB'
                        ),
                        MessageAction(
                            label='線上真人諮詢',
                            text='線上真人諮詢'
                        ),
                        PostbackAction(
                            label='取消追蹤',
                            display_text='取消追蹤',
                            data='action=buy&itemid=1'
                        ),
                    ]
                ),
                CarouselColumn(
                    title='誠徵 系統工程師 System Engineer',
                    text='地點：台北市松山區',
                    actions=[
                        URIAction(
                            label='直接應徵',
                            uri ='https://www.1111.com.tw/job/86025594/?ks=%E5%B7%A5%E7%A8%8B%E5%B8%AB'
                        ),
                        MessageAction(
                            label='線上真人諮詢',
                            text='線上真人諮詢'
                        ),
                        PostbackAction(
                            label='取消追蹤',
                            display_text='取消追蹤',
                            data='action=buy&itemid=1'
                        ),
                    ]
                ),
                CarouselColumn(
                    title='誠徵 硬體工程師(Hardware Mixed Signal Engineer)',
                    text='地點：台北市南港區',
                    actions=[
                        URIAction(
                            label='直接應徵',
                             uri ='https://www.1111.com.tw/job/85013437/?ks=%E5%B7%A5%E7%A8%8B%E5%B8%AB'
                        ),
                        MessageAction(
                            label='線上真人諮詢',
                            text='線上真人諮詢'
                        ),
                        PostbackAction(
                            label='取消追蹤',
                            display_text='取消追蹤',
                            data='action=buy&itemid=1'
                        ),
                    ]
                ),
            ]
        )
    )
    return message



def onlineHumanContact():
    message = TextSendMessage('稍待片刻，將由相關人士與您聯絡')
    return message

def myResume():
    message = TemplateSendMessage(
		alt_text='Carousel template',
        template=ButtonsTemplate(
            title='我的履歷',
            text='選擇新增一份律例或挑選現有的履歷',
            actions=[
                URIAction(
                    label='新增新的一份履歷',
                    uri='https://linebot-human-resource.netlify.com/create-resume'
                ),
                MessageAction(
                    label='瀏覽履歷庫',
                    text='瀏覽履歷庫'
                ),
            ]
        )
    )
    return message

def viewMyResume():
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title='履歷1',
                    text='Lorem lpsum is simply dummy test',
                    actions=[
						URIAction(
                        	label='編輯履歷',
                        	uri='https://linebot-human-resource.netlify.com/create-resume'
                    	)
					]
                ),
                CarouselColumn(
                    title='履歷2',
                    text='Lorem lpsum is simply dummy test',
                    actions=[
						URIAction(
                        	label='編輯履歷',
                        	uri='https://linebot-human-resource.netlify.com/create-resume'
                    	)
					]
                ),
                CarouselColumn(
                    title='履歷3',
                    text='Lorem lpsum is simply dummy test',
                    actions=[
						URIAction(
                        	label='編輯履歷',
                        	uri='https://linebot-human-resource.netlify.com/create-resume'
                    	)
					]
                )
            ]
        )
    )
    return message


def dream():
    url = 'https://www.taiwanlottery.com.tw/index_new.aspx'
    html = requests.get(url)
    sp = BeautifulSoup(html.text, 'html.parser')
    data1 = sp.select("#rightdown")
    data2 = data1[0].find('div', {'class':'contents_box04'})
    data3 = data2.find_all('div', {'class':'ball_tx'})
    dataTitle = data2.find_all('div', {'class':'contents_mine_tx02'})

    title_text=""
    num_text=""

    # 標題.
    for n in range(len(dataTitle)):
        title_text = title_text + " " + dataTitle[n].text
    # 三星彩號碼.
    for n in range(len(data3)):
        num_text = num_text + "  " + data3[n].text

    sum_text= title_text + "\n" + "三星彩中獎號碼：" + num_text
    #sum_text= "三星彩中獎號碼：" + num_text
    return sum_text


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

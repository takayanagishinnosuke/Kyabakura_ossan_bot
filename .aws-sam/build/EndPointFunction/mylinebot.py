"""
じじいのLine Bot
"""

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,
)

import boto3

import random

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))



client = boto3.client('rekognition')#boto3


def lambda_handler(event, context):
    headers = event["headers"]
    body = event["body"]

    # get X-Line-Signature header value
    signature = headers['x-line-signature']

    # handle webhook body
    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}

# メッセージの返答
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):#eventに受け取ったメッセージが入る
    """ TextMessage handler """
    input_text = event.message.text #input_textに格納
    langlist = ['死とは儚く美しい', '賢者モードにわしはなる!', '魑魅魍魎っておいしいの?','壮大な宇宙はまやかし','混沌から湧き出る欲','いつになったらポケモンマスターなれるの?',] 
    x = random.randint(0,5)

    if 'おいじじい' in input_text:
        content = 'なにかようか?'

    elif 'きもい' in input_text:
        content = 'そうかのう'

    elif 'しね' in input_text:
        content = 'おいてめえなんつった!!'
    
    elif 'かわいい' in input_text:
        content = 'おまえさんもな'
    
    elif 'はげ' in input_text:
        content = 'おまえさんもな'
    
    elif 'うるさい' in input_text:
        content = 'すまんな'

    else:
        content = langlist[x]

    # botの返答
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content)
        )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    #画像を一時ファイルとして保存
    message_content = line_bot_api.get_message_content(event.message.id)
    file_path = '/tmp/sent-image.jpg'
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    # rekognitionで感情分析する
    with open(file_path, 'rb') as fd:
        sent_image_binary = fd.read()
        response = client.detect_faces(Image={"Bytes": sent_image_binary}, Attributes=["ALL"])

        #print(response["Emotions"]["Confidence"]["Type"])
    
    ##関数定義(配列から取り出す)
        message = response['FaceDetails']['Emotions']["Type"]




    #メッセージの分岐
        
    #返答を送信する
    line_bot_api.reply_message(
        event.reply_token,
        # TextSendMessage(text=str(response)[:1000])
        TextSendMessage(text = message)
        )

    #file.path の画像を削除
    os.remove(file_path)






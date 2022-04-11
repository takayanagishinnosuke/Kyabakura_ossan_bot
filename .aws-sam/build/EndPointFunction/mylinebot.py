"""
おっさんのLine Bot
"""
##必要なライブラリimport

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,
)

import boto3

import random

import json
from collections import OrderedDict


##LINE設定
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
    langlist = ['今日は部長に怒られちゃった(泣)慰めてほしいなーなんつって!! そろそろお店以外で会えないのかなー？', 'ただいま賢者モード…なんつって!! ねえ、そろそろお店以外で会えないのかなー？', '僕を待っててくれるのは君だけだよ…愛して…なんつって!! そろそろお店以外で会えないのかなー？','僕はおじさんだし、お金もないけどそれでもいいのかい？僕は本気だよ…？ そろそろお店以外で会えないのかなー？','やる気マックスオリックス！なんつって！ 今日もお店以外で会えない？？','今までは女性が苦手だったけど、君に出会ってから変わったよ僕は！ そろそろお店以外で会えないのかな…？',] 
    x = random.randint(0,5)

    if 'むり' in input_text:
        content = 'そっか…タイミングってあるよね！いつでも大丈夫だからね！'

    elif 'きもい' in input_text:
        content = 'そんな…でも君は優しいから、心にも無いことを言ってしまうことあるよね！大丈夫だよ！'

    elif 'しね' in input_text:
        content = 'そんなこと言わないで…、きっと疲れているんだね…僕にできる事があればなんでも言って！'
    
    elif 'かっこいい' in input_text:
        content = '嬉しい…これ以上惚れさせないでよ…(照)'
    
    elif 'はげ' in input_text:
        content = '冗談を言ってくるくらい君との距離が近づいてるって証拠だね！'
    
    elif 'うるさい' in input_text:
        content = 'ごめん…ほんとごめん…嫌いにならないでほしいな…おじさん頑張るからさ！'

    elif 'だめ' in input_text:
        content = 'そうだよね…タイミングってあるよね！ごめんね！…おじさんいつまでも待ってるよ！'

    else:
        content = langlist[x]

    # botの返答
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content)
        )

##画像ファイル送信設定
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
        for faceDetail in response['FaceDetails']:
            emotion = faceDetail['Emotions']
            typesrc = emotion[0]
            ##むりくり文字列変換（json.load効かない…)
            typestr = json.dumps(typesrc)
            print(typestr)

    #メッセージの分岐
        if 'CALM' in typestr:
            emomessage = '穏やかな顔も素敵だね! お店に行っちゃおうかな!(給料日前だけど)てへぺろ'
        elif 'HAPPY' in typestr:
            emomessage = 'わあ!楽しそうだなあ! 笑顔を見にお店に行っちゃおうかな!(金欠だけど)てへぺろ'
        elif 'SAD' in typestr:
            emomessage = 'どうしたの?悲しいことでもあった!?!? 慰めにお店に行っちゃおうかな!(財布無いけど)てへぺろ'
        elif 'ANGRY' in typestr:
            emomessage = 'なんか怒らせるような事したかな…? お詫びにお店に行くね!(2000円しか無いけど)ぺこり'
        elif 'CONFUSED' in typestr:
            emomessage = 'どうして困惑してるの…? ひょっとして最近お店に行ってないからかな…!今日いくよ!(小銭しか無いけど)ぺこり'
        elif 'DISGUSTED' in typestr:
            emomessage = '僕のこと嫌いになった…? ひょっとして最近お店に行ってないからかな…!今日いくよ!(小銭しか無いけど)ぺこり'
        elif 'SURPRISED' in typestr:
            emomessage = 'そんなに驚いてどうしたの! ひょっとして僕を待ってくれてるのかな…!?今日お店いくよ!(商品券しか無いけど)ぺこり'
        elif 'FEAR' in typestr:
            emomessage = 'そんな怖がらないで…僕が守ってあげるからね…!? 今日お店いくよ!(3000円しか無いけど)てへぺろ'
        else:
            emomessage = 'うう〜ん、これはなんて表情かな??今日もかわいいね最高だよ。'
        
        
    #返答を送信する
    line_bot_api.reply_message(
        event.reply_token,
        # TextSendMessage(text=str(response)[:1000])
        TextSendMessage(text = str(emomessage))
        )

    #file.path の画像を削除
    os.remove(file_path)






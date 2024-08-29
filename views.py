from django.shortcuts import render
#models.py資料表
from PoJuiLineBOT.models import *

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

import string
import random
import os
import io

# Imports the Google Cloud client library
from google.cloud import vision
# from google.cloud.vision import types
# Importantance:set your json file in this part, I try to follow official guide but it didn't work, use below instead.T
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"my-project-test-373910-3e45096f9afe.json"
# Instantiates a client
client = vision.ImageAnnotatorClient()

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        #先設定一個要回傳的message空集合
        message=[]
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        #在這裡將body寫入機器人回傳的訊息中，可以更容易看出你收到的webhook長怎樣#
        message.append(TextSendMessage(text=str(body)))

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        ### 建立會員資料的程式碼部分 ###
        # for event in events:
        #     if isinstance(event, MessageEvent):
        #         mtext=event.message.text
        #         uid=event.source.user_id
        #         profile=line_bot_api.get_profile(uid)
        #         name=profile.display_name
        #         pic_url=profile.picture_url

        #         message=[]
        #         if User_Info.objects.filter(uid=uid).exists()==False:
        #             User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext)
        #             message.append(TextSendMessage(text='會員資料新增完畢'))
        #         elif User_Info.objects.filter(uid=uid).exists()==True:
        #             message.append(TextSendMessage(text='已經有建立會員資料囉'))
        #             user_info = User_Info.objects.filter(uid=uid)
        #             for user in user_info:
        #                 info = 'UID=%s\nNAME=%s\n大頭貼=%s'%(user.uid,user.name,user.pic_url)
        #                 message.append(TextSendMessage(text=info))
        #     line_bot_api.reply_message(event.reply_token,message)

        for event in events:
            #如果事件為訊息
            if isinstance(event, MessageEvent):
                # print(event.message.type)
                # print(event.message.text)
                if event.message.type=='text':

                    # message.append(TextSendMessage(text='文字訊息'))
                    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您想說的是:" + event.message.text + "?"))

                    if "高科" in event.message.text:
                        line_bot_api.reply_message(event.reply_token,LocationSendMessage(title= "高科大(建功校區)",address= "807高雄市三民區建工路415號",latitude= 22.651670605211216,longitude= 120.32866089731456))
                    elif "巨城" in event.message.text:
                        line_bot_api.reply_message(event.reply_token,LocationSendMessage(title= "遠東巨城購物中心",address= "新竹市東區中央路229號",latitude= 24.810000,longitude= 120.977500))
                    elif "幹什麼" in event.message.text:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您想說的是:" + event.message.text + "?"))
                    elif "幹嘛" in event.message.text:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您想說的是:" + event.message.text + "?"))
                    elif "幹" in event.message.text:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="不可以罵髒話！"))
                    elif "靠" in event.message.text:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="不可以罵髒話！"))
                    elif "您按到了" in event.message.text:
                        message.append(TextSendMessage(text='文字訊息'))
                    else :line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您想說的是:" + event.message.text + "?"))

                elif event.message.type=='image':
                    image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4)) # 建立隨機圖片名稱
                    image_content = line_bot_api.get_message_content(event.message.id)
                    image_name = image_name.upper()+'.png' # 建立圖片檔案名稱
                    path='./static/'+image_name
                    with open(path, 'wb') as fd: # 將圖片內容寫入檔案
                        print(fd.name)
                        for chunk in image_content.iter_content():
                            fd.write(chunk)

                    # The name of the image file to annotate
                    file_name = os.path.abspath(fd.name) # 拿到圖片
                    # Loads the image into memory
                    with io.open(file_name, 'rb') as image_file:
                        content = image_file.read()
                        image = vision.Image(content=content)

                        response = client.text_detection(image=image)
                        texts = response.text_annotations
                        print('車牌號碼是:' + texts[0].description)

                    # message.append(TextSendMessage(text='圖片訊息'))
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='車牌號碼是:' + texts[0].description))

                elif event.message.type=='location':
                    # print(event.message)
                    message.append(TextSendMessage(text='位置訊息'))
                    # line_bot_api.reply_message(event.reply_token,message)
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您分享的地址是:" + event.message.address))

                elif event.message.type=='video':
                    message.append(TextSendMessage(text='影片訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='sticker':
                    message.append(TextSendMessage(text='貼圖訊息'))
                    # line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=4))
                    line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://i.imgur.com/h3mOJ3x.jpg', preview_image_url='https://i.imgur.com/h3mOJ3x.jpg'))
                
                # elif event.message.type=='emoji':
                #     message.append(TextSendMessage(text='表情貼訊息'))
                #     # line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=4))
                #     line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://i.imgur.com/h3mOJ3x.jpg', preview_image_url='https://i.imgur.com/h3mOJ3x.jpg'))
                
                elif event.message.type=='audio':
                    message.append(TextSendMessage(text='聲音訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='file':
                    message.append(TextSendMessage(text='檔案訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

            # elif isinstance(event, FollowEvent):
            #     print('加入好友')
            #     line_bot_api.reply_message(event.reply_token,message)

            # elif isinstance(event, UnfollowEvent):
            #     print('取消好友')

            # elif isinstance(event, JoinEvent):
            #     print('進入群組')
            #     line_bot_api.reply_message(event.reply_token,message)

            # elif isinstance(event, LeaveEvent):
            #     print('離開群組')
            #     line_bot_api.reply_message(event.reply_token,message)

            # elif isinstance(event, MemberJoinedEvent):
            #     print('有人入群')
            #     line_bot_api.reply_message(event.reply_token,message)

            # elif isinstance(event, MemberLeftEvent):
            #     print('有人退群')
            #     line_bot_api.reply_message(event.reply_token,message)

            elif isinstance(event, PostbackEvent):
                print('PostbackEvent')

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

'''
#初始化資料庫遷移
python manage.py makemigrations
python manage.py migrate

#開啟Django內建伺服器指令
python manage.py runserver

#開啟ngrok
ngrok http 8000
'''
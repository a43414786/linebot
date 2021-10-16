from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage ,ImageSendMessage,VideoSendMessage
import os
import random
import pickle
import time
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
class name:
    def __init__(self):
        self.name = []
    def load(self):
        dirs = os.listdir("D:/linebot/name")
        if "name.pickle" in dirs:
            with open("D:/linebot/name/name.pickle","rb") as f:
                self.name = pickle.load(f)
    def dump(self):
        with open("D:/linebot/name/name.pickle","wb") as f:
            pickle.dump(self.name,f)

def react(event):
    if event.message.text == "抽2D":
        imgs = os.listdir("D:/linebot/static")
        img = imgs[random.randint(0,len(imgs) - 1)]
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            #TextSendMessage(text=event.message.text),
            ImageSendMessage(original_content_url='https://' + settings.ALLOWED_HOSTS[0] + '/static/' + img,preview_image_url='https://' + settings.ALLOWED_HOSTS[0] + '/static/' + img)   
        )

    elif "刪除暱稱" in event.message.text:
        msg = event.message.text[5:]
        count = 0
        fullname = ""
        for i in msg:
            count += 1 
            if i == "=" or i=='＝':
                break
            else:
                fullname += i
        a = name()
        a.load()
        for i in a.name:
            if i['fullname'] == fullname and i['name'] == msg[count:]:
                a.name.remove({'fullname':fullname,'name':msg[count:]})
        a.dump()
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TextSendMessage(text='刪除成功')
        )


    elif "新增暱稱" in event.message.text:
        msg = event.message.text[5:]
        count = 0
        fullname = ""
        for i in msg:
            count += 1 
            if i == "=" or i=='＝':
                break
            else:
                fullname += i
        a = name()
        a.load()
        for i in a.name:
            if i['fullname'] == fullname and i['name'] == msg[count:]:
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text='暱稱已存在')
                )
                return
        a.name.append({'fullname':fullname,'name':msg[count:]})
        a.dump()
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TextSendMessage(text='紀錄成功')
        )

    else:
        flag = 1
        msg = event.message.text
        fullname = ""
        for i in msg:
            if i == "!" or i == "！":
                flag = 0
                break
            else:
                fullname += i
        if flag == 1:
            return
        a = name()
        a.load()
        for i in a.name:
            if i['fullname'] == fullname:
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=i['name'])
                )
    
    
 
    '''elif "youtube-dl" in event.message.text:  
        msg = event.message.text
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TextSendMessage(text='開始下載')
        )

        os.system(msg + " -o \"D:/linebot/static/t.mp4\"")

        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            VideoSendMessage(original_content_url='https://' + settings.ALLOWED_HOSTS[0] + '/static/' + 't.mp4',preview_image_url='https://' + settings.ALLOWED_HOSTS[0] + '/static/' + 't.mp4')
        )
        os.remove("D:/linebot/static/t.mp4")'''       




@csrf_exempt
def callback(request):
    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                with open("record/" + str(time.strftime("%Y%m%d", time.localtime())) + "record.txt","a") as f:
                    f.writelines("\n"+event.message.text) 
                
                react(event)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
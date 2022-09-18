from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackAction, PostbackEvent, PostbackTemplateAction, URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate,ImageSendMessage
import fl,Strategy_data_SQLite
 
line_bot_api = LineBotApi('Ff4GOYKQcVoLtiLR9Lpv9KsND8DG2VF4njWotsE8vNs/CDl68orI6p4wov5hzgcA5Gef/waOK+zb4jK6+8iH76xXw8/gAx+o8ky6ZYVTZDbJJYlSRafD7w2L1jH5wWbC6eYRBQQKD9E2Ib8+GtjRPgdB04t89/1O/w1cDnyilFU=')
#parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
your_ID = 'U6658ff60e29de21166347e537c9b2f65'

def reply():
    
    msg,chosen = fl.fiveline()
    print(msg)
    
    line_bot_api.push_message(your_ID,TextSendMessage(text=msg))
    for i in chosen:
        img_url = Strategy_data_SQLite.linebot_draw_fiveline(i)
        line_bot_api.push_message(your_ID, ImageSendMessage(
                        original_content_url=img_url,
                        preview_image_url=img_url
                    ))
    
reply()
print('===============')
"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from . import fl,ETF_data_SQLite
from . import test
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
ETF_id = ['1','2'] 

    
    
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
                if event.message.text == 'check': #查看服務
                    line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text='選擇基金:\n1 : 國內成分證券ETF \n2 : 國外成分證券ETF')
                )
                elif event.message.text in ETF_id:
                    etf_id = int(event.message.text)
                    reply = fl.fiveline(etf_id)
                    line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=reply)
                )
                elif event.message.text == 'sql':
                    line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=ETF_data_SQLite.get_sql()[0][0])
                )
                elif event.message.text == 'test':
                    line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=test.test1())
                )
                else:
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text='error')
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackAction, PostbackEvent, PostbackTemplateAction, URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate,ImageSendMessage
from . import ETF_data_SQLite,Strategy_data_SQLite,fl

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
your_ID = 'U6658ff60e29de21166347e537c9b2f65'


#123
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
            if isinstance(event, MessageEvent): # 如果有訊息事件

                if event.message.text == "Help":
                #if "Help" in event.message.text:
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text = 'Help Buttons Template',
                            template=ButtonsTemplate(
                                thumbnail_image_url='https://www.nasdaq.com/sites/acquia.prod/files/styles/720x400/public/2020/03/16/stocks-iamchamp-adobe.jpg',
                                title='HELP LIST',
                                text='請選擇你需要的功能',
                                actions=[
                                    MessageAction(
                                        label='Using Instructions',
                                        text='輸入 "ETF____" 搜尋該檔基本資訊或策略圖形\n（ETF清單可在 ETF List Link 中找到）'
                                    ),
                                    URIAction(
                                        label='ETF List Link',
                                        uri='https://www.twse.com.tw/zh/ETF/list'
                                        #text1='國內成分證券ETF:\n0050. 0051. 0052. 0053. 0054. 0055. 0056. 0057. 006203. 006204. 006208. 00690. 00692. 00701. 00713. 00730. 00728. 00731. 00733. 00850. 00878. 00881. 00891. 00892. 00894. 00896. 00901. 00900. 00904. 00905. 00907',
                                        #text='國外成分證券ETF:\n0061. 006205. 00625K. 006206. 006207. 00636. 00636K. 00639. 00645. 00643. 00643K. 00646. 00652. 00657. 00657K. 00661. 00662. 00668. 00668K. 00678. 00700. 00703. 00709. 00702. 00710B. 00711B. 00712. 00714. 00717. 00732. 00735. 00736. 00737. 00739. 00743. 00752. 00757. 00762. 00770. 00775B. 00774B. 00774C. 00830. 00771. 00851. 00861. 00875. 00876. 00882. 00885. 00893. 00895. 00897. 00898. 00899. 00903. 00902. 00906. 00908'
                                    ),
                                    MessageAction(
                                        label='Dashboard Link',
                                        text='Dashboard Link'
                                    ),
                                    URIAction(
                                        label='Yahoo Finance Link',
                                        uri='https://finance.yahoo.com'
                                    )
                                ]
                            )
                        )
                    )
 
                elif "ETF" in event.message.text:
                    msg = event.message.text[4:]
                    #msg = event.message.text.strip("ETF ")
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text = 'Buttons Template',
                            template=ButtonsTemplate(
                                thumbnail_image_url='https://nai500.com/wp-content/uploads/2021/05/canada-ETF.jpg',
                                title= event.message.text + ' Visualization',
                                text='請選擇想查看的基本資訊或策略圖形',
                                actions=[
                                    MessageAction(
                                        label='Basic Information',
                                        text= ETF_data_SQLite.basic_information(msg)
                                        #text='Basic Information'
                                    ),
                                    URIAction(
                                        label= 'Fiveline',
                                        uri= 'https://i.imgur.com/VZjVFkJ.png'  #這個傳送方法是錯的，要改掉～
                                        #data= Strategy_data_SQLite.linebot_draw_fiveline()
                                    ),
                                    PostbackAction(
                                        label= 'Fiveline + BBands',
                                        data= '發送 Fiveline + BBands'
                                    ),
                                    PostbackAction(
                                        label= 'Fiveline + KD',
                                        data= '發送 Fiveline + KD'
                                    )
                                ]
                            )
                        )
                    )
                
                elif event.message.text == "Chosen":
                    pass
                
                elif "recommend" in event.message.text:
                    #etf_id = int(event.message.text)
                    count = event.message.text[10:]
                    #print(count)
                    reply,chosen = fl.fiveline(int(count))
                    #print(reply)
                    #print(chosen)
                    line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=reply))
                    for i in chosen:
                        print(i)
                        img_url = Strategy_data_SQLite.linebot_draw_fiveline(i)
                        print(img_url)
                        line_bot_api.push_message(your_ID, ImageSendMessage(
                        original_content_url=img_url,
                        preview_image_url=img_url
                    ))
                        
                elif "fl" in event.message.text:
                    msg = event.message.text[3:]
                    img_url = Strategy_data_SQLite.linebot_draw_fiveline(msg)
                    
                    line_bot_api.reply_message(  
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url=img_url,
                        preview_image_url=img_url
                    )
                )
                elif "kd" in event.message.text:
                    msg = event.message.text[3:]
                    img_url = Strategy_data_SQLite.linebot_draw_fivelinekd(msg)
                    
                    line_bot_api.reply_message(  
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url=img_url,
                        preview_image_url=img_url
                    )
                )
                elif "bb" in event.message.text:
                    msg = event.message.text[3:]
                    img_url = Strategy_data_SQLite.linebot_draw_fivelinebb(msg)
                    
                    line_bot_api.reply_message(  
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url=img_url,
                        preview_image_url=img_url
                    )
                )


                else:
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text= '【 指令輸入錯誤 】\n• 輸入 "Help" 可搜尋ETF清單以及相關網站連結\n• 輸入 "ETF___(eg. ETF 0050)" 搜尋該檔最新交易日基本資訊或策略圖形，清單可在Help指令的ETF List Link中找到\n• 輸入 "Chosen" 可得最新交易日所推薦的ETF')
                )

                    #line_bot_api.reply_message(  # 回復傳入的訊息文字
                    #event.reply_token,
                    #TextSendMessage(text=event.message.text)
                #)
            
            if not isinstance(event, MessageEvent):
                pass

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
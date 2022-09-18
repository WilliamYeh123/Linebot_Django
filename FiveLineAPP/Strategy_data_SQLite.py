#from msilib import datasizemask
import sqlite3
import pyimgur
from matplotlib import use
import yfinance as yf
import ta
import requests
import pandas as pd
import numpy as np
import datetime,time,re
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
from pandas.core.frame import DataFrame

dict_from_ETF_list = pd.read_excel("C:/Users/willi/Documents/LineBot/FiveLineAPP/ETF_list.xlsx")
ETF_list = dict_from_ETF_list['Number']

today = datetime.date.today()
end = today - datetime.timedelta(days=1)
start = end - datetime.timedelta(days=365*3.5)

'''
conn = sqlite3.connect('ETF_list.db')
cursor = conn.cursor()


conn.execute("""CREATE TABLE if not exists Strategy_data
       (Date date ,
       Number TEXT ,
       Close FLOAT,
       '+2SD' FLOAT,
       '+1SD' FLOAT,
       TL FLOAT,
       '-1SD' FLOAT,
       '-2SD' FLOAT,
       bbh FLOAT,
       bbm FLOAT,
       bbl FLOAT,
       K FLOAT,
       D FLOAT,
       primary key (Date, Number));""")
conn.commit()

def five_line(data):   
    timetrend = list(range(1, data.shape[0]+1))
    data['timetrend'] = timetrend
    data = data[['timetrend','Close']]
    data = data.dropna()
    reg = LinearRegression()
    x = data['timetrend'].to_frame()
    y = data['Close'].to_frame()
    reg.fit(x,y)
    
    a = reg.intercept_ #截距
    beta = reg.coef_ #斜率
    longtrend = a + beta*x
    res = np.array(list(data['Close'])) - np.array(list(longtrend['timetrend']))
    std = np.std(res,ddof=1)
    fiveline = pd.DataFrame()
    fiveline['+2SD'] = longtrend['timetrend'] + (2*std)
    fiveline['+1SD'] = longtrend['timetrend'] + (1*std)
    fiveline['TL'] = longtrend['timetrend']
    fiveline['-1SD'] = longtrend['timetrend'] - (1*std)
    fiveline['-2SD'] = longtrend['timetrend'] - (2*std) 
    use_fiveline = pd.merge(data, fiveline[['+2SD','+1SD','TL','-1SD','-2SD']], left_index=True, right_index=True, how='left')
    pick_fiveline = use_fiveline[['Close','+2SD','+1SD','TL','-1SD','-2SD']]
    return pick_fiveline

def BBands(data): #布林通道，非樂活通道
    data_bb = data.copy()
    indicator_bb = ta.volatility.BollingerBands(close = data_bb['Close'], window = 20, window_dev = 2)
    data_bb['bbh'] = indicator_bb.bollinger_hband()
    data_bb['bbm'] = indicator_bb.bollinger_mavg()
    data_bb['bbl'] = indicator_bb.bollinger_lband()
    data_bb = data_bb.dropna()
    use_BBands = pd.merge(data, data_bb[['bbh','bbm','bbl']], left_index=True, right_index=True, how='left')
    pick_BBands = use_BBands[['bbh','bbm','bbl']]
    return pick_BBands

def KD(data):
    data_KD = data.copy()
    data_KD['min'] = data_KD['Low'].rolling(9).min()
    data_KD['max'] = data_KD['High'].rolling(9).max()
    data_KD['RSV'] = 100*(data_KD['Close'] - data_KD['min'])/(data_KD['max'] - data_KD['min'])
    data_KD = data_KD.dropna()

    K_list = [50]
    for num,rsv in enumerate(list(data_KD['RSV'])):
        K_yestarday = K_list[num]
        K_today = 2/3 * K_yestarday + 1/3 * rsv
        K_list.append(K_today)
    data_KD['K'] = K_list[1:]

    D_list = [50]
    for num,K in enumerate(list(data_KD['K'])):
        D_yestarday = D_list[num]
        D_today = 2/3 * D_yestarday + 1/3 * K
        D_list.append(D_today)
    data_KD['D'] = D_list[1:]
    use_KD = pd.merge(data, data_KD[['K','D']], left_index=True, right_index=True, how='left')
    pick_KD = use_KD[['K','D']]
    return pick_KD


#ETF_list = ['0050','0051','0052']
for i in ETF_list:
    df = yf.download(f"{i}.TW", start = str(start), end = str(end))
    f = five_line(df)
    b = BBands(df)
    k = KD(df)
    merge_df = pd.merge(b,k, left_index=True, right_index=True, how='left')
    merge2_df = pd.merge(f, merge_df, left_index=True, right_index=True, how='left')
    merge2_df = merge2_df.dropna()
    merge2_df['Number'] = f'{i}'
    merge2_df['Date'] = merge2_df.index.strftime("%Y-%m-%d")
    pick_df = merge2_df[['Date','Number','Close','+2SD','+1SD','TL','-1SD','-2SD','bbh','bbm','bbl','K','D']]
    #print(pick_df)

    for i in range(len(pick_df)):
        #pick_df[i][6] = pick_df[i][6].astype(str)
        #print(type(pick_df.iloc[i][6]))
        cursor.execute("insert into Strategy_data(Date, Number, Close, '+2SD', '+1SD', TL, '-1SD', '-2SD', bbh, bbm, bbl, K, D) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(pick_df.iloc[i]))
        conn.commit()
        #(pick_df[0][0], pick_df[0][1], ,,,)


    conn = sqlite3.connect('ETF_list.db')  #建立資料庫
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE 'Strategy_data_{i}'(Date, Number, Close, '+2SD', '+1SD', TL, '-1SD', '-2SD', bbh, bbm, bbl, K, D)")  #建立資料表
    conn.commit()

    #如果資料表存在，就寫入資料，否則建立資料表
    pick_df.to_sql(f'Strategy_data_{i}', conn, if_exists='append', index=False) 
'''

#client_id = '65399a44df56745'
#client_secret = '62879a34ffe8b1e696cf8ddf092512d42c4abf6c'


def linebot_draw_fiveline(msg):
    conn = sqlite3.connect('/home/awinlab/Documents/yeh/LineBot/FiveLineAPP/ETF_list.db')
    cursor = conn.cursor()
    sql =f"select * from Strategy_data where Number = '{msg}'"
    cursor.execute(sql)
    data = cursor.fetchall()
    #print(data)
    #date = []
    close = []
    highest = []
    high = []
    trend = []
    low = []
    lowest = []
    for row in data:
        #date.append(row[0])
        close.append(row[2])
        highest.append(row[3])
        high.append(row[4])
        trend.append(row[5])
        low.append(row[6])
        lowest.append(row[7])
    plt.figure(facecolor = 'white', figsize = (9,3), dpi=100)
    plt.plot(close)
    plt.plot(highest)
    plt.plot(high)
    plt.plot(trend)
    plt.plot(low)
    plt.plot(lowest)
    #plt.grid(True, axis = 'y')
    plt.title(f"{msg}.TW", color = 'black', fontsize = 24) 
    plt.ylabel("Stock price")
    plt.savefig(f'FIVELINE{msg}.png')
    plt.plot

    CLIENT_ID = "57cd6881c0b51ab"
    PATH = f"FIVELINE{msg}.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=f"FIVELINE{msg}")
    return uploaded_image.link
#img_url = linebot_draw_fiveline()
#print(img_url)


### 回傳fiveline+bb圖---------------------------------------------------------------------------------------------
def linebot_draw_fivelinebb(msg):
    conn = sqlite3.connect('/home/awinlab/Documents/yeh/LineBot/FiveLineAPP/ETF_list.db')
    cursor = conn.cursor()
    sql =f"select * from Strategy_data where Number = '{msg}'"
    cursor.execute(sql)
    data = cursor.fetchall()

    date = []
    close = []
    bbh = []
    bbm = []
    bbl = []
    for row in data:
        date.append(row[0])
        close.append(row[2])
        bbh.append(row[8])
        bbm.append(row[9])
        bbl.append(row[10])

    plt.figure(facecolor = 'white', figsize = (15,5), dpi=100)
    plt.plot(date, close)
    plt.plot(date, bbh)
    plt.plot(date, bbm)
    plt.plot(date, bbl)
    #plt.grid(True, axis = 'y')
    plt.title(f"{msg}.TW", color = 'black', fontsize = 24) 
    plt.ylabel("Stock price")
    plt.savefig(f'FivelineBB{msg}.png')
    plt.plot

    CLIENT_ID = "57cd6881c0b51ab"
    PATH = f"FivelineBB{msg}.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=f"FivelineBB{msg}")
    return uploaded_image.link



### 回傳fiveline+kd圖---------------------------------------------------------------------------------------------
def linebot_draw_fivelinekd(msg):
    conn = sqlite3.connect('/home/awinlab/Documents/yeh/LineBot/FiveLineAPP/ETF_list.db')
    cursor = conn.cursor()
    sql =f"select * from Strategy_data where Number = '{msg}'"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    date = []
    close = []
    k = []
    d = []
    for row in data:
        date.append(row[0])
        close.append(row[2])
        k.append(row[11])
        d.append(row[12])

    plt.figure(facecolor = 'white', figsize = (15,5), dpi=100)
    plt.plot(date, close)
    plt.plot(date, k)
    plt.plot(date, d)
    #plt.grid(True, axis = 'y')
    plt.title("0051.TW", color = 'black', fontsize = 24) 
    plt.ylabel("Stock price")
    plt.savefig('FivelineKD0051.png')
    plt.plot

    CLIENT_ID = "57cd6881c0b51ab"
    PATH = "FivelineKD0051.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="FivelineKD0051")
    return uploaded_image.link
    #return 'https://i.imgur.com/O8avbDH.png'


"""
### 推播圖（還沒完成）---------------------------------------------------------------------------------------------------------
def five_line(data):   
    timetrend = list(range(1, data.shape[0]+1))
    data['timetrend'] = timetrend
    data = data[['timetrend','Close']]
    data = data.dropna()
    reg = LinearRegression()
    x = data['timetrend'].to_frame()
    y = data['Close'].to_frame()
    reg.fit(x,y)
    
    a = reg.intercept_ #截距
    beta = reg.coef_ #斜率
    longtrend = a + beta*x
    res = np.array(list(data['Close'])) - np.array(list(longtrend['timetrend']))
    std = np.std(res,ddof=1)
    fiveline = pd.DataFrame()
    fiveline['+2SD'] = longtrend['timetrend'] + (2*std)
    fiveline['+1SD'] = longtrend['timetrend'] + (1*std)
    fiveline['TL'] = longtrend['timetrend']
    fiveline['-1SD'] = longtrend['timetrend'] - (1*std)
    fiveline['-2SD'] = longtrend['timetrend'] - (2*std) 
    use_fiveline = pd.merge(data, fiveline[['+2SD','+1SD','TL','-1SD','-2SD']], left_index=True, right_index=True, how='left')
    pick_fiveline = use_fiveline[['Close','+2SD','+1SD','TL','-1SD','-2SD']]
    return pick_fiveline

def linebot_draw_chosen_fiveline():
    def draw_chosen_fiveline(data):
        fig = plt.figure(facecolor = 'white', figsize = (15,5), dpi=100)
        plt.plot(data)
        #plt.grid(True, axis = 'y')
        plt.title(f"{i}.TW", color = 'black', fontsize = 24) 
        plt.ylabel("Stock price")


    for i in ETF_list:
        #price = stock_price(i)
        df = yf.download(f"{i}.TW", start = str(start), end = str(end))
        #df_plot = df[['Open', 'High', 'Low', 'Close']]
        df_fiveline = five_line(df)  
        a = df_fiveline.iloc[-1][-3] - df_fiveline.iloc[-2][-3]
        if (a>0.07) and (df_fiveline.iat[-1,-6] < df_fiveline.iat[-1,-2]):
            #print(i, df[['Close']])
            draw_chosen_fiveline(df_fiveline)
            plt.show()
    return plt.show()

linebot_draw_chosen_fiveline()"""

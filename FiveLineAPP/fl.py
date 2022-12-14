import yfinance as yf
import os
import sqlite3
from pathlib import Path
import datetime
import pandas as pd
import numpy as np
import datetime,time,re
from sklearn.linear_model import LinearRegression
import requests
from bs4 import BeautifulSoup

today = datetime.date.today()
end = today - datetime.timedelta(days=1)
start = end - datetime.timedelta(days=365*3.5)

dict_from_ETF_list = pd.read_excel("C:/Users/willi/Documents/LineBot/FiveLineAPP/ETF_list.xlsx")
ETF_list = dict_from_ETF_list['Number']


#etf1 = ['0050','0051','0056', '00850', '006205', '00645', '00646', '00662', '00631L', '00632R', '00633L', '00634R', '008201', '00635U', '00642U', '00673R', '00674R']

def five_line(data):   
    timetrend = list(range(1, data.shape[0]+1))
    data['timetrend'] = timetrend
    data = data[['timetrend','Close']]
    data = data.dropna()
    reg = LinearRegression()
    x = data['timetrend'].to_frame()
    y = data['Close'].to_frame()
    reg.fit(x,y)
    
    a = reg.intercept_ #æŠč·
    beta = reg.coef_ #æį
    #print(beta)
    #beta = beta[0][0]
    #print(beta)
    longtrend = a + beta*x
    res = np.array(list(data['Close'])) - np.array(list(longtrend['timetrend']))
    std = np.std(res,ddof=1)
    fiveline = pd.DataFrame()
    fiveline['highest'] = longtrend['timetrend'] + (2*std)
    fiveline['high'] = longtrend['timetrend'] + (1*std)
    fiveline['TL'] = longtrend['timetrend']
    fiveline['low'] = longtrend['timetrend'] - (1*std)
    fiveline['lowest'] = longtrend['timetrend'] - (2*std) 
    use_fiveline = pd.merge(data, fiveline[['highest','high','TL','low','lowest']], left_index=True, right_index=True, how='left')
    pick_fiveline = use_fiveline[['Close','highest','high','TL','low','lowest']]
    return pick_fiveline,beta

def stock_price(stock:str):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }

    data = requests.get(f"https://finance.yahoo.com/quote/{stock}.TW?p={stock}.TW", headers = headers)
    soup = BeautifulSoup(data.text)
    price = soup.find('fin-streamer',{'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'})
    return price.text



def fiveline(recommend_count):
    etf_data = {}
    slope = []
    reply = ''
    conn = sqlite3.connect('/home/awinlab/Documents/yeh/LineBot/FiveLineAPP/ETF_list.db')
    cursor = conn.cursor()
    for i in ETF_list:
        sql =f"select * from Strategy_data where Number = '{i}'"
        cursor.execute(sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        df = df.drop([1,8,9,10,11,12],axis =1)

        df.set_axis(['Date', 'Close', 'highest','high','TL','low','lowest'], axis='columns', inplace=True)
        df.set_index('Date', inplace = True)
        df2,beta = five_line(df)
        
        beta = beta.tolist() 
        #print(beta)
        beta = beta[0][0]
        #print(beta)
        slope.append((i,beta)) #(ETF_ID, æį)å­åĨslope
        #print(slope)
        etf_data[i] = df2 
        #print('df2 :',df2)
    #print(slope)
    slope.sort(key = lambda s: s[1]) #æ đææįæåš
    slope.reverse() #įąåĪ§å°å°
    #print('slope :',slope)
    #print(etf_data)
        
    #print(total_data)
    #print(total_data[0][1][0])
    recommend_count = recommend_count #æĻčĶåæļ
    recommended = 0 
    reply = ''
    chosen = []
    for i in slope:
        temp_data = etf_data[i[0]]
        #print('temp data :',temp_data)
        price = stock_price(i[0])
        #print('price :',price)
        if temp_data.iat[-1,-6] < temp_data.iat[-1,-2]:
            reply += i[0]+'.TWä―æžæēč§į·ïžčĄįĨĻåđæ ž : '+price+'ïžåŊčē·éē\n'
            recommended += 1
            chosen.append(i[0])
            if recommended == recommend_count:
                break
            else:continue
            #return reply
        else:continue
        if reply == '':
            return 'none'
    #print(reply)
    #print(chosen)
    return reply,chosen
        
        
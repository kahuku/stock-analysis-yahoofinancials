from datetime import datetime
from datetime import *
from dateutil.relativedelta import *
import requests
from yahoofinancials import YahooFinancials
import csv
import os
import pandas as pd
import numpy
import smtplib
import imghdr
from email.message import EmailMessage
import re
import time
import ssl



DATE_RANGE1 = 19
DATE_RANGE2 = 99
today = datetime.date(datetime.now())#saves today's date in correct form
errorLog = []

tickersList = ['']
fmaList = ['Fast MA']
smaList = ['Slow MA']
rsiList = ['RSI']
actionList = ['Action']
reasonList = ['Reason']
listsList = [tickersList,fmaList,smaList,rsiList,actionList,reasonList]

def get_start_date(ticker, start_date, days_prior):
    start_date = str(start_date)
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    prior_to_start_date_dt = start_date_dt - relativedelta(days=2 * days_prior)
    prior_to_start_date = prior_to_start_date_dt.strftime('%Y-%m-%d')

    yahoo_financials = YahooFinancials(ticker)

    df = yahoo_financials.get_historical_price_data(
        prior_to_start_date, start_date, 'daily')
    df = pd.DataFrame(df[ticker]['prices'])['formatted_date']
    if df.iloc[-1] == start_date:
        days_prior += 1

    try:
        new_start_date = df.iloc[-days_prior]
    except:
        new_start_date = today
    return new_start_date

def dataGet(tickerS):
    
    tickerS = tickerS.upper()
    
    yahoo_financials = YahooFinancials(tickerS)#uses ticker to gather data

    try:
        print(yahoo_financials.get_stock_quote_type_data()[tickerS]['shortName'])
        #shortName, longName, market
    except TypeError:
        print("Invalid input. Please enter a public ticker symbol.")
        return
    except Exception as e:
        None
        
    print(f"Stock analysis for {tickerS}")
    print()
    row1 = [yahoo_financials.get_stock_quote_type_data()[tickerS]['shortName'] + " - " + tickerS]


    start_date = get_start_date(tickerS, today, DATE_RANGE2)

    data = yahoo_financials.get_historical_price_data(start_date=str(start_date),end_date=str(today),time_interval='daily') 
    ticker_df = pd.DataFrame(data[tickerS]['prices'])#establishes panda dataframe based on the prices stats
    ticker_df = ticker_df.drop('date', axis=1).set_index('formatted_date')#date is going down i think, not really sure
    ticker_df.head()
    dataToPrint = ticker_df['open'] + ticker_df['close']
    dataToPrint = dataToPrint / 2
    #print(round(dataToPrint,2))#shows table



    pricesArray = [] 
    
    for row in dataToPrint:
        pricesArray.append(round(row,2))

    

    smallPricesArray = pricesArray[-DATE_RANGE1:]
    maFast = 0
    for elem in smallPricesArray:
        maFast += elem
    maFast /= len(smallPricesArray)
    maFast = round(maFast, 2)
    print("\nFast MA:", maFast)
    fmaList.append(maFast)



    maSlow = 0
    for elem in pricesArray:
        maSlow += elem
    maSlow /= len(pricesArray)
    maSlow = round(maSlow,2)
    print("Slow MA:", maSlow)
    smaList.append(maSlow)


    previousDayMaFast = 0
    previousDayPrices = pricesArray[-(DATE_RANGE1+1):-1]
    for elem in previousDayPrices:
        previousDayMaFast += elem
    previousDayMaFast /= len(previousDayPrices)
    previousDayMaFast = round(previousDayMaFast, 2)
    print("Previous day MA:", previousDayMaFast)



    start_date = get_start_date(tickerS, today, 30)

    dataClose = yahoo_financials.get_historical_price_data(start_date=str(start_date),end_date=str(today),time_interval='daily') 
    close_df = pd.DataFrame(dataClose[tickerS]['prices'])#establishes panda dataframe based on the prices stats
    close_df = close_df.drop('date', axis=1).set_index('formatted_date')#date is going down i think, not really sure
    close_df.head()
    closeData = close_df['close']
    clsoeData = closeData.tolist()
    closeData = closeData[-14:]

    closePrices = []
    for row in closeData:
        closePrices.append(round(row,2))


    #print(closePrices)

    totalGain = 0
    totalLoss = 0
    i = 1
    while i < (len(closePrices) - 1):
        change = closePrices[i+1] - closePrices[i]
        if change > 0:
            totalGain += change
        elif change < 0:
            totalLoss += -(change)
        i += 1

    avgGain = totalGain / 14
    avgLoss = totalLoss / 14
    
    rs = avgGain/avgLoss
    rsi = int(100 - (100/(1+rs)))
    print("RSI:",rsi)
    rsiList.append(rsi)


    

    reasons = []
    actions = []
    
    #RSI Strategy
    if rsi <= 30:
        print("buy",tickerS,"rsi")
        reasons.append('RSI')
        actions.append('Buy')

    elif rsi >= 70:
        print("sell",tickerS,"rsi")
        reasons.append('RSI')
        actions.append('Sell')


    #MA Crossover Strategy
    if ((previousDayMaFast < maSlow) & (maFast > maSlow)):
        print("buy more", tickerS,"MA Cross")
        reasons.append('MA Cross')
        actions.append('Buy')

    elif ((previousDayMaFast > maSlow) & (maFast < maSlow)):
        print("sell", tickerS,"MA Cross")
        reasons.append('MA Cross')
        actions.append('Sell')
    
    #SMA Stragegy
    if ((pricesArray[-2] < maFast) & (pricesArray[-1] > maFast)):
        print("buy more", tickerS,"SMA")
        reasons.append('SMA')
        actions.append('Buy')


    elif ((pricesArray[-2] > maFast) & (pricesArray[-1] < maFast)):
        print("sell", tickerS,"SMA")
        reasons.append('SMA')
        actions.append('Sell')
    
    if reasons:
        reasonList.append(reasons)
    else:
        reasonList.append('')

    if actions:
        actionList.append(actions)
    else:
        actionList.append('')





    

    
if __name__ == "__main__":
    
    print(today)
    open_file = open('/Users/drew/Documents/Python/Stocks/yahoofinancials/tickers_list.csv', 'r')
    reader = csv.reader(open_file)
    for ticker in reader:
        dataGet(ticker[0])
        tickersList.append(ticker[0])
        print('\n')
        errorLog = []
    

    fileName = '/Users/drew/Documents/Python/Stocks/yahoofinancials/csv_files/auto_reports/' + str(today) +'.csv'
    open_file = open(fileName, 'w')
    writer = csv.writer(open_file)
    for l in listsList:
        writer.writerow(l)
    open_file.close()

    EMAIL_ADDRESS = 'kevin.watts0608@gmail.com'
    EMAIL_PASSWORD = "Spankin' Fuhriman"


    get_content = []
    j = 1
    while j < (len(actionList)):
        if actionList[j] != '':
            strToAppend = (str(actionList[j][0]) + ' ' + str(tickersList[j]))
            get_content.append(strToAppend)
        j += 1
        
    print(get_content)

    message = (f'Drew,\nHere are the moves for today:\n\t{get_content}\n\nThe detailed information has been saved in the csv_files/auto_reports folder under today\'s date.')
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = f"Moves for {today}"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = "buzzinbubba@gmail.com"
        server.send_message(msg)
    print('sent')
    

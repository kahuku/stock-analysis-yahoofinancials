from datetime import datetime
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


DATE_RANGE1 = 19
DATE_RANGE2 = 99
today = datetime.date(datetime.now())#saves today's date in correct form
errorLog = []

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

    new_start_date = df.iloc[-days_prior]

    return new_start_date

def dataGet(tickerS, fileName):

    
    if (fileName != ''):
        filepath = "csv_files/" + fileName
    else:
        filepath = "csv_files/DELETEME"
    open_file = open(filepath, 'w')
    writer = csv.writer(open_file)#, delimiter='\t')
    
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
    writer.writerow(row1)

    start_date = get_start_date(tickerS, today, DATE_RANGE2)

    data = yahoo_financials.get_historical_price_data(start_date=str(start_date),end_date=str(today),time_interval='daily') 
    ticker_df = pd.DataFrame(data[tickerS]['prices'])#establishes panda dataframe based on the prices stats
    ticker_df = ticker_df.drop('date', axis=1).set_index('formatted_date')#date is going down i think, not really sure
    ticker_df.head()
    dataToPrint = ticker_df['open'] + ticker_df['close']
    dataToPrint = dataToPrint / 2
    #print(round(dataToPrint,2))#shows table


#    for row in dataToPrint.iloc[0:-1]:
 #       writer.writerow([round(row,2)])


    pricesArray = [] 
    
    for row in dataToPrint:
        writer.writerow([round(row,2)])
        pricesArray.append(round(row,2))

    for element in pricesArray[-20:]:
        print(element)

    

    smallPricesArray = pricesArray[-DATE_RANGE1:]
    maFast = 0
    for elem in smallPricesArray:
        maFast += elem
    maFast /= len(smallPricesArray)
    maFast = round(maFast, 2)
    print("\nFast MA:", maFast)


    maSlow = 0
    for elem in pricesArray:
        maSlow += elem
    maSlow /= len(pricesArray)
    maSlow = round(maSlow,2)
    print("Slow MA:", maSlow)

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


    print(closePrices)

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

    


    #RSI Strategy
    #if rsi <= 30:
     #   print("buy",tickerS)
    #elif rsi >= 70:
     #   print("sell",tickerS)

    #MA Crossover Strategy
    #if ((previousDayMaFast < maSlow) & (maFast > maSlow)):
     #   print("buy more", tickerS)
    #elif ((previousDayMaFast > maSlow) & (maFast < maSlow)):
     #   print("sell", tickerS)
    
    #SMA Stragegy
    #if ((pricesArray[-2] < ma) & (pricesArray[-1] > ma)):
     #   print("buy more", tickerS)

    #elif ((pricesArray[-2] > ma) & (pricesArray[-1] < ma)):
     #   print("sell", tickerS)
    






    open_file.close()
    if (filepath == "csv_files/DELETEME"):
        os.remove(filepath)

    
if __name__ == "__main__":
    
    print(today)
    symbol = input("Enter the symbol to check: ")
    fileToWrite = input("Enter the name of the file: ")
    flag = False
    while flag == False:
        dataGet(symbol, fileToWrite)
        print('\n')
        if errorLog != []:
           #print(errorLog)
           print()
        errorLog = []
        print("\n")
        symbol = input("Enter another symbol or done to quit: ")
        if symbol == "done":
            flag = True
        else:
            fileToWrite = input("Enter the name of the file: ")


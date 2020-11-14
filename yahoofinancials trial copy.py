#https://pypi.org/project/yahoofinancials/
#https://towardsdatascience.com/a-comprehensive-guide-to-downloading-stock-prices-in-python-2cd93ff821d4
#https://github.com/JECSand/yahoofinancials


#FCF

from datetime import datetime
from bs4 import BeautifulSoup
import requests
from yahoofinancials import YahooFinancials
import csv
import os


today = datetime.date(datetime.now())#saves today's date in correct form
errorLog = []

def dataGet(tickerS, fileName):
    if (fileName != ''):
        filepath = "csv_files/" + fileName
    else:
        filepath = "csv_files/DELETEME"
    open_file = open(filepath, 'w')
    writer = csv.writer(open_file)#, delimiter='\t')
    
    tickerS = tickerS.upper()
    
    yahoo_financials = YahooFinancials(tickerS)#uses ticker to gather data

    gEstimate = input("Estimate 7-10 yr earnings growth %: ")
    print('\n')
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
    """
    #table of formatted date, high, low, open, close, volume, adj close
    #gets prices. Can pass arguments time interval, start&end dates
    data = yahoo_financials.get_historical_price_data(start_date='2020-01-01',end_date='2020-06-30',time_interval='weekly') 
    ticker_df = pd.DataFrame(data[tickerS]['prices'])#establishes panda dataframe based on the prices stats
    ticker_df = ticker_df.drop('date', axis=1).set_index('formatted_date')#date is going down i think, not really sure
    ticker_df.head()
    print(ticker_df)#shows table
    """

    #list of other useful functions with formatting
    #"${:,.2f}".format(amount) #formatting format for grouped prices
    #"{:,}".format(amount) #formatting format for grouped numbers
    #"{:.0%}".format(a_number) #formatting format for a percent from decimal
    ljust1 = 8
    ljust2 = 17
    ljust3 = 24

    #price
    try:
        price = yahoo_financials.get_current_price()
        price_f = "${:,.2f}".format(price)
        print(("Price: ").ljust(ljust1),price_f)
        rowToWrite = ["Price", price_f]
        writer.writerow(rowToWrite)
    except Exception as e:
        errorLog.append(e)
        print(("Price: ").ljust(ljust1),"error loading")
        writer.writerow(["Price", None])

    #MC
    try:
        marketCap = (yahoo_financials.get_summary_data()[tickerS]['marketCap'])
        print(("Market Cap: ").ljust(ljust1),"{:,}".format(marketCap))
        writer.writerow(["Market Cap", "{:,}".format(marketCap)])
    except Exception as e:
        errorLog.append(e)
        print(("Market Cap: ").ljust(ljust1),"error loading")
        writer.writerow(["Market Cap", None])
    
    print()
    
    #beta
    try:
        beta = round(yahoo_financials.get_beta(),3)
        print(("Beta: ").ljust(ljust1), beta)
        writer.writerow(["Beta",beta])
    except TypeError:
        print(("Beta: ").ljust(ljust1), None)
        writer.writerow(["Beta",None])
    except Exception as e:
        errorLog.append(e)
        print(("Beta: ").ljust(ljust1), "error loading")
        writer.writerow(["Beta", None])

    print()
    #eps
    try:  
        eps = yahoo_financials.get_earnings_per_share()
        eps_f = "${:,.2f}".format(eps)
        print(("EPS: ").ljust(ljust2) ,eps_f)
        writer.writerow(["EPS", eps_f])
    except TypeError:
        print(("EPS: ").ljust(ljust2) ,None)
        writer.writerow(["EPS", None])
    except Exception as e:
        errorLog.append(e)
        print(("EPS: ").ljust(ljust2) ,"error loading")
        writer.writerow(["EPS", None])

    #pe  
    try:
        pe = round(yahoo_financials.get_pe_ratio(),3)
        print(("P/E: ").ljust(ljust2), pe)
        writer.writerow(["PE",pe])
    except TypeError:
        print(("P/E: ").ljust(ljust2), None)
        writer.writerow(["PE", None])
    except Exception as e:
        errorLog.append(e)
        print(("P/E: ").ljust(ljust2), "error loading")
        writer.writerow(["PE",None])

    #PEG
    try:
        gSite = 'http://finance.yahoo.com/quote/' + tickerS + '/key-statistics?p=' + tickerS
        gSource = requests.get(gSite).text
        gSoup = BeautifulSoup(gSource, 'lxml')
        
        gTable = gSoup.find('table')
        #print(gTable)
        #print('\n')
        gLog = []
        for gTag in gTable.find_all('tr'):
            #print(gTag)
            gLog.append(gTag)

        gRow = gLog[5]
        #print(gRow)
        pegLog = []
        for gThing in gRow.find_all('td'):
            #print(gThing.text)
            pegLog.append(gThing.text)

        print(("PEG: ").ljust(ljust2),pegLog[1])
        writer.writerow(["PEG",pegLog[1]])
    except Exception as e:
        errorLog.append(e)
        print(("PEG: ").ljust(ljust2),"error loading")
        writer.writerow(["PEG",None])
        
    #earnings yield
    try:
        ey = 1/pe
        print(("Earnings yield: ").ljust(ljust2),"{:.2%}".format(ey))
        writer.writerow(["Earnings yield","{:.2%}".format(ey)])
    except Exception as e:
        errorLog.append(e)
        print(("Earnigns Yield: ").ljust(ljust2),"error loading")
        writer.writerow(["Earnings yield", None])

    #forwardEPS
    try:
        forwardEps = yahoo_financials.get_key_statistics_data()[tickerS]['forwardEps']
        print(("Forward EPS: ").ljust(ljust2),"${:,.2f}".format(forwardEps))
        writer.writerow(["Foward EPS","${:,.2f}".format(forwardEps)])
    except Exception as e:
        errorLog.append(e)
        print(("Forward EPS: ").ljust(ljust2),"error loading")
        writer.writerow(["ForwardEPS",None])
        
    #forwardPE
    try:
        forwardPE = yahoo_financials.get_key_statistics_data()[tickerS]['forwardPE']
        print(("Forward PE: ").ljust(ljust2),round(forwardPE,3))
        writer.writerow(["Forward PE", round(forwardPE,3)])
    except Exception as e:
        errorLog.append(e)
        print(("Forward PE: ").ljust(ljust2),"error loading")
        writer.writerow(["Forward PE",None])

    #earnings quarterly growth
    try:
        eqg = yahoo_financials.get_key_statistics_data()[tickerS]['earningsQuarterlyGrowth']
        print(("Earnings Quarterly Growth: ").ljust(ljust2),"{:.2%}".format(eqg))
        writer.writerow(["EQG", "{:.2%}".format(eqg)])
    except TypeError:
        writer.writerow(["EQG", None])
    except Exception as e:
        errorLog.append(e)
        print(("Earnings Quarterly Growth: ").ljust(ljust2),"error loading")
        writer.writerow(["EQG",None])

    print()
    
    #ptb
    try:
        ptb = round(yahoo_financials.get_key_statistics_data()[tickerS]['priceToBook'],3)
        print(("PTB: ").ljust(ljust2),ptb)
        writer.writerow(["PTB",ptb])
    except Exception as e:
        try:
            book_value = yahoo_financials.get_book_value()
            #print(("Book Value: ").ljust(ljust) + "${:,.2f}".format(book_value))

            ks = yahoo_financials.get_key_statistics_data()
            shares_outstanding = ks[tickerS]['sharesOutstanding']
            #print(("# of shares: ").ljust(ljust) + "{:,}".format(shares_outstanding))

            all_price = shares_outstanding*price
            book_value_per_share = book_value/shares_outstanding
            price_to_bvps = price/book_value_per_share
            print(("PTB: ").ljust(ljust2),round(price_to_bvps,3))
            writer.writerow(["PTB",round(price_to_bvps,3)])
        except Exception as e:
            errorLog.append(e)
            print(("PTB: ").ljust(ljust2),"error loading")
            writer.writerow(["PTB",None])

    #fair value
    try:
        if gEstimate != '':
            fairValue1 = (eps*(7+int(gEstimate))*4.4)/3
            fairValue2 = (eps*(8.5+int(gEstimate))*4.4)/2.44
            print(("Fair value low: ").ljust(ljust2),"${:,.2f}".format(fairValue1))
            print(("Fair value high: ").ljust(ljust2),"${:,.2f}".format(fairValue2))
            writer.writerow(["Fair value low", "${:,.2f}".format(fairValue1)])
            writer.writerow(["Fair value high", "${:,.2f}".format(fairValue2)])
        else:
            g = pegLog[1]
            g = float(g)
            g = 1/g
            g *= pe
            fairValue1 = (eps*(7+g)*4.4)/3
            fairValue2 = (eps*(8.5+g)*4.4)/2.44
            print(("Fair value low: ").ljust(ljust2),"${:,.2f}".format(fairValue1))
            print(("Fair value high: ").ljust(ljust2),"${:,.2f}".format(fairValue2))
            writer.writerow(["Fair value low", "${:,.2f}".format(fairValue1)])
            writer.writerow(["Fair value high", "${:,.2f}".format(fairValue2)])

    except Exception as e:
        errorLog.append(e)
        print(("Fair value: ").ljust(ljust2),"error loading")
        writer.writerow(["Fair value",None])
    
    #AL     
    try:
        #Balance sheet data. Freq can be annual or quarterly. Statement type = income, balance, cash. Reformat defaults true 
        balance_sheet_data_qt = yahoo_financials.get_financial_stmts(frequency='quarterly', statement_type='balance', reformat='True')
        #print(balance_sheet_data_qt)

        assets = balance_sheet_data_qt['balanceSheetHistoryQuarterly'][tickerS][0]
        #assets = next(iter(assets))
        assets = assets[next(iter(assets))]
        liab = assets['totalLiab']
        total_assets = assets['totalAssets']
        a_l_ratio = total_assets/liab
        print(("A/L ratio: ").ljust(ljust2),round(a_l_ratio,3))
        writer.writerow(["AL", round(a_l_ratio,3)])
    except Exception as e:
        errorLog.append(e)
        print(("A/L ratio: ").ljust(ljust2),"error loading")
        writer.writerow(["AL",None])

    #Profit margin
    try:
        profitMargins = yahoo_financials.get_key_statistics_data()[tickerS]['profitMargins']
        #profitMargins = round(profitMargins, 4)
        print(("Profit margin: ").ljust(ljust2),"{:.2%}".format(profitMargins))
        writer.writerow(["Profit margin", "{:.2%}".format(profitMargins)])
    except Exception as e:
        errorLog.append(e)
        print(("Profit margin: ").ljust(ljust2),"error loading")
        writer.writerow(["Profit margin", None])


    #ROE
    try:
        site = 'http://finance.yahoo.com/quote/' + tickerS + '/key-statistics?p=' + tickerS
        source = requests.get(site).text
        soup = BeautifulSoup(source, 'lxml')
        tables = soup.find('div',class_="Mb(10px) Pend(20px) smartphone_Pend(0px)")
        taglog = []
        #print(tables)
        for tag in tables.find_all('td'):
            #print(tag.text)
            taglog.append(tag.text)
        print(("ROE: ").ljust(ljust2),taglog[11])
        writer.writerow(["ROE", taglog[11]])

    except Exception as e:
        errorLog.append(e)
        print(("ROE: ").ljust(ljust2), "error loading")
        writer.writerow(["ROE", None])

    #FCF
    try:
        fSite = 'http://finance.yahoo.com/quote/' + tickerS + '/cash-flow/'
        fSource = requests.get(fSite).text
        fSoup = BeautifulSoup(fSource, 'lxml')

        """
        fLog1 = []
        fLog2 = []
        for fTag in fSoup.find_all('div',class_="Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)"):
            #print(fTag.text)
            fLog1.append(fTag.text)
        for fTag2 in fSoup.find_all('div',class_="Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(tbc)"):
            #print(fTag2.text)
            fLog2.append(fTag2.text)
    
        #print(fLog1[33])
        #print(fLog2[22])
        #print(fLog1[34])
        #print(fLog2[23])
        #print(fLog1[35])
        
        print(("FCF: ").ljust(ljust2),fLog1[33])
        """
        fSoup = fSoup.find('div',class_="D(tbrg)")
        #print(fSoup)
        fSoupCut = []
        fcfList = []
        for item in fSoup.find_all('div', attrs={"data-test":"fin-row"}):
            fSoupCut.append(item)
        fSoupCut = fSoupCut[::-1]
        fSoupCut = fSoupCut[0]
        for row in fSoupCut.find_all('div', attrs={"data-test":"fin-col"}):
            #print(row.text)
            fcfList.append(row.text)



        print(("FCF: ").ljust(ljust2), fcfList[0])
        writer.writerow(["FCF", fcfList[0]])
        i = 0
        for i in range(0,len(fcfList)):
            fcfList[i] = fcfList[i].replace(',','') 
            fcfList[i] = int(fcfList[i])
            i += 1
    except Exception as e:
        errorLog.append(e)
        print(("FCF: ").ljust(ljust2),"error loading")
        writer.writerow(["ROE", None])

    try:
        fcfG = (fcfList[0] - fcfList[1])/fcfList[1]
        if fcfG == 0:
            fcfG = (fcfList[1] - fcfList[2])/fcfList[2]
        print(("FCF growth: ").ljust(ljust2),"{:.0%}".format(fcfG))
        writer.writerow(["FCF growth", "{:.0%}".format(fcfG)])
    except Exception as e:
        errorLog.append(e)
        print(("FCF growth: ").ljust(ljust2),"error loading")
        writer.writerow(["FCF growth", None])

    try:
        fcf5 = 0
        j = 0
        if len(fcfList) < 5:
            for value in fcfList:
                fcf5 += value
            fcf5 /= len(fcfList)
        
        else:
            for j in range(0,5):
                fcf5 += fcfList[j]
            fcf5 /= 5
        print(("5 yr avg FCF: ").ljust(ljust2),"{:,}".format(fcf5))
        writer.writerow(["5 yr avg FCF", "{:,}".format(fcf5)])
    except Exception as e:
        errorLog.append(e)
        print(("5 yr avg FCF: ").ljust(ljust2),"error loading")
        writer.writerow(["5 yr avg FCF", None])

    print()
    """
    try:
        rqg = yahoo_financials.get_key_statistics_data()[tickerS]['revenueQuarterlyGrowth']
        print(("Revenue Quarterly Growth: ").ljust(ljust),rqg)
    except Exception as e:
        errorLog.append(e)
        print(("Revenue Quarterly Growth: ").ljust(ljust),"error loading")
    """



    #print(yahoo_financials.get_financial_stmts('quarterly', 'income')['incomeStatementHistoryQuarterly'][tickerS])
    ##netIncome, grossProfit, operatingIncome, totalRevenue, totalOperatingExpenses, costOfRevenue, netIncomeApplicableToCommonShares
    ##quarterly displays all this information for each of the past four quarers in a dictionary with it's quarter's date on it
     
    #print(yahoo_financials.get_financial_stmts('quarterly','balance'))
    ##capitalSurplus, totalAssets, retainedEarnings, cash,totalCurrentAssets,

    #print(yahoo_financials.get_financial_stmts('quarterly','cash'))
    ##totalCashflowsFromInvestingActivities,netIncome, changeInCash, totalCashFromOperatingActivities, depreciation, changeToNetincome 

    #print(yahoo_financials.get_summary_data())
    ##twoHundredDayAverage, payoutRatio, averageDailyVolume10Day, beta, trailingPE, fiftyDayAverage
    
    #operating income, current volume, 10 day avg volume, 3 mo average volume, dividend rat

    #50 day average
    try:
        avg50 = yahoo_financials.get_summary_data()[tickerS]['fiftyDayAverage']
        print(("50 Day Average: ").ljust(ljust2),"${:,.2f}".format(avg50))
        writer.writerow(["50 Day Average", "${:,.2f}".format(avg50)])
    except Exception as e:
        errorLog.append(e)
        print(("50 Day Average: ").ljust(ljust2),"error loading")
        writer.writerow(["50 Day Average", None])

    #200 day average
    try:
        avg200 = yahoo_financials.get_summary_data()[tickerS]['twoHundredDayAverage']
        print(("200 Day Average: ").ljust(ljust2),"${:,.2f}".format(avg200))
        writer.writerow(["200 Day Average", "${:,.2f}".format(avg200)])
    except Exception as e:
        errorLog.append(e)
        print(("200 Day Average: ").ljust(ljust2),"error loading")
        writer.writerow(["200 Day Average", None])
    print()
    """
    #payout ratio
    try:
        payout = yahoo_financials.get_summary_data()[tickerS]['payoutRatio']
        print(("Payout Ratio: ").ljust(ljust1),"{:.0%}".format(payout))
    except Exception as e:
        errorLog.append(e)
        print(("Payout Ratio: ").ljust(ljust1),"error loading")
    print()
    """
    #volume
    try:
        vol = yahoo_financials.get_summary_data()[tickerS]['volume']
        print(("Volume: ").ljust(ljust3),"{:,}".format(vol))
        writer.writerow(["Volume", "{:,}".format(vol)])
    except Exception as e:
        errorLog.append(e)
        print(("Volume: ").ljust(ljust3),"error loading")
        writer.writerow(["Volume", None])

    #10 day volume
    try:
        vol10day = yahoo_financials.get_summary_data()[tickerS]['averageDailyVolume10Day']
        print(("10 Day Average Volume: ").ljust(ljust3),"{:,}".format(vol10day))
        writer.writerow(["10 Day Average Volume", "{:,}".format(vol10day)])
    except Exception as e:
        errorLog.append(e)
        print(("10 Day Average Volume: ").ljust(ljust3),"error loading")
        writer.writerow(["10 Day Average Volume", None])

    #3 month volume
    try:
        vol3mo = yahoo_financials.get_three_month_avg_daily_volume()
        print(("3 Month Average Volume: ").ljust(ljust3),"{:,}".format(vol3mo))
        writer.writerow(["3 Month Average Volume", "{:,}".format(vol3mo)])
    except Exception as e:
        errorLog.append(e)
        print(("3 Month Average Volume: ").ljust(ljust3),"error loading")
        writer.writerow(["3 Month Average Volume", None])

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


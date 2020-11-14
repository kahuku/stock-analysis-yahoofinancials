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


tickersList = ["Tickers"]
priceList = ["Price"]
mcList = ["Market cap"]
betaList = ["Beta"]
epsList = ["EPS"]
peList = ["PE"]
pegList = ["PEG"]
eyList = ["Earnings yield"]
fepsList = ["Forward EPS"]
fpeList = ["Forward PE"]
eqgList= ["Earnings Quarterly Growth"]
ptbList = ["PTB"]
fvlList = ["Fair value low"]
fvhList = ["Fair value high"]
alrList = ["A/L Ratio"]
pmList = ["Profit margins"]
roeList = ["ROE"]
fcfL = ["FCF"]
fcfgList = ["FCF Growth"]
fcf5List = ["5 yr avg FCF"]
ma50 = ["MA 50"]
ma200 = ["MA 200"]
volList = ["Volume"]
vol10 = ["10 Day Avg Vol"]
vol3 = ["3 Month Avg Vol"]

listsList = [tickersList, priceList, mcList, betaList, epsList, peList, pegList, eyList, fepsList, fpeList, eqgList, ptbList, fvlList, fvhList, alrList, pmList, roeList, fcfL, fcfgList, fcf5List, ma50, ma200, volList, vol3, vol10]


def dataGet(tickerS):
    
    tickerS = tickerS.upper()
    
    yahoo_financials = YahooFinancials(tickerS)#uses ticker to gather data

    #gEstimate = input(f"Estimate 7-10 yr earnings growth % for {tickerS}: ")
    gEstimate = ''
    #print('\n')
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
    tickersList.append(tickerS)
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
        priceList.append(price_f)
    except Exception as e:
        errorLog.append(e)
        print(("Price: ").ljust(ljust1),"error loading")
        priceList.append('')

    #MC
    try:
        marketCap = (yahoo_financials.get_summary_data()[tickerS]['marketCap'])
        print(("Market Cap: ").ljust(ljust1),"{:,}".format(marketCap))
        mcList.append("{:,}".format(marketCap))
    except Exception as e:
        errorLog.append(e)
        print(("Market Cap: ").ljust(ljust1),"error loading")
        mcList.append('')
    
    print()
    
    #beta
    try:
        beta = round(yahoo_financials.get_beta(),3)
        print(("Beta: ").ljust(ljust1), beta)
        betaList.append(beta)
    except TypeError:
        print(("Beta: ").ljust(ljust1), None)
        betaList.append('')
    except Exception as e:
        errorLog.append(e)
        print(("Beta: ").ljust(ljust1), "error loading")
        betaList.append('')
    print()
    
    #eps
    try:  
        eps = yahoo_financials.get_earnings_per_share()
        eps_f = "${:,.2f}".format(eps)
        print(("EPS: ").ljust(ljust2) ,eps_f)
        epsList.append(eps_f)
    except TypeError:
        print(("EPS: ").ljust(ljust2) ,None)
        epsList.append('')
    except Exception as e:
        errorLog.append(e)
        print(("EPS: ").ljust(ljust2) ,"error loading")
        epsList.append('')

    #pe  
    try:
        pe = round(yahoo_financials.get_pe_ratio(),3)
        print(("P/E: ").ljust(ljust2), pe)
        peList.append(pe)
    except TypeError:
        print(("P/E: ").ljust(ljust2), None)
        peList.append('')
    except Exception as e:
        errorLog.append(e)
        print(("P/E: ").ljust(ljust2), "error loading")
        peList.append('')

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
        pegList.append(pegLog[1])
    except Exception as e:
        errorLog.append(e)
        print(("PEG: ").ljust(ljust2),"error loading")
        pegList.append('')
        
    #earnings yield
    try:
        ey = 1/pe
        print(("Earnings yield: ").ljust(ljust2),"{:.2%}".format(ey))
        eyList.append("{:.2%}".format(ey))
    except Exception as e:
        errorLog.append(e)
        print(("Earnigns Yield: ").ljust(ljust2),"error loading")
        eyList.append('')

    #forwardEPS
    try:
        forwardEps = yahoo_financials.get_key_statistics_data()[tickerS]['forwardEps']
        print(("Forward EPS: ").ljust(ljust2),"${:,.2f}".format(forwardEps))
        fepsList.append("${:,.2f}".format(forwardEps))
    except Exception as e:
        errorLog.append(e)
        print(("Forward EPS: ").ljust(ljust2),"error loading")
        fepsList.append('')
        
    #forwardPE
    try:
        forwardPE = yahoo_financials.get_key_statistics_data()[tickerS]['forwardPE']
        print(("Forward PE: ").ljust(ljust2),round(forwardPE,3))
        fpeList.append(round(forwardPE,3))
    except Exception as e:
        errorLog.append(e)
        print(("Forward PE: ").ljust(ljust2),"error loading")
        fpeList.append('')

    #earnings quarterly growth
    try:
        eqg = yahoo_financials.get_key_statistics_data()[tickerS]['earningsQuarterlyGrowth']
        print(("Earnings Quarterly Growth: ").ljust(ljust2),"{:.2%}".format(eqg))
        eqgList.append("{:.2%}".format(eqg))
    except TypeError:
        eqgList.append('')
    except Exception as e:
        errorLog.append(e)
        print(("Earnings Quarterly Growth: ").ljust(ljust2),"error loading")
        eqgList.append('')

    print()
    
    #ptb
    try:
        ptb = round(yahoo_financials.get_key_statistics_data()[tickerS]['priceToBook'],3)
        print(("PTB: ").ljust(ljust2),ptb)
        ptbList.append(ptb)
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
            ptbList.append(round(price_to_bvps,3))
        except Exception as e:
            errorLog.append(e)
            print(("PTB: ").ljust(ljust2),"error loading")
            ptbList.append('')

    #fair value
    try:
        if gEstimate != '':
            fairValue1 = (eps*(7+int(gEstimate))*4.4)/3
            fairValue2 = (eps*(8.5+int(gEstimate))*4.4)/2.44
            print(("Fair value low: ").ljust(ljust2),"${:,.2f}".format(fairValue1))
            print(("Fair value high: ").ljust(ljust2),"${:,.2f}".format(fairValue2))
            fvlList.append("${:,.2f}".format(fairValue1))
            fvhList.append("${:,.2f}".format(fairValue2))
        else:
            g = pegLog[1]
            g = float(g)
            g = 1/g
            g *= pe
            fairValue1 = (eps*(7+g)*4.4)/3
            fairValue2 = (eps*(8.5+g)*4.4)/2.44
            print(("Fair value low: ").ljust(ljust2),"${:,.2f}".format(fairValue1))
            print(("Fair value high: ").ljust(ljust2),"${:,.2f}".format(fairValue2))
            fvlList.append("${:,.2f}".format(fairValue1))
            fvhList.append( "${:,.2f}".format(fairValue2))

    except Exception as e:
        errorLog.append(e)
        print(("Fair value: ").ljust(ljust2),"error loading")
        fvlList.append('')
        fvhList.append('')
    
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
        alrList.append(round(a_l_ratio,3))
    except Exception as e:
        errorLog.append(e)
        print(("A/L ratio: ").ljust(ljust2),"error loading")
        alrList.append('')

    #Profit margin
    try:
        profitMargins = yahoo_financials.get_key_statistics_data()[tickerS]['profitMargins']
        #profitMargins = round(profitMargins, 4)
        print(("Profit margin: ").ljust(ljust2),"{:.2%}".format(profitMargins))
        pmList.append("{:.2%}".format(profitMargins))
    except Exception as e:
        errorLog.append(e)
        print(("Profit margin: ").ljust(ljust2),"error loading")
        pmList.append('')


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
        roeList.append(taglog[11])

    except Exception as e:
        errorLog.append(e)
        print(("ROE: ").ljust(ljust2), "error loading")
        roeList.append('')

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
        fcfL.append(fcfList[0])
        i = 0
        for i in range(0,len(fcfList)):
            fcfList[i] = fcfList[i].replace(',','') 
            fcfList[i] = int(fcfList[i])
            i += 1
    except Exception as e:
        errorLog.append(e)
        print(("FCF: ").ljust(ljust2),"error loading")
        fcfL.append('')

    try:
        fcfG = (fcfList[0] - fcfList[1])/fcfList[1]
        if fcfG == 0:
            fcfG = (fcfList[1] - fcfList[2])/fcfList[2]
        print(("FCF growth: ").ljust(ljust2),"{:.0%}".format(fcfG))
        fcfgList.append("{:.0%}".format(fcfG))
    except Exception as e:
        errorLog.append(e)
        print(("FCF growth: ").ljust(ljust2),"error loading")
        fcfgList.append('')

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
        fcf5List.append("{:,}".format(fcf5))
    except Exception as e:
        errorLog.append(e)
        print(("5 yr avg FCF: ").ljust(ljust2),"error loading")
        fcf5List.append('')

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
        ma50.append("${:,.2f}".format(avg50))
    except Exception as e:
        errorLog.append(e)
        print(("50 Day Average: ").ljust(ljust2),"error loading")
        ma50.append('')

    #200 day average
    try:
        avg200 = yahoo_financials.get_summary_data()[tickerS]['twoHundredDayAverage']
        print(("200 Day Average: ").ljust(ljust2),"${:,.2f}".format(avg200))
        ma200.append("${:,.2f}".format(avg200))
    except Exception as e:
        errorLog.append(e)
        print(("200 Day Average: ").ljust(ljust2),"error loading")
        ma200.append('')
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
        volList.append("{:,}".format(vol))
    except Exception as e:
        errorLog.append(e)
        print(("Volume: ").ljust(ljust3),"error loading")
        volList.append('')

    #10 day volume
    try:
        vol10day = yahoo_financials.get_summary_data()[tickerS]['averageDailyVolume10Day']
        print(("10 Day Average Volume: ").ljust(ljust3),"{:,}".format(vol10day))
        vol10.append("{:,}".format(vol10day))
    except Exception as e:
        errorLog.append(e)
        print(("10 Day Average Volume: ").ljust(ljust3),"error loading")
        vol10.append('')

    #3 month volume
    try:
        vol3mo = yahoo_financials.get_three_month_avg_daily_volume()
        print(("3 Month Average Volume: ").ljust(ljust3),"{:,}".format(vol3mo))
        vol3.append("{:,}".format(vol3mo))
    except Exception as e:
        errorLog.append(e)
        print(("3 Month Average Volume: ").ljust(ljust3),"error loading")
        vol3.append('')

    

    
    
if __name__ == "__main__":
    
    print(today)
    numComps = int(input("How many companies would you like data for? "))
    compsList = []
    j = 0
    while (j < numComps):
        symbol = input(f"Enter symbol {j+1}: ")
        compsList.append(symbol)
        j += 1
    fileToWrite = input("Enter the name of the file: ")
    
    i = 0
    while (i < numComps):
        dataGet(compsList[i])
        print('\n')
        errorLog = []
        i += 1

    #write to file
    if (fileToWrite != ''):
        filepath = "/Users/drew/Documents/Python/Stocks/yahoofinancials/csv_files/" + fileToWrite
    else:
        filepath = "/Users/drew/Documents/Python/Stocks/yahoofinancials/csv_files/DELETEME"
    open_file = open(filepath, 'w')
    writer = csv.writer(open_file)
    #write here

    for l in listsList:
        writer.writerow(l)
    
    open_file.close()
    if (filepath == "/Users/drew/Documents/Python/Stocks/yahoofinancials/csv_files/DELETEME"):
        os.remove(filepath)

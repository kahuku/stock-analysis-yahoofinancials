#https://pypi.org/project/yahoofinancials/
#https://towardsdatascience.com/a-comprehensive-guide-to-downloading-stock-prices-in-python-2cd93ff821d4
#https://github.com/JECSand/yahoofinancials


#dividend statistics.
#formatting
#clean up commented code and spacing

from datetime import datetime
import pandas as pd
from yahoofinancials import YahooFinancials
import yfinance as yf
import matplotlib

today = datetime.date(datetime.now())#saves today's date in correct form
errorLog = []

def dataGet(tickerS):
    tickerS = tickerS.upper()
    
    yahoo_financials = YahooFinancials(tickerS)#uses ticker to gather data

    try:
        print(yahoo_financials.get_stock_quote_type_data()[tickerS]['shortName'])
        #shortName, longName, market
    except Exception as e:
        None
        
    print(f"Stock analysis for {tickerS}")
    print()
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
    except TypeError:
        print("Invalid input. Please enter a public ticker symbol.")
        return
    except Exception as e:
        errorLog.append(e)
        print(("Price: ").ljust(ljust1),"error loading")
    print()
    #beta
    try:
        beta = round(yahoo_financials.get_beta(),3)
        print(("Beta: ").ljust(ljust1), beta)
    except TypeError:
        print(("Beta: ").ljust(ljust1), None)
    except Exception as e:
        errorLog.append(e)
        print(("Beta: ").ljust(ljust1), "error loading")

    print()
    #eps
    try:  
        eps = yahoo_financials.get_earnings_per_share()
        eps_f = "${:,.2f}".format(eps)
        print(("EPS: ").ljust(ljust2) ,eps_f)
    except TypeError:
        print(("EPS: ").ljust(ljust2) ,None)
    except Exception as e:
        errorLog.append(e)
        print(("EPS: ").ljust(ljust2) ,"error loading")

    #pe  
    try:
        pe = round(yahoo_financials.get_pe_ratio(),3)
        print(("P/E: ").ljust(ljust2), pe)
    except TypeError:
        print(("P/E: ").ljust(ljust2), None)
    except Exception as e:
        errorLog.append(e)
        print(("P/E: ").ljust(ljust2), "error loading")

    #forwardEPS
    try:
        forwardEps = yahoo_financials.get_key_statistics_data()[tickerS]['forwardEps']
        print(("Forward EPS: ").ljust(ljust2),"${:,.2f}".format(forwardEps))
    except Exception as e:
        errorLog.append(e)
        print(("Forward EPS: ").ljust(ljust2),"error loading")
        
    #forwardPE
    try:
        forwardPE = yahoo_financials.get_key_statistics_data()[tickerS]['forwardPE']
        print(("Forward PE: ").ljust(ljust2),round(forwardPE,3))
    except Exception as e:
        errorLog.append(e)
        print(("Forward PE: ").ljust(ljust2),"error loading")

    #earnings quarterly growth
    try:
        eqg = yahoo_financials.get_key_statistics_data()[tickerS]['earningsQuarterlyGrowth']
        print(("Earnings Quarterly Growth: ").ljust(ljust2),"{:.0%}".format(eqg))
    except Exception as e:
        errorLog.append(e)
        print(("Earnings Quarterly Growth: ").ljust(ljust2),"error loading")

    print()
    
    #ptb
    try:
        ptb = round(yahoo_financials.get_key_statistics_data()[tickerS]['priceToBook'],3)
        print(("PTB: ").ljust(ljust2),ptb)
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
        except Exception as e:
            errorLog.append(e)
            print(("PTB: ").ljust(ljust2),"error loading")
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
    except Exception as e:
        errorLog.append(e)
        print(("A/L ratio: ").ljust(ljust2),"error loading")

    #Profit margin
    try:
        profitMargins = yahoo_financials.get_key_statistics_data()[tickerS]['profitMargins']
        #profitMargins = round(profitMargins, 4)
        print(("Profit margin: ").ljust(ljust2),"{:.2%}".format(profitMargins))
    except Exception as e:
        errorLog.append(e)
        print(("Profit margin: ").ljust(ljust2),"error loading")

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
    except Exception as e:
        errorLog.append(e)
        print(("50 Day Average: ").ljust(ljust2),"error loading")

    #200 day average
    try:
        avg200 = yahoo_financials.get_summary_data()[tickerS]['twoHundredDayAverage']
        print(("200 Day Average: ").ljust(ljust2),"${:,.2f}".format(avg200))
    except Exception as e:
        errorLog.append(e)
        print(("200 Day Average: ").ljust(ljust2),"error loading")
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
    except Exception as e:
        errorLog.append(e)
        print(("Volume: ").ljust(ljust3),"error loading")

    #10 day volume
    try:
        vol10day = yahoo_financials.get_summary_data()[tickerS]['averageDailyVolume10Day']
        print(("10 Day Average Volume: ").ljust(ljust3),"{:,}".format(vol10day))
    except Exception as e:
        errorLog.append(e)
        print(("10 Day Average Volume: ").ljust(ljust3),"error loading")

    #3 month volume
    try:
        vol3mo = yahoo_financials.get_three_month_avg_daily_volume()
        print(("3 Month Average Volume: ").ljust(ljust3),"{:,}".format(vol3mo))
    except Exception as e:
        errorLog.append(e)
        print(("3 Month Average Volume: ").ljust(ljust3),"error loading")



    
if __name__ == "__main__":
    
    print(today)
    symbol = input("Enter the symbol to check: ")
    flag = False
    while flag == False:
        print('\n')
        dataGet(symbol)
        print('\n')
        #if errorLog != []:
         #   print(errorLog)
          #  print()
        errorLog = []
        print("\n")
        symbol = input("Enter another symbol or done to quit: ")
        if symbol == "done":
            flag = True








#Graham principles- 1/3+ positive EPS growth
#Current assets to liabilities ratio of 1.5+
#Price to book value per share ratio of <1.5 or 1.2

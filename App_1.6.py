import datetime as dt
from flask import Flask, render_template, request # type: ignore
import numpy_financial as npf
import json

def Average(lst):
    return sum(lst) / len(lst)

def read_data(symbol):

    #file_path_ernings = r'D:\Python\Investing5.0\Local\SAMPLE_IBM_Earning.json'
    with open(file_path_ernings, 'r') as file:
        data_ernings = file.read()

    #file_path_dividends = r'D:\Python\Investing5.0\Local\SAMPLE_IBM_Dividends.json'
    with open(file_path_dividends, 'r') as file:
        data_dividends = file.read()

    #file_path_balancesheet =r'D:\Python\Investing5.0\Local\SAMPLE_IBM_Balance-sheet.json'
    with open(file_path_balancesheet, 'r') as file:
        data_balancesheet = file.read()
    
    #file_path_incomestatement = r'D:\Python\Investing5.0\Local\SAMPLE_IBM_Income-stetement.json'
    with open(file_path_incomestatement, 'r') as file:
        data_incomestatement = file.read()

    #file_path_price = r'D:\Python\Investing5.0\Local\SAMPLE_IBM_Price-time-series.json'
    with open(file_path_price, 'r') as file:
        data_price = file.read()
    
    # Parse the JSON data
    json_data_ernings = json.loads(data_ernings)
    json_data_dividends = json.loads(data_dividends)
    json_data_incomestatement = json.loads(data_incomestatement)
    json_data_balancesheet = json.loads(data_balancesheet)
    json_data_price = json.loads(data_price)

    json_data = [json_data_ernings, json_data_dividends, json_data_incomestatement, json_data_balancesheet, json_data_price]

    return json_data

def read_api(symbol):
    import requests

    url_eps = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey=AILA1I4F6KIGWUD6"
    data_ernings = requests.get(url_eps).json()
    url_dividends = f"https://www.alphavantage.co/query?function=DIVIDENDS&symbol={symbol}&apikey=AILA1I4F6KIGWUD6"
    data_dividends = requests.get(url_dividends).json()
    url_incomestatement = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey=AILA1I4F6KIGWUD6"
    data_incomestatement = requests.get(url_incomestatement).json()
    url_balancesheet = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey=AILA1I4F6KIGWUD6"
    data_balancesheet = requests.get(url_balancesheet).json()
    url_price = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=AILA1I4F6KIGWUD6"
    data_price = requests.get(url_price).json()

    # Parse the JSON data
    json_data_ernings = json.loads(data_ernings)
    json_data_dividends = json.loads(data_dividends)
    json_data_incomestatement = json.loads(data_incomestatement)
    json_data_balancesheet = json.loads(data_balancesheet)
    json_data_price = json.loads(data_price)

    json_data = [json_data_ernings, json_data_dividends, json_data_incomestatement, json_data_balancesheet, json_data_price]

    return json_data

def fundamentals(symbol, nb_shares, RealDiscountRate, AverageInflation, price_5_years_ago):
    #data = read_data(symbol)
    data = read_api(symbol)

    #Load JSON data
    json_data_ernings = data[0]
    json_data_dividends = data[1]
    json_data_incomestatement = data[2]
    json_data_balancesheet = data[3]
    json_data_price = data[4]

    # Extract EPS and year
    eps_data = []
    if 'annualEarnings' in json_data_ernings:
        for entry in json_data_ernings['annualEarnings']:
            year = entry['fiscalDateEnding'][:4]
            eps = entry['reportedEPS']
            eps_data.append({'year': year, 'eps': eps})

    # Extract Dividends and year
    dividends_data = []
    if 'data' in json_data_dividends:
        temp_data = {}
        for entry in json_data_dividends['data']:
            year = entry['ex_dividend_date'][:4]
            amount = float(entry['amount'])
            if year in temp_data:
                temp_data[year] += amount
            else:
                temp_data[year] = amount
        for year, amount in temp_data.items():
            dividends_data.append({'year': year, 'amount': amount})
    #print(dividends_data)

    #RORE 5 years
    if len(eps_data) >= 5 and len(dividends_data) >= 5:
        RORE_5years = (float(eps_data[0]['eps']) - float(eps_data[4]['eps'])) / (
            sum(float(eps_data[i]['eps']) for i in range(5)) -
            sum(float(dividends_data[i]['amount']) for i in range(5))
        ) * 100
    else:
        print("Not enough data to calculate RORE")

    #RORE 3 years
    if len(eps_data) >= 3 and len(dividends_data) >= 3:
        RORE_3years = (float(eps_data[0]['eps']) - float(eps_data[2]['eps'])) / (
            sum(float(eps_data[i]['eps']) for i in range(3)) -
            sum(float(dividends_data[i]['amount']) for i in range(3))
        ) * 100
    else:
        print("Not enough data to calculate RORE")

    #Extract Net Income data
    net_income_data = []
    if 'annualReports' in json_data_incomestatement:
        for report in json_data_incomestatement['annualReports']:
            year = report['fiscalDateEnding'][:4]
            net_income = report['netIncome']
            net_income_data.append({'year': year, 'netIncome': net_income})

    #NetIncomeGrouth_5years
    if len(net_income_data) >= 5:
        NetIncomeGrouth_5years = (float(net_income_data[0]['netIncome']) - float(net_income_data[4]['netIncome'])) / float(net_income_data[4]['netIncome']) * 100

    #CAGR 5 years
    cagr5years = (((float(net_income_data[0]['netIncome']) / float(net_income_data[4]['netIncome'])) ** (1 / 5)) - 1) * 100

    #NetIncomeGrouth_Average
    NetIncomeGrouth_Average = Average([(float(net_income_data[i]['netIncome']) - float(net_income_data[i + 1]['netIncome'])) / float(net_income_data[i + 1]['netIncome']) * 100 for i in range(4)])

    #EPSGrouth_5years
    EPSGrouth_5years = (float(eps_data[0]['eps']) - float(eps_data[4]['eps'])) / float(eps_data[4]['eps']) * 100

    #EPSGrouth_Average
    EPSGrouth_Average = Average([(float(eps_data[i]['eps']) - float(eps_data[i + 1]['eps'])) / float(eps_data[i + 1]['eps']) * 100 for i in range(4)])

    #PaidDividends_5years
    PaidDividends_5years = round(sum(float(dividends_data[i]['amount']) for i in range(5)), 2)

    #CurrentLiabilitiesToCash
    total_current_liabilities_data = []
    total_cash_and_cash_equivalents_data = []
    if 'annualReports' in json_data_balancesheet:
        for report in json_data_balancesheet['annualReports']:
            year = report['fiscalDateEnding'][:4]
            total_current_liabilities = report['totalCurrentLiabilities']
            total_cash_and_cash_equivalents = report['cashAndCashEquivalentsAtCarryingValue']
            total_current_liabilities_data.append({'year': year, 'totalCurrentLiabilities': total_current_liabilities})
            total_cash_and_cash_equivalents_data.append({'year': year, 'cashAndCashEquivalentsAtCarryingValue': total_cash_and_cash_equivalents})

    latest_total_current_liabilities = float(total_current_liabilities_data[0]['totalCurrentLiabilities'])
    latest_cash_and_cash_equivalents = float(total_cash_and_cash_equivalents_data[0]['cashAndCashEquivalentsAtCarryingValue'])
    current_liabilities_to_cash_factor = (latest_total_current_liabilities / latest_cash_and_cash_equivalents)*100

    #TotalLiabilitiestoAssets
    total_liabilities_data = []
    total_assets_data = []
    if 'annualReports' in json_data_balancesheet:
        for report in json_data_balancesheet['annualReports']:
            year = report['fiscalDateEnding'][:4]
            total_liabilities = report['totalLiabilities']
            total_assets = report['totalAssets']
            total_liabilities_data.append({'year': year, 'totalLiabilities': total_liabilities})
            total_assets_data.append({'year': year, 'totalAssets': total_assets})

    latest_total_liabilities = float(total_liabilities_data[0]['totalLiabilities'])
    latest_total_assets = float(total_assets_data[0]['totalAssets'])
    total_liabilities_to_assets_factor = (latest_total_liabilities / latest_total_assets)*100

    #PE
    #Extract Price data
    time_series_data = json_data_price['Time Series (Daily)']
    price_data = [{"date": dt.datetime.strptime(date, "%Y-%m-%d"), "close": float(details["4. close"])} for date, details in time_series_data.items()]
    price_data.sort(key=lambda x: x["date"])

    #Calculate PE ratio
    latest_eps = float(eps_data[0]['eps'])
    latest_price = price_data[0]['close']
    pe_ratio = latest_price / latest_eps

    #OVERPRICED
    investment = nb_shares * price_5_years_ago
    RetainedErnings = []
    for i in range(0, 4):
        retained_earnings = nb_shares * (float(eps_data[0]['eps']) - float(dividends_data[i]['amount']))
        RetainedErnings.append(f"{round(float(retained_earnings), 2):.2f}")
    RetainedErnings = [float(i) for i in RetainedErnings]
    NominalDiscountRate = RealDiscountRate + AverageInflation
    NetPresentValue = npf.npv(NominalDiscountRate, RetainedErnings)
    # EstimatedPrice
    TotalValueYears = "%.2f" % round(npf.fv(-AverageInflation, 5, 0, -NetPresentValue) + npf.fv(-AverageInflation, 5, 0,-(investment)), 2)
    EstimatedPrice = "%.2f" % round((float(TotalValueYears) / float(nb_shares)), 2)
    Overpriced = "%.2f" % round(100 * (latest_price / float(EstimatedPrice) - 1), 2)

    return pe_ratio, RORE_5years, RORE_3years, cagr5years, NetIncomeGrouth_5years, NetIncomeGrouth_Average, EPSGrouth_5years, EPSGrouth_Average, current_liabilities_to_cash_factor, total_liabilities_to_assets_factor, PaidDividends_5years, Overpriced
#print(fundamentals("IBM", 100, 0.05, 0.02, 137.29))

app = Flask(__name__)

@app.route('/')
def student():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        nb_shares = int(request.form['Number_Shares'])
        RealDiscountRate = float(request.form['RealDiscountRate'])
        AverageInflation = float(request.form['AverageInflation'])  
        t = [['Stock', 'P/E', 'RORE 5 years', 'RORE 3 years', 'CAGR 5 Years', 'Net Income Growth 5 years', 'Net Income Growth Average', 'EPS Growth 5 years', 'EPS Growth Average', 'Current Liabilities/Cash factor', 'Total Liabilities/Assets factor', 'Total paid dividends', 'Overpriced']]
        now = dt.datetime.now()
        graphdata = [['Year']] + [[now.year-i] for i in range(6)]

        for i in range(6):
            if request.form[f'Stock_symbol{i+1}'] != '':
                r = fundamentals(str(request.form[f'Stock_symbol{i+1}']), nb_shares, RealDiscountRate, AverageInflation, float(request.form[f'price_5_years_ago{i+1}']))
                stockname = request.form[f'Stock_symbol{i+1}']
                pe_ratio = '{:.2f}'.format(r[0])
                RORE_5years = '{:.2f}%'.format(r[1])
                RORE_3years = '{:.2f}%'.format(r[2])
                cagr5years = '{:.2f}%'.format(r[3])
                NetIncomeGrouth_5years = '{:.2f}%'.format(r[4])
                NetIncomeGrouth_Average = '{:.2f}%'.format(r[5])
                EPSGrouth_5years = '{:.2f}%'.format(r[6])
                EPSGrouth_Average = '{:.2f}%'.format(r[7])
                current_liabilities_to_cash_factor = '{:.2f}%'.format(r[8])
                total_liabilities_to_assets_factor = '{:.2f}%'.format(r[9])
                PaidDividends_5years = '{}'.format(r[10])
                Overpriced = '{}%'.format(r[11])

                table_data = [stockname, pe_ratio, RORE_5years, RORE_3years, cagr5years, NetIncomeGrouth_5years, NetIncomeGrouth_Average, EPSGrouth_5years, EPSGrouth_Average, current_liabilities_to_cash_factor, total_liabilities_to_assets_factor, PaidDividends_5years, Overpriced]
                t.append(table_data)
                
                if Overpriced != 0:
                    graphdata[0].append(stockname)
                    for i in range(6):
                        try:
                            graphdata[i+1].append(Overpriced)
                        except:
                            graphdata[i+1].append(0)

                graphdata = [['Year']] + [[now.year-i] for i in range(6)]

        print("graph data", graphdata)
        
        #format table data
        t = [x for x in t if str(x) != 'nan']
        columnNames = t[0]
        rows = t[1:]

        return render_template("result2.html", columnNames=columnNames, rows=rows, graphdata=graphdata)
    
if __name__ == '__main__':
    app.run(debug=True)


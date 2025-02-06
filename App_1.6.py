
import requests
from flask import Flask, render_template, request # type: ignore
from Fundamentals import fundamentals
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re

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
        now = datetime.datetime.now()
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

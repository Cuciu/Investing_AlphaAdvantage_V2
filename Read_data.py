import json

#symbol = 'IBM'

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

    url_eps = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey="[your API key]""
    data_ernings = requests.get(url_eps).json()
    url_dividends = f"https://www.alphavantage.co/query?function=DIVIDENDS&symbol={symbol}&apikey="[your API key]""
    data_dividends = requests.get(url_dividends).json()
    url_incomestatement = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey="[your API key]""
    data_incomestatement = requests.get(url_incomestatement).json()
    url_balancesheet = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey="[your API key]""
    data_balancesheet = requests.get(url_balancesheet).json()
    url_price = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey="[your API key]""
    data_price = requests.get(url_price).json()

    # Parse the JSON data
    json_data_ernings = json.loads(data_ernings)
    json_data_dividends = json.loads(data_dividends)
    json_data_incomestatement = json.loads(data_incomestatement)
    json_data_balancesheet = json.loads(data_balancesheet)
    json_data_price = json.loads(data_price)

    json_data = [json_data_ernings, json_data_dividends, json_data_incomestatement, json_data_balancesheet, json_data_price]

    return json_data

#print(read_data("IBM"))

import requests
import csv


class APIClient:
    def __init__(self, apikey='Y0L31DS6L0B9UL0B'):
        self.apikey = apikey
        self.urlbase = 'https://www.alphavantage.co/query?'

    def get(self, function, params: dict = None):
        url = self.urlbase + f'function={function}'
        if params:
            for key, value in params.items():
                url += f'&{key}={value}'
        url += f'&apikey={self.apikey}'
        return requests.get(url)

    def overview(self, symbol):
        params = {
            'symbol': symbol
        }
        ret = self.get('OVERVIEW', params)
        return ret.json()

    def dividends(self, symbol):
        params = {
            'symbol': symbol
        }
        ret = self.get('DIVIDENDS', params)
        return ret.json()

    def splits(self, symbol):
        params = {
            'symbol': symbol
        }
        ret = self.get('SPLITS', params)
        return ret.json()

    def income_statement(self, symbol):
        params = {
            'symbol': symbol
        }
        ret = self.get('INCOME_STATEMENT', params)
        return ret.json()

    def balance_sheet(self, symbol):
        params = {
            'symbol': symbol
        }
        ret = self.get('BALANCE_SHEET', params)
        return ret.json()

    def cash_flow(self, symbol):
        params = {
            'symbol': symbol
        }
        ret = self.get('CASH_FLOW', params)
        return ret.json()

    def active_stock_list(self):
        download = self.get('LISTING_STATUS')
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        stock_list_csv = list(cr)
        return stock_list_csv

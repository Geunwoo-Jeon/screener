import requests


class APIClient:
    def __init__(self, apikey='Y0L31DS6L0B9UL0B'):
        self.apikey = apikey
        self.urlbase = 'https://www.alphavantage.co/query?'

    def call(self, function, params):
        url = self.urlbase + f'function={function}'
        for key, value in params.items():
            url += f'&{key}={value}'
        url += f'&apikey={self.apikey}'
        ret = requests.get(url)
        data = ret.json()
        return data

    def income_statement(self, symbol='IBM'):
        params = {
            'symbol': symbol
        }
        return self.call('INCOME_STATEMENT', params)

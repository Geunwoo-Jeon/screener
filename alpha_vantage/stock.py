from api_client import APIClient
import ipdb


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol

        self.api_client = APIClient()
        self.overview = self.api_client.overview(
            self.symbol
        )

    def get_fundamentals(self):
        self.dividends = self.api_client.overview(
            self.symbol
        )
        self.income_statement = self.api_client.income_statement(
            self.symbol
        )
        self.balance_sheet = self.api_client.balance_sheet(
            self.symbol
        )
        self.cash_flow = self.api_client.cash_flow(
            self.symbol
        )

    def is_usa_stock(self):
        return self.overview['Country'] == 'USA'

    def is_older_5y(self):
        oldest_fisical_date = self.income_statement[
            'annualReports'][-1]['fiscalDateEnding']
        oldest_fisical_year = oldest_fisical_date.split('-')[0]
        oldest_fisical_year = int(oldest_fisical_year)
        return oldest_fisical_year <= 2019

    def is_surplus_5y(self):
        for quarter_IS in self.income_statement['quarterlyReports'][:20]:
            quarter_net_income = int(quarter_IS['netIncome'])
            if quarter_net_income < 0:
                return False
        return True

    def get_FCF(self, cash_flow):
        OCF = int(cash_flow['operatingCashflow'])
        capitalExpenditures = int(cash_flow['capitalExpenditures'])
        change_in_net_working_capital = int(cash_flow['changeInOperatingAssets']) - \
            int(cash_flow['changeInOperatingLiabilities'])
        FCF = OCF - capitalExpenditures + change_in_net_working_capital
        return FCF

    def has_trustable_income_5y(self):
        ann_CF_5y = self.cash_flow['annualReports'][:5]
        occr_list, fccr_list = [], []
        for i in range(4):
            net_income_sum_2y = int(ann_CF_5y[i]['netIncome']) + \
                int(ann_CF_5y[i+1]['netIncome'])
            OCF_sum_2y = int(ann_CF_5y[i]['operatingCashflow']) + \
                int(ann_CF_5y[i+1]['operatingCashflow'])
            FCF_sum_2y = self.get_FCF(
                ann_CF_5y[i]) + self.get_FCF(ann_CF_5y[i+1])

            if net_income_sum_2y < 0:
                return False
            if OCF_sum_2y < 0:
                return False
            if FCF_sum_2y < 0:
                return False
            occr = OCF_sum_2y / net_income_sum_2y
            fccr = FCF_sum_2y / net_income_sum_2y
            occr_list.append(occr)
            fccr_list.append(fccr)
            if occr < 1:
                return False
            if fccr < 0.8:
                return False
        print('Operating Cashflow Conversion Rate: ', occr_list)
        print('Free Cashflow Conversion Rate: ', fccr_list)
        return True

    def has_sufficient_cash(self):
        cur_balance_sheet = stock.balance_sheet['quarterlyReports'][0]
        total_assets = int(cur_balance_sheet['totalAssets'])
        cash = int(cur_balance_sheet['cashAndShortTermInvestments'])
        if total_assets < 0 or cash < 0:
            return False
        print('cash asset ratio: ', cash / total_assets)
        return cash / total_assets > 0.1

    def is_financially_healthy(self):
        cur_balance = stock.balance_sheet['quarterlyReports'][0]
        if int(cur_balance['totalShareholderEquity']) < 0:
            return False
        debt_ratio = int(cur_balance['totalLiabilities']) / \
            int(cur_balance['totalShareholderEquity'])
        print('debt_ratio = ', debt_ratio)
        return debt_ratio < 0.5

    def is_candidate(self):
        if not self.is_usa_stock():
            return 'no USA'
        self.get_fundamentals()
        if not self.is_older_5y():
            return 'no 5y'
        if not self.has_trustable_income_5y():
            return 'no trustable income'
        if not self.has_sufficient_cash():
            return 'no sufficient cash'
        if not self.is_financially_healthy():
            return 'no financially healthy'
        return 'yes'

    def get_weighted_avg_eps(self):
        stock_shares = int(
            self.balance_sheet['quarterlyReports'][0]['commonStockSharesOutstanding'])
        weighted_sum_eps = 0
        sum_weights = 0
        for i in range(12):
            earning = int(
                self.income_statement['quarterlyReports'][i]['netIncome'])
            eps = earning / stock_shares
            weighted_sum_eps += eps * (12-i)
            sum_weights += 12-i
        weighted_avg_eps = weighted_sum_eps / sum_weights
        print('Weighted Average EPS: ', weighted_avg_eps)
        return weighted_avg_eps

    def get_bps(self):
        cur_balance = self.balance_sheet['quarterlyReports'][0]
        equity = int(cur_balance['totalShareholderEquity'])
        stock_shares = int(cur_balance['commonStockSharesOutstanding'])
        bps = equity / stock_shares
        print('BPS: ', bps)
        return bps

    def get_intrinsic_value(self):
        weighted_eps = self.get_weighted_avg_eps()
        bps = self.get_bps()
        intrinsic_value = 1/2*(bps + weighted_eps * 10)
        return intrinsic_value


stock = Stock('AAPL')
ipdb.set_trace()

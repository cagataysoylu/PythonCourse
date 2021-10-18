import random

# Portfolio class inherits object


class Portfolio(object):
    def __init__(self):
        self.cash = 0.0
        self.transaction_history = ""
        self.stocks_balance = {}
        self.mutual_fonds_balance = {}

    def addCash(self, cash):
        self.cash += cash
        self.transaction_history += "$%f Cash added to portfolio.\n" % (cash)

    def withdrawCash(self, cash):
        if self.cash < cash:
            print("Can not withdraw.")
            self.transaction_history += "$%f withdrawal failed because balance is %f\n" % (
                cash, self.cash)
            return
        self.cash -= cash
        self.transaction_history += "$%f withdrawal succeeded. Now balance is %f\n" % (
            cash, self.cash)

    def buyStock(self, shares, stock):
        if self.cash < stock.price * shares:
            self.transaction_history += "Failed to buy %f shares of %s stocks. Required balance is %f, you have %f.\n" % (
                shares, stock.ticker, stock.price * shares, self.cash)
            return

        self.cash -= shares * stock.price
        self.transaction_history += "Bought %f shares of %s stocks. Now balance is %f.\n" % (
            shares, stock.ticker, self.cash)
        if not stock.ticker in self.stocks_balance:  # Initial buy of the stock
            self.stocks_balance[stock.ticker] = {
                'share': shares,
                'stock': stock  # For holding price
            }
        else:  # Already bought the stock, now we should increase amound of shares
            self.stocks_balance[stock.ticker] = {
                'share': self.stocks_balance[stock.ticker]['share'] + shares,
                'stock': stock
            }

    def buyMutualFund(self, shares, mf):
        if self.cash < shares:
            self.transaction_history += "Failed to buy %f shares of %s mutual fund. Required balance is %f, you have %f.\n" % (
                shares, mf.ticker, shares, self.cash)
            return

        self.cash -= shares
        self.transaction_history += "Bought %f shares of %s mutual fund. Now balance is %f.\n" % (
            shares, mf.ticker, self.cash)
        if not mf.ticker in self.mutual_fonds_balance:  # Initial buy of the fund
            self.mutual_fonds_balance[mf.ticker] = {
                'share': shares,
                'mutual_fund': mf  # For holding price
            }
        else:  # Already bought the fund, now we should increase amound of shares
            self.mutual_fonds_balance[mf.ticker] = {
                'share': self.mutual_fonds_balance[mf.ticker]['share'] + shares,
                'mutual_fund': mf  # For holding price
            }
        pass

    def __str__(self):

        stocks_summary = ""
        for stock_balance in self.stocks_balance:
            shares = self.stocks_balance[stock_balance]['share']
            if shares > 0:
                stocks_summary += "%s: %d\n" % (stock_balance, shares)

        fund_summary = ""
        for fund_balance in self.mutual_fonds_balance:
            shares = self.mutual_fonds_balance[fund_balance]['share']
            if shares > 0:
                fund_summary += "%s: %d\n" % (fund_balance, shares)

        return "Balance: %f\nStocks:\n%s \nMutual Funds:\n%s" % (
            self.cash, stocks_summary, fund_summary)

    def sellMutualFund(self, ticker, shares):
        if ticker in self.mutual_fonds_balance:
            if self.mutual_fonds_balance[ticker]['share'] < shares:
                self.transaction_history += "Failed to sell %d shares of %s mutual fund. You have %d.\n" % (
                    shares, ticker, self.mutual_fonds_balance[ticker]['share'])
                return
            else:
                self.mutual_fonds_balance[ticker]['share'] -= shares
                self.addCash(shares)
                self.transaction_history += "Succeed to sell %d shares from %s\n" % (
                    shares, ticker)
        else:
            self.transaction_history += "Failed to sell %d shares of %s mutual fund. You do not have any.\n" % (
                shares, ticker)
            return

    def sellStock(self, ticker, shares):
        if ticker in self.stocks_balance:
            if self.stocks_balance[ticker]['share'] < shares:
                self.transaction_history += "Failed to sell %d shares of %s stocks. You have %d.\n" % (
                    shares, ticker, self.stocks_balance[ticker]['share'])
                return
            else:
                self.stocks_balance[ticker]['share'] -= shares
                self.addCash(
                    shares * self.stocks_balance[ticker]['stock'].generateSellPrice())
                self.transaction_history += "Succeed to sell %d shares from %s\n" % (
                    shares, ticker)
        else:
            self.transaction_history += "Failed to sell %d shares of %s stocks. You do not have any.\n" % (
                shares, ticker)
            return
        pass

    def history(self):
        print(self.transaction_history)


class Stock(object):
    def __init__(self, price, ticker):
        self.price = price
        self.ticker = ticker

    def generateSellPrice(self):
        return random.uniform(0.5 * self.price, 1.5 * self.price)


class MutualFund(object):
    def __init__(self, ticker):
        self.ticker = ticker

    def generateSellPrice(self):
        return random.uniform(0.9, 1.2)


if __name__ == '__main__':
    portfolio = Portfolio()
    portfolio.addCash(300.50)
    s = Stock(20, "HFH")
    portfolio.buyStock(5, s)
    mf1 = MutualFund("BRT")
    mf2 = MutualFund("GHT")
    portfolio.buyMutualFund(10.3, mf1)
    portfolio.buyMutualFund(2, mf2)
    print(portfolio)

    portfolio.sellMutualFund("BRT", 3)
    portfolio.sellStock("HFH", 1)

    portfolio.history()

# region imports
from AlgorithmImports import *
# endregion

class HipsterYellowBuffalo(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2002, 5, 6)
        self.SetEndDate(2024, 2, 10)
        self.SetAccountCurrency("GBP")
        self.SetCash(1500)

        self.a = ["SPY", "NDX", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "JNJ", "JPM", "WMT", "PG", "V", "NVDA", "AMD", "SANA", "SHOP", "AMC", "UBER", "COIN", "BRK.A", "MA", "XOM", "HD", "COST", "ORCL", "CVX", "MCD", "CRM", "PEP", "KO", "BAC", "ADBE", "VZ", "CMCSA", "TMUS", "ABT", "CSCO", "INTC", "NFLX", "QCOM", "NKE", "DIS", "PFE", "IBM", "VIX", "DXY", "BTCUSD", "BTCUSDT", "ETHUSD", "USOIL", "GOLD", "SILVER", "EURUSD", "BAC", "DTE", "LHA", "O2D", "MBG", "ALV", "BMW", "VOW", "SHEL", "HSBA", "BP.", "BARC", "VOD", "PDG", "SSE-600519", "SSE-601398", "SSE-600941", "SSE-601857", "SSE-601288", "SSE-601988", "SSE-601939", "SSE-600036", "DOGE/GBP", "ADA/GBP", "XRP/GBP", "LTC/GBP", "SMI", "SIW00", "PLW00", "PAW00", "ALIW00"]
        self.stock = []
        self.stockSma = []
        self.stockRsi = []
        self.trailingStopLoss = []

        for i in range(0, len(self.a)):
            self.stock.append(self.AddEquity(self.a[i], Resolution.Daily))
            self.stockSma.append(self.SMA(self.stock[i].Symbol, 200))
            self.stockRsi.append(self.RSI(self.stock[i].Symbol, 14))
            self.trailingStopLoss.append(0)

        #self.Schedule.On(self.DateRules.WeekEnd(), self.TimeRules.Noon, self.Salary)

        self.SetWarmup(250, Resolution.Daily)

    def OnData(self, data: Slice):
        if self.IsWarmingUp:
            return
        
        #if self.stock[0].Price > self.stockSma[0].Current.Value:
            #if self.stock[0].Price > self.stockSma[0].Current.Value + 25:
                #self.b = 6
            #elif self.stock[0].Price > self.stockSma[0].Current.Value + 50:
                #self.b = 7
            #elif self.stock[0].Price > self.stockSma[0].Current.Value + 75:
                #self.b = 8
            #elif self.stock[0].Price > self.stockSma[0].Current.Value + 100:
                #self.b = 9
            #else:
                #self.b = 10
        #else:
            #if self.stock[0].Price < self.stockSma[0].Current.Value + 25:
                #self.b = 5
            #elif self.stock[0].Price < self.stockSma[0].Current.Value + 50:
                #self.b = 4
            #elif self.stock[0].Price < self.stockSma[0].Current.Value + 75:
                #self.b = 3
            #elif self.stock[0].Price < self.stockSma[0].Current.Value + 100:
                #self.b = 2
            #else:
                #self.b = 1
        
        for i in range(0, len(self.a)):
            holding = self.Portfolio[self.stock[i].Symbol]
            tradable = self.Securities[self.stock[i].Symbol].IsTradable
            if not holding.Invested and tradable:
                self.trailingStopLoss[i] = 0
                if self.stock[i].Price > self.stockSma[i].Current.Value and self.Portfolio.Cash > (self.stock[i].Price * 5) and self.stockRsi[i].Current.Value > 10:
                    self.SetHoldings(self.stock[i].Symbol, 1/3)
                    self.trailingStopLoss[i] = self.stock[i].Price - 5
            if holding.Invested and tradable:
                if self.stock[i].Price > (self.trailingStopLoss[i] + 5):
                    self.trailingStopLoss[i] = self.stock[i].Price - 5
                if self.stock[i].Price <= self.trailingStopLoss[i]:
                    self.Liquidate(self.stock[i].Symbol)
            #self.Plot(self.a[i], "MA100", self.stockSma[i].Current.Value)
            #self.Plot(self.a[i], self.a[i], self.stock[i].Price)

    def Salary(self):
        self.Portfolio.CashBook["GBP"].AddAmount(450)

import enum
from enum import Enum
from datetime import datetime, timedelta
import abc
import operator
from functools import reduce

@enum.unique
class StockSymbol(Enum):
    """
    Unique identifier for one of th Stocks traded
    """
    TEA = 1
    POP = 2
    ALE = 3
    GIN = 4
    JOE = 5
    
@enum.unique
class SuperTrend(Enum):
    """
    Unique Indicator to buy or sell
    """
    BUY = 1
    SELL = 2


class Trade:
    """
    Transfer of shares buy/sell at the given time  
    """
    def __init__(self,
                 stock_symbol: StockSymbol,
                 timestamp: datetime,
                 quantity:int,
                 price_per_share: float,
                 super_trend: SuperTrend):
        """
        :param timestamp: The moment when the transaction has taken place
        :param quantity: The quantity of shares bought or sold  
        :param price_per_share: Price of each share
        :param super_trend: Signal to buy or sell share
        """
        
        self.stock_symbol = stock_symbol
        self.timestamp = timestamp
        
        self.quantity = quantity
        self.price_per_share = price_per_share
        self.super_trend = super_trend
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        """
        if the quantity of shares to buy/sell is less than zero raise error 
        else update the quantity
        """
        if quantity >= 0:
            self._quantity = quantity
        else:
            error_message = "The quantity of shares cannot be less than zero"
            raise ValueError(error_message)
            
    @property
    def price_per_share(self):
        return self._price_per_share
    
    @price_per_share.setter
    def price_per_share(self, price_per_share):
        """
        if the price of share is less than zero raise error
        else update the cost of each share
        """
        if price_per_share >= 0:
            self._price_per_share = price_per_share
        else:
            error_message = "The Price of shares cannot be less than zero"
            raise ValueError(error_message)
    
    @property 
    def total_price(self):
        """
        :return: The total price of the trade
        """
        return self.quantity * self.price_per_share

class Stock(abc.ABC):
    """
    Abstract class for common stocks share and preferred stocks share.
    """
    price_time_interval = timedelta(minutes=15)
    def __init__(self, 
                 stock_symbol:StockSymbol,
                 par_value:float):
        """
        :param stock_symbol: The stock_symbol that identifies this stock
        :param par_value: The value of the share for this stock
        """
        self.stock_symbol = stock_symbol
        self.par_value = par_value
        
        self.trades = []
        
    def record_trade(self, trade:Trade):
        """
        Records the trade for this stock
        :param trade to be recorded
        """
        
        if not isinstance(trade, Trade):
            error_message = "Given trade={trade} should be of type Trade.".format(trade=trade)
            raise TypeError(msg)
        elif self.stock_symbol is not trade.stock_symbol:
            error_message = " Given Trade does not belong to this stock."
            raise ValueError(error_message)
        else:
            self.trades.append(trade)
        
    @property
    @abc.abstractmethod
    def dividend(self):
        """
        :return: Dividend for the given stock
        """
        pass
    
    @property
    def price(self):
        """
        Returns the share pirce of the last recorded trade
        """
        if len(self.trades) > 0:
            by_timestamp = sorted(self.trades,
                                  key=lambda trade: trade.timestamp,
                                  reverse=True)
            return by_timestamp[0].price_per_share
        else:
            error_message = "The Price for the last trade is not available"
            raise AttributeError(error_message)
        
    @property
    def dividend_yield(self):
        """
        Returns the dividend yield
        """
        return self.dividend / self.price
    
    @property
    def price_earnings_ratio(self):
        """
        :return: The P/E ratio for this stock
        """
        if self.dividend != 0:
            return self.price / self.dividend
        else:
            return None
        
    def avg_price(self,
              current_time: datetime=datetime.now()):
        """
        :param current_time: The point of time defined as the current one.
        :return: The average price per share based on trades recorded in the last
            Stock.price_time_interval. None if there are 0 trades that satisfy this
            condition.
        """
        significant_trades = [trade for trade in self.trades
                              if trade.timestamp >= current_time - self.price_time_interval]

        if len(significant_trades) > 0:
            trade_prices = (trade.total_price for trade in significant_trades)
            quantities = (trade.quantity for trade in significant_trades)
            return sum(trade_prices) / sum(quantities)
        else:
            return None

class CommonStock(Stock):
    """
    Common Stocks
    """
    def __init__(self,
                 stock_symbol:StockSymbol,
                 par_value:float,
                 last_dividend:float):
    
        """
        :param last_dividend: An absolute value that indicates the last dividend
            per share for this stock.
        """

        super().__init__(stock_symbol, par_value)
        self.last_dividend = last_dividend

    @property
    def dividend(self):
        return self.last_dividend

class PreferredStock(Stock):
    
    """A preferred stock"""

    def __init__(self,
                 stock_symbol: StockSymbol,
                 par_value: float,
                 fixed_dividend: float,
                 last_dividend:float):
        """
        :param fixed_dividend: A decimal number that expresses the fixed dividend
            as a ratio of the face value of each share.
        """

        super().__init__(stock_symbol, par_value)
        self.fixed_dividend = fixed_dividend
        self.last_dividend = last_dividend

    @property
    def dividend(self):
        return self.fixed_dividend * self.par_value

    
class GlobalBeverageCorporationExchange():
    """
    Where the trade takes place
    """
    def __init__(self, stocks:[Stock]):
        """
        :param stocks: The total stocks traded 
        """
        self.stocks = stocks
        
    @property
    def stocks(self):
        return self._stocks
    
    @stocks.setter
    def stocks(self, stocks):
        if len(stocks) > 0:
            self._stocks = stocks
        else:
            error_message = "Stocks traded should be a non empty sequence."
            raise ValueError(error_message)
        
    def record_trade(self, trade:Trade):
        """
        Records the trade
        :param trade: The trade to be recorded.
        """
        stock.record_trade(trade)
    
    def all_share_index(self, current_time = datetime.now()):
        """
        Return the Geometric mean of all the stocks Prices. 
        Returns None if the none of the stock prices are present
        :param current_time: The point of time for which index has to be obtained
        """
        stock_prices = [stock.total_price for stock in self.stocks]
        
        if len(stock_prices) == 0:
            return None
        else:
            total_product = reduce(operator.mul, stock_prices, 1)
            return total_product**(1/len(stock_prices))
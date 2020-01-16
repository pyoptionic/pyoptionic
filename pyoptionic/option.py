import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style


# Class for a naked option
class Option(object):
    def __init__(self, option_type, premium, strike_price):
        option_types = ('call', 'put')
        if option_type not in option_types:
            raise('Option type can only be call or put')
        self.option_type = option_type
        self.premium = premium
        self.strike_price = strike_price
        # Breakeven Point (BEP)
        self.bep = strike_price + premium if option_type == 'call' else strike_price - premium
        # Plot settings
        self.x_extend = 100

    def in_val(self, stock_price):
        if self.option_type == 'call':
            if stock_price > self.strike_price:
                intrinsic_val = stock_price - self.strike_price
            else:
                intrinsic_val = 0
        elif self.option_type == 'put':
            if stock_price < self.strike_price:
                intrinsic_val = self.strke_price - stock_price
            else:
                intrinsic_val = 0

        return intrinsic_val

    def moneyness(self, stock_price):
        if self.option_type == 'call':
            if stock_price > self.strike_price:
                money = 'ITM'
            elif stock_price == self.strike_price:
                money = 'ATM'
            else:
                money = 'OTM'
        elif self.option_type == 'put':
            if stock_price < self.strike_price:
                money = 'ITM'
            elif stock_price == self.strike_price:
                money = 'ATM'
            else:
                money = 'OTM'

        return money

    def plot_pnl(self):
        # Plot settings
        style.use('ggplot')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.xlabel('Stock Price at Expiration')
        plt.ylabel('Profit or Loss')
        plt.xlim(-5, self.strike_price+self.x_extend)

        if self.option_type == 'call':
            intercept = -self.premium - self.strike_price
            x = np.linspace(self.strike_price, self.strike_price+self.x_extend)
            y = x + intercept

            plt.hlines(y=-self.premium, xmin=0, xmax=self.strike_price, color='r', linestyle='-')
            plt.vlines(x=self.strike_price, ymin=-self.premium, ymax=0, color='#1949cf', label='ATM', linestyle='--')
            plt.axvspan(0, self.strike_price, alpha=0.25, color='#d61e40', label='OTM')
            plt.axvspan(self.strike_price, self.strike_price+self.x_extend, alpha=0.25, color='#18c918', label='ITM')
            plt.title('Call Option Profit & Loss Diagram')
        elif self.option_type == 'put':
            intercept = -self.premium + self.strike_price
            x = np.linspace(0, self.strike_price)
            y = -x + intercept

            plt.hlines(y=-self.premium, xmin=self.strike_price, xmax=self.strike_price+self.x_extend , color='r', linestyle='-')
            plt.vlines(x=self.strike_price, ymin=-self.premium, ymax=0, color='#1949cf', label='ATM', linestyle='--')
            plt.axvspan(0, self.strike_price, alpha=0.25, color='#18c918', label='ITM')
            plt.axvspan(self.strike_price, self.strike_price+self.x_extend, alpha=0.25, color='#d61e40', label='OTM')
            plt.title('Put Option Profit & Loss Diagram')

        plt.plot(x, y, '-r')
        plt.legend()
        plt.show()

    def plot_inval(self):
        # Plot settings
        style.use('ggplot')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.xlabel('Stock Price at Expiration')
        plt.ylabel('Intrinsic Value of Option')
        plt.xlim(-5, self.strike_price+self.x_extend)

        if self.option_type == 'call':
            x = np.linspace(self.strike_price, self.strike_price+self.x_extend)
            y = x + -self.strike_price

            plt.hlines(y=0, xmin=0, xmax=self.strike_price, color='r', linestyle='-')
            plt.axvspan(0, self.strike_price, alpha=0.25, color='#d61e40', label='OTM')
            plt.axvspan(self.strike_price, self.strike_price+self.x_extend, alpha=0.25, color='#18c918', label='ITM')
            plt.title('Call Option Intrinsic Value Diagram')
        elif self.option_type == 'put':
            x = np.linspace(0, self.strike_price)
            y = -x + self.strike_price

            plt.hlines(y=-0, xmin=self.strike_price, xmax=self.strike_price+self.x_extend , color='r', linestyle='-')
            plt.axvspan(0, self.strike_price, alpha=0.25, color='#18c918', label='ITM')
            plt.axvspan(self.strike_price, self.strike_price+self.x_extend, alpha=0.25, color='#d61e40', label='OTM')
            plt.title('Put Option Intrinsic Value Diagram')

        plt.plot(x, y, '-r')
        plt.legend()
        plt.show()

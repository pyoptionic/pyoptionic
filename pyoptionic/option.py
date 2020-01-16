import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style


# Class for a naked option
class Option(object):
    def __init__(self, position, option_type, premium, strike_price):
        option_types = ('call', 'put')
        if option_type not in option_types:
            raise('Option type can only be call or put')
        if position not in ('long', 'short'):
            raise('Position is not specified')
        self.option_type = option_type
        self.premium = premium
        self.strike_price = strike_price
        self.position = position

    def __str__(self):
        return '{} {}'.format(self.position, self.option_type)

    def __repr__(self):
        return 'Option("{}", "{}", {}, {})'.format(
            self.position,
            self.option_type,
            self.premium,
            self.strike_price)

    # Breakeven Point (BEP)
    def bep(self):
        if self.option_type == 'call':
            breakeven = self.strike_price + self.premium
        elif self.option_type == 'put':
            breakeven = self.strike_price - self.premium

        return breakeven

    def max_gain(self):
        if self.position == 'long':
            gain = 'unlimited'
        elif self.position == 'short':
            gain = self.premium

        return gain

    def max_loss(self):
        if self.position == 'long':
            loss = self.premium
        elif self.position == 'short':
            loss = 'unlimited'

        return loss

    # Intrinsic Value
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

    # Time Value
    def time_val(self, stock_price):
        return self.premium - self.in_val(stock_price)

    # ITM, ATM or OTM
    def moneyness(self, stock_price):
        if stock_price == self.strike_price:
            money = 'ATM'
        # Long Call
        elif self.position == 'long' and self.option_type == 'call':
            if stock_price > self.strike_price:
                money = 'ITM'
            elif stock_price < self.strike_price:
                money = 'OTM'
        # Long Put
        elif self.position == 'long' and self.option_type == 'put':
            if stock_price < self.strike_price:
                money = 'ITM'
            elif stock_price > self.strike_price:
                money = 'OTM'
        # Short Call
        elif self.position == 'short' and self.option_type == 'call':
            if stock_price < self.strike_price:
                money = 'ITM'
            elif stock_price > self.strike_price:
                money = 'OTM'
        # Short Put
        elif self.position == 'short' and self.option_type == 'put':
            if stock_price > self.strike_price:
                money = 'ITM'
            elif stock_price < self.strike_price:
                money = 'OTM'

        return money

    # Y-intercept of Profit & Loss Diagram
    def intercept(self, position, option_type):
        premium = self.premium
        strike_price = self.strike_price

        if position == 'long' and option_type == 'call':
            c = -premium - strike_price
        elif position == 'short' and option_type == 'call':
            c = premium + strike_price
        elif position == 'long' and option_type == 'put':
            c = strike_price - premium
        elif position == 'short' and option_type == 'put':
            c = premium - strike_price

        return c

    def pnl(self, x):
        position = self.position
        option_type = self.option_type
        premium = self.premium
        strike_price = self.strike_price
        c = self.intercept(position, option_type)

        if position == 'long' and option_type == 'call':
            y = np.piecewise(
                x,
                [x <= strike_price, x > strike_price],
                [-premium, lambda x: x + c])
        elif position == 'short' and option_type == 'call':
            y = np.piecewise(
                x,
                [x <= strike_price, x > strike_price],
                [-premium, lambda x: x + c])
        elif position == 'long' and option_type == 'put':
            y = np.piecewise(
                x,
                [x <= strike_price, x > strike_price],
                [-premium, lambda x: x + c])
        elif position == 'short' and option_type == 'put':
            y = np.piecewise(
                x,
                [x <= strike_price, x > strike_price],
                [-premium, lambda x: x + c])

        return y

    # Plot Profit & Loss Diagram
    def plot_pnl(self, x_extend=100):
        # Plot settings
        style.use('ggplot')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.xlabel('Stock Price at Expiration')
        plt.ylabel('Profit or Loss')
        plt.xlim(-5, self.strike_price+x_extend)

        c = self.intercept(self.position, self.option_type)

        # Long Call
        if self.position == 'long' and self.option_type == 'call':
            x = np.linspace(self.strike_price, self.strike_price+x_extend)
            y = x + c

            plt.hlines(
                y=-self.premium,
                xmin=0,
                xmax=self.strike_price,
                color='r',
                linestyle='-')
            plt.vlines(
                x=self.strike_price,
                ymin=-self.premium,
                ymax=0,
                color='#1949cf',
                label='ATM',
                linestyle='--')

            plt.axvspan(
                0,
                self.strike_price,
                alpha=0.25,
                color='#d61e40',
                label='OTM')
            plt.axvspan(
                self.strike_price,
                self.strike_price+x_extend,
                alpha=0.25,
                color='#18c918',
                label='ITM')

            plt.title('Long Call Profit & Loss Diagram')
        # Short Call
        elif self.position == 'short' and self.option_type == 'call':
            x = np.linspace(self.strike_price, self.strike_price+x_extend)
            y = -x + c

            plt.hlines(
                y=self.premium,
                xmin=0,
                xmax=self.strike_price,
                color='r',
                linestyle='-')
            plt.vlines(
                x=self.strike_price,
                ymin=0,
                ymax=self.premium,
                color='#1949cf',
                label='ATM',
                linestyle='--')

            plt.axvspan(
                0,
                self.strike_price,
                alpha=0.25,
                color='#18c918',
                label='ITM')
            plt.axvspan(
                self.strike_price,
                self.strike_price+x_extend,
                alpha=0.25,
                color='#d61e40',
                label='OTM')

            plt.title('Short Call Profit & Loss Diagram')
        # Long Put
        elif self.position == 'long' and self.option_type == 'put':
            x = np.linspace(0, self.strike_price)
            y = -x + c

            plt.hlines(
                y=-self.premium,
                xmin=self.strike_price,
                xmax=self.strike_price+x_extend,
                color='r',
                linestyle='-')
            plt.vlines(
                x=self.strike_price,
                ymin=-self.premium,
                ymax=0,
                color='#1949cf',
                label='ATM',
                linestyle='--')

            plt.axvspan(
                0,
                self.strike_price,
                alpha=0.25,
                color='#18c918',
                label='ITM')
            plt.axvspan(
                self.strike_price,
                self.strike_price+x_extend,
                alpha=0.25,
                color='#d61e40',
                label='OTM')
            plt.title('Long Put Profit & Loss Diagram')
        # Short Put
        elif self.position == 'short' and self.option_type == 'put':
            x = np.linspace(0, self.strike_price)
            y = x + c

            plt.hlines(
                y=self.premium,
                xmin=self.strike_price,
                xmax=self.strike_price+x_extend,
                color='r',
                linestyle='-')
            plt.vlines(
                x=self.strike_price,
                ymin=0,
                ymax=self.premium,
                color='#1949cf',
                label='ATM',
                linestyle='--')

            plt.axvspan(
                0,
                self.strike_price,
                alpha=0.25,
                color='#d61e40',
                label='OTM')
            plt.axvspan(
                self.strike_price,
                self.strike_price+x_extend,
                alpha=0.25,
                color='#18c918',
                label='ITM')
            plt.title('Short Put Profit & Loss Diagram')

        plt.plot(x, y, '-r')
        plt.legend()
        plt.show()

    def plot_inval(self, x_extend=100):
        # Plot settings
        style.use('ggplot')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.xlabel('Stock Price at Expiration')
        plt.ylabel('Intrinsic Value of Option')
        plt.xlim(-5, self.strike_price+x_extend)

        if self.option_type == 'call':
            x = np.linspace(self.strike_price, self.strike_price+x_extend)
            y = x + -self.strike_price

            plt.hlines(
                y=0,
                xmin=0,
                xmax=self.strike_price,
                color='r',
                linestyle='-')
            plt.axvspan(
                0,
                self.strike_price,
                alpha=0.25,
                color='#d61e40',
                label='OTM')
            plt.axvspan(
                self.strike_price,
                self.strike_price+x_extend,
                alpha=0.25,
                color='#18c918',
                label='ITM')
            plt.title('Call Option Intrinsic Value Diagram')
        elif self.option_type == 'put':
            x = np.linspace(0, self.strike_price)
            y = -x + self.strike_price

            plt.hlines(
                y=-0,
                xmin=self.strike_price,
                xmax=self.strike_price+x_extend,
                color='r',
                linestyle='-')
            plt.axvspan(
                0,
                self.strike_price,
                alpha=0.25,
                color='#18c918',
                label='ITM')
            plt.axvspan(
                self.strike_price,
                self.strike_price+x_extend,
                alpha=0.25,
                color='#d61e40',
                label='OTM')
            plt.title('Put Option Intrinsic Value Diagram')

        plt.plot(x, y, '-r')
        plt.legend()
        plt.show()

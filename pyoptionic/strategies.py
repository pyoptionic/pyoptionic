import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np


class LongStradle(object):
    def __init__(self, long_call, long_put):
        if long_call.strike_price != long_put.strike_price:
            raise('Strike prices must be equivalent')
        self.long_call = long_call
        self.long_put = long_put
        self.strike_price = long_call.strike_price
        self.premium = long_call.premium + long_put.premium

    def __str__(self):
        return 'Long Stradle'

    def __repr__(self):
        return 'LongStradle({}, {})'.format(self.long_call, self.long_put)

    def bep(self):
        pass

    def in_val(self, stock_price):
        if stock_price < self.strike_price:
            intrinsic_val = self.strike_price - stock_price
        elif stock_price == self.strike_price:
            intrinsic_val = 0
        else:
            intrinsic_val = stock_price - self.strike_price

        return intrinsic_val

    def moneyness(self, stock_price):
        if stock_price < self.strike_price:
            money = 'ITM'
        elif stock_price == self.strike_price:
            money = 'ATM'
        elif stock_price > self.strike_price:
            money = 'ITM'

        return money

    def plot_pnl(self, x_extend=100):
        pass

    def plot_inval(self, x_extend=100):
        # Plot settings
        style.use('ggplot')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.xlabel('Stock Price at Expiration')
        plt.ylabel('Intrinsic Value of Long Straddle')
        plt.xlim(-5, self.strike_price+x_extend)

        x_put = np.linspace(0, self.strike_price)
        x_call = np.linspace(self.strike_price, self.strike_price+x_extend)

        y_put = -x_put + self.strike_price
        y_call = x_call - self.strike_price

        plt.plot(x_put, y_put, '-r')
        plt.plot(x_call, y_call, 'r')
        plt.legend()
        plt.show()


class BullCallSpread(object):
    def __init__(self, long_call, short_call):
        if short_call.strike_price <= long_call.strike_price:
            raise('Short call strike price must be '
                  'higher than long call strike price')
        self.long_call = long_call
        self.short_call = short_call

    def __str__(self):
        return 'Bull Call Spread'

    def __repr__(self):
        return 'BullCallSpread({}, {})'.format(self.long_call, self.short_call)

    def spread_width(self):
        return self.short_call.strike_price - self.long_call.strike_price

    def net_debit(self):
        return self.long_call.premium - self.short_call.premium

    def max_loss(self):
        return self.debit() * 100

    def max_profit(self):
        return (self.spread_width() - self.net_debit()) * 100

    def bep(self):
        return self.long_call.strike_price + self.net_debit()

    def in_val(self):
        pass

    def moneyness(self):
        pass


class BullPutSpread(object):
    def __init__(self, long_put, short_put):
        if long_put.strike_price >= short_put.strike_price:
            raise('Long put strike price must be '
                  'lower than short put strike price')
        self.long_put = long_put
        self.short_put = short_put

    def __str__(self):
        return 'Bull Put Spread'

    def __repr__(self):
        return 'BullPutSpread({}, {})'.format(self.long_put, self.short_put)

    def spread_width(self):
        return self.short_put.strike_price - self.long_put.strike_price

    def net_credit(self):
        return self.short_put.premium - self.long_put.premium

    def bep(self):
        return self.short_put.strike_price - self.net_credit()

    def max_loss(self):
        return (self.spread_width() - self.net_credit()) * 100

    def max_profit(self):
        return self.net_credit() * 100

    def in_val(self):
        pass

    def moneyness(self):
        pass


class BearCallSpread(object):
    def __init__(self, long_call, short_call):
        if long_call.strike_price <= short_call.strike_price:
            raise('Long call strike price must be '
                  'higher than short call strike price')
        long_call = self.long_call
        short_call = self.short_call

    def __str__(self):
        return 'Bear Call Spread'

    def __repr__(self):
        return 'BearCallSpread({}, {})'.format(self.long_call, self.short_call)

    def spread_width(self):
        return self.long_call.strike_price - self.short_call.strike_price

    def net_credit(self):
        return self.short_call.premium - self.long_call.premium

    def bep(self):
        return self.short_call.strike_price + self.net_credit()

    def max_loss(self):
        return (self.spread_width() - self.net_credit()) * 100

    def max_gain(self):
        return self.net_credit() * 100

    def in_val(self):
        pass

    def moneyness(self):
        pass


class BearPutSpread(object):
    def __init__(self, long_put, short_put):
        if long_put.strike_price <= short_put.strike_price:
            raise('Long put strike price must be '
                  'higher than short put strike price')
        self.long_put = long_put
        self.short_put = short_put

    def __str__(self):
        return 'Bear Put Spread'

    def __repr__(self):
        return 'BearPutSpread({}, {})'.format(self.long_put, self.short_put)

    def spread_width(self):
        return self.long_put.strike_price - self.short_put.strike_price

    def net_debit(self):
        return self.long_put.premium - self.short_put.premium

    def bep(self):
        return self.long_put.strike_price - self.net_debit()

    def max_loss(self):
        return self.net_debit() * 100

    def max_gain(self):
        return (self.spread_width() - self.net_debit()) * 100

    def in_val(self):
        pass

    def moneyness(self):
        pass


class IronCondor(object):
    def __init__(self, long_call, long_put, short_call, short_put):
        self.long_call = long_call
        self.long_put = long_put
        self.short_call = short_call
        self.short_put = short_put

    def __str__(self):
        return 'Iron Condor'

    def __repr__(self):
        return 'IronCondor({}, {}, {}, {})'.format(
            self.long_call, self.long_put, self.short_call, self.short_put)

    def in_val(self):
        pass

    def moneyness(self):
        pass


class IronButterfly(object):
    def __init__(self):
        pass

    def __str__(self):
        return 'Iron Butterfly'

    def __repr__(self):
        return 'IronButterfly()'.format()

    def in_val(self):
        pass

    def moneyness(self):
        pass

import yahoo_finance
import json
import os
import click

stocks = ['MSFT', 'AMZN', 'GOOG']


def stock_util(stocks):
    '''
    attempt = open_shares()
    if attempt:
        shares = attempt
    else:
        shares = get_shares(stocks)
    '''
    shares = get_shares(stocks)
    #write_shares(shares)
    print_shares(shares)


def get_shares(stocks):
    shares = {}
    for stock in stocks:
        key = ((yahoo_finance.Share(stock)).get_name())
        val = (yahoo_finance.Share(stock))
        # print(key)  # debug
        # print(val)  # debug
        shares.update({key: val})
    #print(type(shares))  # debug
    return shares


def print_shares(shares):
    for key, val in shares.items():
        price = val.get_price()
        change = val.get_change()
        percent = float(change)/float(price)
        print('{} - Price: {}'.format(key, price))

        print('Change: {} - {}%'.format(change, round(percent, 2)))


def write_shares(shares):
    with open('shares.txt', 'w') as handle:
        json.dump(shares, handle)


def open_shares():
    if os.path.isfile('shares.txt'):
        with open('shares.txt', 'r') as handle:
            return json.load(handle)
    else:
        return None

stock_util(stocks)
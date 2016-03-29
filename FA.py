import csv
import urllib.request
from lxml import etree
from yahoo_finance import *
from bs4 import BeautifulSoup
import datetime
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib

def get_company_info(c):
    if c == None:
        return None
    
    d = datetime.datetime.now().date()

    comp = Share(c)
    soup = BeautifulSoup(urllib.request.urlopen('http://finance.yahoo.com/q?s='+c).read(), 'lxml')
    if comp == None:
        return None
    
    return dict(list({'history': list(reversed(list(map(lambda x: x['High'],
                                                        comp.get_historical(str(d - datetime.timedelta(days=300)), str(d))))))}.items()) + \
                list({tr.th.text: tr.td.text
                    for tr in list(soup.find("table", {"id":"table1"}).children)}.items()) +\
                list({'Name': c}.items())+\
                list({'Current':comp.get_price()}.items()))

def training_info(x):
    return (list(reversed(list(map(eval, get_company_info(x)['history'])))),
            eval(get_company_info(x)['Current']))
try:
    print("Trying to load AI.")
    ai = joblib.load('expert.pkl')
except FileNotFoundError:
    print("AI not found, training a new one....")
    ai = LinearRegression()
    histories = [
        training_info('GOOG'),
        training_info('AAPL'),
        training_info('CSCO'),
        training_info('LNKD'),
        training_info('FB'),
        training_info('TWTR'),
        training_info('AMZN'),
        training_info('NFLX'),
        training_info('MSFT'),
        training_info('YHOO'),
        training_info('VZ'),
        training_info('HPQ'),
        training_info('JPM'),
        training_info('BAC'),
        training_info('IBM'),
        training_info('WFC'),
        training_info('CMCSA'),
        training_info('INTC'),
        training_info('TSLA'),
        training_info('WMT'),
        training_info('ANET'),
        training_info('ATVI'),
        training_info('ADBE'),
        training_info('ADI'),
        training_info('AMAT'),
        training_info('ADSK'),
        training_info('ADP'),
        training_info('WFC'),
        training_info('FDX'),
        training_info('UPS'),
        training_info('MMM'),
        training_info('ABT'),
        training_info('ABBV'),
        training_info('ACN'),
        training_info('ATVI'),
        training_info('ADBE'),
        training_info('ADT'),
        training_info('AAP'),
        training_info('AES'),
        training_info('AET'),
        training_info('AFL'),
        training_info('AMG'),
        training_info('A'),
        training_info('GAS'),
        training_info('APD'),
        training_info('ARG'),
        training_info('AKAM'),
        training_info('AA'),
        training_info('AGN'),
        training_info('ALXN'),
        training_info('ALLE'),
        training_info('ADS'),
        training_info('ALL'),
        training_info('MO'),
        training_info('AEE'),
        training_info('AAL'),
        training_info('AEP'),
        training_info('AXP'),
        training_info('AIG'),
        training_info('AMT'),
        training_info('AWK'),
        training_info('AMP'),
        training_info('ABC'),
        training_info('AME'),
        training_info('AMGN'),
        training_info('APH'),
        training_info('APC'),
        training_info('ADI'),
        training_info('AON'),
        training_info('APA'),
        training_info('AIV'),
        training_info('AMAT'),
        training_info('ADM'),
        training_info('AIZ'),
        training_info('T'),
        training_info('ADSK'),
        training_info('CAT'),
        training_info('SCHW'),
        training_info('CMG'),
        training_info('CHD'),
        training_info('KO'),
        training_info('CCE'),
        training_info('COST'),
        training_info('DE'),
        training_info('DLTR'),
        training_info('DD'),
        training_info('DUK'),
        training_info('ETFC'),
        training_info('EA'),
        training_info('GPS'),
        training_info('GE'),
        training_info('GM'),
        training_info('HAS'),
        training_info('HD'),
        training_info('JPM'),
        training_info('KSS'),
        training_info('M'),
        training_info('HD'),
        training_info('MRO'),
        training_info('F'),
        training_info('FCX'),
        training_info('PFE'),
    ]

    ai.fit(list(map(lambda x: x[0], histories)),
        list(map(lambda x: x[1], histories)))

    print("Done!")
    print("Saving AI for next time...")
    joblib.dump(ai, 'expert.pkl')
    print("Done!")

def company_worth_investing_once(c, prevp=[]):
    i = get_company_info(c)
    if i == None:
        return None
    else:
        history = list(reversed(list(map(eval, i['history']))))
        current = eval(i['Current'])
        if prevp == 0:
            nvalue = ai.predict([history[1:]+[current]])[0]
        else:
            p = list(map(lambda x: x[-1], prevp))
            size = 206 - len(p)
            nvalue = ai.predict([history[:size]+[current]+p])[0]

        beta = 0
        if i['Beta:'] != 'N/A':
            beta = i['Beta:']
        else:
            return None
        
        b = eval(beta)

        if 0.85 < b < 1.15:
            risk = 'low'
        elif 0.5 < b < 0.85 or 1.15 < b < 1.5:
            risk = 'medium'
        elif 0.5 > b or 1.5 < b:
            risk = 'high'

        # Name, Risk (low/medium/high), Beta, Percentage Increase, CPPS, PPPS
        return (i['Name'],
                risk, b,
                (nvalue-eval(i['Current']))/eval(i['Current']),
                eval(i['Current']),
                nvalue)

def company_worth_investing(c, preds=[], iters=0):
    if iters == 0:
        return preds
    else:
        cwio = company_worth_investing_once(c, preds)
        if cwio == None:
            return None
        else:
            return company_worth_investing(c, preds + [cwio], iters-1)

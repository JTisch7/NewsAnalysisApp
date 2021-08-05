
import flask
from flask import request, jsonify, render_template, url_for, flash, redirect, session
from werkzeug.exceptions import abort

#import sklearn
import json
import pickle
import numpy as np
import pandas as pd
import time
#import psycopg2
from dateutil.parser import parse
import os
import requests
import math
#import threading
#from polygonPull import getPolygonData, recordData
import datetime
#from waitress import serve
import re
import urllib.request
import pytz
import datetime
#import firstChartFuncs
import secondChartFuncs
import combNewsPull

#import tensorflow as tf
import numpy as np
#from transformers import BertTokenizer

import requests
import json



application = flask.Flask(__name__)
#application.config["DEBUG"] = True
#app.config['SECRET_KEY'] = '123453452435243545455678'

chartOne = pickle.load(open('defaultChartData/firstChartData.pkl','rb'))
chartTwo = pickle.load(open('defaultChartData/secondChartStocksData.pkl','rb'))
chartTwoEvents = pickle.load(open('defaultChartData/secondChartEventsData.pkl','rb'))
chartTwoTickers = ['TSLA', 'AAPL', 'NFLX', 'AMZN', 'T', 'GOOG', 'F', 'NKE']

testv = 0
events = ''
company = ''
stocksList = ''
eventsList = ''
ticksStrip = ''



def sentLoop(allLists):
    children1 = []
    for df, sentiments, comp in zip(allLists[0], allLists[2], allLists[4]):
        children2 = []
        for title, sent in zip(df['comb'][:60].tolist(),sentiments[:60]):
            children3 = []
            children3.append(dict([('name', 'positive'),('size',sent[0]),('value',(sent[0]))]))
            children3.append(dict([('name', 'negative'),('size',sent[1]),('value',(0-sent[1]))]))
            children2.append(dict([('name', str(title)),('children',children3)]))
        children1.append(dict([('name', str(comp)),('children', children2)]))
    data1 = [dict([('name','root'),('children',children1)])]
    return data1



def secondChartFunc(days, allLists):
    stocksList = []
    eventsList = []
    for dfNews, events, sentList2, tick in zip(allLists[0], allLists[1], allLists[3], allLists[5]):

        cur30Time = math.floor((time.time()*1000)/1800000)*1800000
        oneDay = 86400000
        ago5 = cur30Time-(oneDay*days)
        stocks1, totalTime = secondChartFuncs.recordData(str(ago5), str(cur30Time), str(tick))

        pos, neg = secondChartFuncs.sortingFunc(dfNews, stocks1, sentList2)
        posAve, negAve, count = secondChartFuncs.sagemakerAPIsent2MaxSent(pos, neg)

        stocks1 = stocks1[:-1]
        stocks1['artCnt'] = count
        stocks1['pos'] = posAve
        stocks1['neg'] = negAve
        columns = ('opn', 'high', 'low', 'close', 'volume', 'epochDate', 'date', 'artCnt', 'pos', 'neg')
        results = []
        z = stocks1.values.tolist()
        for row in z:
            results.append(dict(zip(columns, row)))

        stocksList.append(results)
        eventsList.append(events)

    return stocksList, eventsList



@application.route('/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        if request.form.get('stocks') == 'val1':
            #get function parameters
            if request.form.get('indData')!='moreData':
                days = int(request.form['timePeriod'])
                if days > 8:
                    days = 8
                testv = 0
                stocksList = ''
                eventsList = ''
            if request.form.get('indData')=='moreData':
                days = 6
            company = request.form['company']
            company = company.split(',') 
            company = company[:5]  
            ticks = request.form['tickers'].upper()
            ticks = ticks.split(',') 
            ticksStrip = []
            for tick in ticks:
                ticksStrip.append(tick.strip())
            ticksStrip = ticksStrip[:5]
            #Pull all data for news and create sentiments
            allLists = combNewsPull.createSentDFs(company, days, ticksStrip)    
            #create first chart    
            data = sentLoop(allLists)
            #create second chart
            if request.form.get('indData')=='moreData':
                stocksList, eventsList = secondChartFunc(days, allLists)
                ticksStrip=allLists[5]
                testv = 1
        
        return render_template('SentTemplate.html', data=data, testv=testv, stocks=stocksList, events=eventsList, company=ticksStrip)   
            
    else:
        data = chartOne
        stocksList = chartTwo
        eventsList = chartTwoEvents
        ticksStrip = chartTwoTickers
        testv = 1
        
    return render_template('SentTemplate.html', data=data, testv=testv, stocks=stocksList, events=eventsList, company=ticksStrip)   


@application.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    application.run()

#for waitress on local

#if __name__ == "__main__":
   #app.run() ##Replaced with below code to run it using waitress 
#   serve(application, host="0.0.0.0", port=8000)

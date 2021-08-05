import json
import urllib.request
import pandas as pd
import time
import pytz
from dateutil.parser import parse
import datetime
import json
import numpy as np
import requests
import re
import os

def newsFilterPull(frm, company, begin, end):
    API_KEY = os.environ['newsKEY']
    API_ENDPOINT = "https://api.newsfilter.io/public/actions?token={}".format(str(API_KEY))
    
    queryString = "(title:\"{}\" OR title:\"{}\'s\") AND NOT source.id:sec-api AND publishedAt:[{} TO {}]".format(company, company, begin, end)
    payload = {
        "type": "filterArticles",
        "queryString": queryString,
        "from": frm,
        "size": 50
        }
    
    jsondata = json.dumps(payload)
    jsondataasbytes = jsondata.encode('utf-8')
    req = urllib.request.Request(API_ENDPOINT)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    res_body = response.read()
    articles = json.loads(res_body.decode("utf-8"))
    return articles

def createDateframe(frm, company, begin, end):
    start_time = time.time()
    date = []
    title = []
    desc = []
    source = []

    def loopingFunc(frm, company, begin, end):
        y = frm + 1
        while frm < y:
            time.sleep(1)
            print('running - slowly but surely : ', frm)
            articles = newsFilterPull(frm=frm, company=company, begin=begin, end=end)
            l = 0
            while l < len(articles['articles']):
                title.append(articles['articles'][l]['title'])
                date.append(articles['articles'][l]['publishedAt'])
                source.append(articles['articles'][l]['source']['name'])
                try:
                    desc.append(articles['articles'][l]['description'])
                except:
                    desc.append('')
                l+=1
            y = articles['total']['value']
            frm += 50
            
            if (frm >= y) and (articles['total']['relation'] == 'gte'):
                timestampStr = parse(date[-1]).strftime("%Y-%m-%d")
                loopingFunc(frm=0, company=company, begin=begin, end=timestampStr)
            

    loopingFunc(frm=frm,company=company,begin=begin,end=end)
        
    df = pd.DataFrame()        
    df['date'] = date
    df['title'] = title
    df['description'] = desc
    df['source'] = source
    
    for j in range(len(df)):
        df['date'][j] = parse(df['date'][j]).astimezone(pytz.timezone('America/Los_Angeles'))
     
    end_time = time.time()
    totalTime = (end_time-start_time)/60
    return df, totalTime


def sagemakerAPIsent(df):
    def APIFunc(payload):
        url = os.environ['urlKEY']
        headers = {"Content-Type": "application/json"}
        r = requests.request("POST", str(url), headers=headers, data=json.dumps(payload))
        z = json.loads(r.text)
        return z

    sentList = []
    sentListpos = []
    sentListneg = []

    i=0
    while i < len(df):
        titList = []
        for title in df['title'][i:(i+20)]:
            titList.append({'text': title})
        inp = {'instances': titList}
        sentiments = APIFunc(inp)
        for sent in sentiments:
            sentList.append(sent[0:2])
            sentListpos.append(sent[0])
            sentListneg.append(sent[1])
        print(i)
        i+=20

    sentListneg1 = [-x for x in sentListneg]
    sentList2 = [sentListpos, sentListneg1]

    return sentList, sentList2



def createSentDFs(company, days, ticksStrip):
    TicksUpd = []
    dfList = []
    evList = []
    combSentList = []
    combSentList2 = []
    compList = []
    today = str(datetime.date.today())
    numDays = datetime.timedelta(days)
    Ago3 = str(datetime.date.today()-numDays)
    for comp, tick in zip(company, ticksStrip):
        df, totalTime = createDateframe(frm=0, company=str(comp), begin=Ago3, end=today)
        df = df.drop_duplicates(subset='title', keep='last').reset_index(drop=True)
        df = df[df.source != 'SEC']
        if len(df) > 0:
            sentList, sentList2 = sagemakerAPIsent(df)
            titleTrunc = []
            for title in df['title']:
                tit = title[0:500]
                tit = re.sub(pattern = "[^\w\s]", repl = "", string = tit)
                titleTrunc.append(tit)
            df['titleTrunc'] = titleTrunc
            df['comb'] = df['date'].astype(str) + ' - ' + df['titleTrunc']
            events = []

            columns = ('date', 'description')
            dfEv = df[['date', 'titleTrunc']].values.tolist()
            for row in dfEv:
                events.append(dict(zip(columns, row)))

            dfList.append(df)
            evList.append(events)
            combSentList.append(sentList)
            combSentList2.append(sentList2)
            compList.append(comp)
            TicksUpd.append(tick)
    return dfList, evList, combSentList, combSentList2, compList, TicksUpd
    


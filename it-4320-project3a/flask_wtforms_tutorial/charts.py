'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
import time
import datetime
import pygal
import midtermstruct4320
import json

def apiRequest(function,symbol,apikey):
    if function == "1":
        url= 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+symbol+'&interval=60min&outputsize=full&apikey=('+apikey+')'
        r = requests.get(url)
        data = r.json()
        return data
    if function == "2":
        url= 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&outputsize=full&apikey=('+apikey+')'
        r = requests.get(url)
        data = r.json()
        return data
    if function == "3":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+symbol+'&outputsize=full&apikey=('+apikey+')'
        r = requests.get(url)
        data = r.json()
        return data
    if function == "4":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+symbol+'&outputsize=full&apikey=('+apikey+')'
        r = requests.get(url)
        data = r.json()
        return data

def refineData(data,bd,ed,function):
    list1=[]
    format1=""
    if function == "1":
        format1= '%Y-%m-%d %H:%M:%S'
        bd=bd+' 00:00:00'
        ed=ed+' 00:00:00'
    else:
        format1 = '%Y-%m-%d'
    for item in data:
        x = datetime.datetime.strptime(item, format1)
        x1 = datetime.datetime.strptime(bd, format1)
        x2 = datetime.datetime.strptime(ed, format1)
        #print(item)
        if (x < x2 or x == x2) and( x > x1 or x == x1):
            open1=float(data[item]['1. open'])
            high=float(data[item]['2. high'])
            low=float(data[item]['3. low'])
            close=float(data[item]['4. close'])
            volume=float(data[item]['5. volume'])
            date=item
            #print(date)
            temp = midtermstruct4320.midtermstruct(open1,high,low,close,volume,date)
            list1.append(temp)
        else:
            continue
    return list1


def timeSeriesCheck(function):
    timeSeries=''
    if function == "1":
        timeSeries = 'Time Series (60min)'
    if function == "2":
        timeSeries = 'Time Series (Daily)'
    if function == "3":
        timeSeries = 'Weekly Time Series'
    if function == "4":
        timeSeries = 'Monthly Time Series'
    return timeSeries

def makeGraph(choice,data6,lowDate,highDate,symbol,function):
    open2=[]
    high1=[]
    low1=[]
    close1=[]
    volume1=[]
    date1=[]
    if choice == "1":
        chart=pygal.Line(x_label_rotation=45)
    if choice == "2":
        chart=pygal.Bar(x_label_rotation=45)
    for item in data6:
        temp = item.getOpen()
        open2.append(temp)
        temp = item.getHigh()
        high1.append(temp)
        temp = item.getLow()
        low1.append(temp)
        temp=item.getClose()
        close1.append(temp)
        temp=item.getVolume()
        volume1.append(temp)
        temp=item.getDate()
        date1.append(temp)
    chart.title = ''+symbol+' stock data from '+lowDate+' to ' +highDate+''
    temp10=date1
    temp10.reverse()
    if function == "1":
        lowDate = lowDate + ' 00:00:00'
    if choice != "1":
        lowDate = lowDate
    temp10.insert(0,lowDate)
    chart.x_labels = temp10                                                                      
    chart.add('Open',open2)
    chart.add('High',high1)
    chart.add('Low',low1)
    chart.add('Close',close1)
    chart.render_in_browser()


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()


'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal
import requests
import json
import midtermstruct4320

def x1():
    symbol,chart,function,bd,ed,apikey=questions()
    data=apiRequest(function,symbol,apikey)
    timeSeries=timeSeriesCheck(function)
    data1=(data[timeSeries])
    test=json.dumps(data1)
    test2=json.loads(test)
    data7=refineData(test2,bd,ed,function)
    graph1=makeGraph(chart,data7,bd,ed,symbol,function)
    again=exit()
    
    
#makes graph option two supposed to be bar graph
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
        # print(item)
        if (x < x2 or x == x2) and( x > x1 or x == x1):
            open1=float(data[item]['1. open'])
            high=float(data[item]['2. high'])
            low=float(data[item]['3. low'])
            close=float(data[item]['4. close'])
            volume=float(data[item]['5. volume'])
            date=item
            # print(date)
            temp = midtermstruct4320.midtermstruct(open1,high,low,close,volume,date)
            list1.append(temp)
        else:
            continue
    return list1


def makeGraph(choice,data6,lowDate,highDate,symbol,function): #has to match makeGraph variable in routes.py file
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

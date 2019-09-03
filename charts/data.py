import json
from datetime import datetime
from datetime import timedelta
import os,binascii
import argparse

DATEFORMAT='%Y-%m-%d'
parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
parser.add_argument('--days', default=30)
days = int(parser.parse_args().days)
startDate = (datetime.now() - timedelta(days=days)).strftime(DATEFORMAT)
# Adjust start date to first trading day on or b4 startDate
with open("full/SPY-full.json", 'r') as f:
    spyTrades = json.load(f)
    while (spyTrades["Time Series (Daily)"].get(startDate, None) is None):
        days += 1
        startDate = (datetime.now() - timedelta(days=days)).strftime(DATEFORMAT)

data = dict()
initialPrice = dict()
symbols = [line.rstrip() for line in open('symbols.txt')]
with open('header.html') as f: output = f.read()
for symbol in symbols:
    with open("full/%s-full.json" % symbol, 'r') as f:
        data[symbol] = json.load(f)
        initialPrice[symbol] = float(data[symbol]["Time Series (Daily)"].get(startDate)["4. close"])
        output += "      data.addColumn('number', '%s');\n" % symbol

output += "      fullDataSet = [\n"
for days in range(1, days):
    currentDate =  datetime.strptime(startDate, DATEFORMAT) + timedelta(days=days)
    dateString = currentDate.strftime(DATEFORMAT)
    out = "[new Date({0}, {1}, {2})".format(currentDate.strftime('%Y'),
        int(currentDate.strftime('%m')) - 1,
        currentDate.strftime('%d'))
    for symbol in symbols:
        currentPrice = float(data[symbol]["Time Series (Daily)"].get(dateString, {"4. close": -1})["4. close"])
        if currentPrice != -1:
            out += ", {:.2f}".format((currentPrice - initialPrice[symbol]) / initialPrice[symbol] * 100)
        else:
            out = None
            break
    if out is not None:
        output += out + '],\n' 

output += "\n      ];\n      data.addRows(fullDataSet);\n      var options = { hAxis: { title: 'Date' }, width:2000, height:1500, vAxis: { title: 'Capital Gain' }, colors: [\n"
for symbol in symbols:
    if symbol == 'SPY':
        output += "          '#FF0000',\n"
    else:
        output += "          '#" + binascii.b2a_hex(os.urandom(3)) + "',\n"

output += "] }; var chart = new google.visualization.LineChart(document.getElementById('chart_div')); chart.draw(data, options); } </script>"

print output

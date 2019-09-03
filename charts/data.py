import json
from datetime import datetime
from datetime import timedelta
import os,binascii

START="2019-08-01"
DATEFORMAT='%Y-%m-%d'

data = dict()
initialPrice = dict()
startDate = (datetime.strptime(START, DATEFORMAT)).strftime(DATEFORMAT)
days = (datetime.now() - datetime.strptime(START, DATEFORMAT)).days
symbols = [line.rstrip() for line in open('symbols.txt')]
with open('header.html') as f: output = f.read()
for symbol in symbols:
    with open("full/%s-full.json" % symbol, 'r') as f:
        data[symbol] = json.load(f)
        initialPrice[symbol] = float(data[symbol]["Time Series (Daily)"].get(startDate)["4. close"])
        output += "      data.addColumn('number', '%s');\n" % symbol

output += "      fullDataSet = [\n"
for days in range(1, days):
    currentDate = datetime.strptime(START, DATEFORMAT) + timedelta(days=days)
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

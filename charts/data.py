import json
from datetime import datetime
from datetime import timedelta

START="2019-03-05"
DATEFORMAT='%Y-%m-%d'

data = dict()
initialPrice = dict()
symbols = [line.rstrip() for line in open('symbols.txt')]
for symbol in symbols:
    with open("full/%s-full.json" % symbol, 'r') as f:
        data[symbol] = json.load(f)
        dateString = (datetime.strptime(START, DATEFORMAT)).strftime(DATEFORMAT)
        initialPrice[symbol] = float(data[symbol]["Time Series (Daily)"].get(dateString)["4. close"])

output = ''
for days in range(1, 179):
    currentDate = datetime.strptime(START, DATEFORMAT) + timedelta(days=days)
    dateString = currentDate.strftime(DATEFORMAT)
    out = "[new Date({0}, {1}, {2})".format(currentDate.strftime('%Y'),
        int(currentDate.strftime('%m')) - 1,
        currentDate.strftime('%d'))
    for symbol in symbols:
        currentPrice = float(data[symbol]["Time Series (Daily)"].get(dateString, {"4. close": -1})["4. close"])
        if currentPrice != -1:
            out += ", {:.2f}".format((currentPrice - initialPrice[symbol]) / initialPrice[symbol] * 100)
#            out += str((currentPrice - initialPrice[symbol]) / initialPrice[symbol] * 100)
        else:
            out = None
            break
    if out is not None:
        output += out + '],\n' 
print output

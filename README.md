# misc-scripts

```
for stock in `cat ../symbols.txt `; do curl 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='$stock'&apikey=$APIKEY&outputsize=full' > ${stock:?}-full.json; sleep 20; done
```

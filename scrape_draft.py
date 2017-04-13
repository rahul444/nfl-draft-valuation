import bs4 as bs
import urllib.request

def get(year):
    trades = []
    URL = 'http://www.prosportstransactions.com/football/DraftTrades/Years/' + str(year) + '.htm'
    source = urllib.request.urlopen(URL).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    print(soup)
    for p in soup.findAll("p", class_='bodyCopySm'):
        trades.append(p.string)
    filter(None, trades)
    return trades

years = [2013]
result = []
for year in years:
    result.append(get(year))

print(result)

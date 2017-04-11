import bs4 as bs
import urllib.request
import requests

# URL = "https://pythonprogramming.net/parsememcparseface/"
URL = "http://www.pro-football-reference.com/players/"

source = urllib.request.urlopen(URL).read()
soup = bs.BeautifulSoup(source, 'lxml')

def get_player_stats(first, last):
    last = last[:4]
    if len(last) < 4:
        last = last + ("x" * (4 - len(last)))
    first = first[:2]

    suffix = "00"
    path = last[0] + "/" + last + first + suffix + ".htm"

    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    # r = requests.get(URL+path, headers=headers)
    # data = r.text
    # soup = bs.BeautifulSoup(data, "lxml")
    # print(soup.find_all('div', class_='table_wrapper table_controls'))
    
    print(URL + path)
    
    source = urllib.request.urlopen(URL + path).read()
    soup = bs.BeautifulSoup(source, 'lxml')

    print(soup.text)
    # print(soup.find_all('div', class_='table_wrapper table_controls'))


get_player_stats("Tom", "Brady")

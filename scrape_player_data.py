import bs4 as bs
import urllib.request
import requests

BASE_URL = "http://www.pro-football-reference.com/players/"

def get_url(name):
    first, last = name.split()
    last = last[:4]
    if len(last) < 4:
        last = last + ("x" * (4 - len(last)))
    first = first[:2]

    suffix = "00"
    path = last[0] + "/" + last + first + suffix + ".htm"
    return BASE_URL + path


def get_player_stats(name):
    URL = get_url(name)
    print(URL)

    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    # r = requests.get(URL+path, headers=headers)
    
    source = urllib.request.urlopen(URL).read()
    soup = bs.BeautifulSoup(source, 'lxml')

    meta = str(soup.find_all('div', class_='players')[0])
    pos_index = meta.index("Position")
    position = meta[pos_index + 19: pos_index + 21]
    print(position)
    
    # print(soup.find_all('div', class_='table_outer_container'))
    # print(soup.find_all('tr', class_='full_table'))


get_player_stats("Tom Brady")
get_player_stats("Jason Kelce")



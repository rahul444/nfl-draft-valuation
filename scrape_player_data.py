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
    path = last[0] + "/" + last + first
    
    # try all possible urls for certain player
    for i in range(10):
        suffix = "0" + str(i) + ".htm"
        URL = BASE_URL + path + suffix
        source = urllib.request.urlopen(URL).read()
        soup = bs.BeautifulSoup(source, 'lxml')
        site_name = soup.find_all('h1')[0].text.strip()
        if site_name == name:
            break

    return URL, soup


def get_player_stats(name):
    URL, soup = get_url(name)
    print(URL)

    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    # r = requests.get(URL+path, headers=headers)

    print(soup.find_all('h1')[0].string)

    meta = str(soup.find_all('div', class_='players')[0])
    pos_index = meta.index("Position")
    position = meta[pos_index + 19: pos_index + 21]
    print(position)
    
    table = soup.find_all('tr', class_='full_table')
    parse_table(table, position)

def parse_table(table, pos):
    if pos == "QB":
        parse_qb_table(table)
    elif pos == "RB":
        parse_rb_table(table)
    elif pos == "WR":
        parse_wr_table(table)
    return None

def parse_qb_table(table):
    tds = 0
    yards = 0
    for row in table:
        gs = row.find('td', {"data-stat" : "gs"}).string
        tds += int(row.find('td', {"data-stat" : "pass_td"}).string)
        yards += int(row.find('td', {"data-stat" : "pass_yds"}).string)


    print('average tds:')
    print(tds/len(table))

    print('average yards:')
    print(yards/len(table))

    return None

def parse_rb_table(table):
    return None

def parse_wr_table(table):
    return None


get_player_stats("Tom Brady")
# get_player_stats("Dan Marino")
# get_player_stats("Janoris Jenkins")



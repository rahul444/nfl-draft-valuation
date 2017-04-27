import bs4 as bs
import urllib.request

BASE_URL = 'http://www.pro-football-reference.com/players/'

def get_player_stats(name):
    URL, soup = get_url(name)
    if soup == None:
        return
    print(URL)
    print(soup.find_all('h1')[0].string)

    meta = str(soup.find_all('div', class_='players')[0])
    pos_index = meta.index('Position')
    position = meta[pos_index + 19: pos_index + 21]
    
    table = soup.find_all('tr', class_='full_table')
    val = parse_table(table, position)
    print(val)
    return val

def get_url(name):
    first, last = name.split()
    last = last[:4]
    if len(last) < 4:
        last = last + ('x' * (4 - len(last)))
    first = first[:2]

    suffix = '00'
    path = last[0] + '/' + last + first
    
    # try all possible urls for certain player
    for i in range(10):
        suffix = '0' + str(i) + '.htm'
        URL = BASE_URL + path + suffix
        source = urllib.request.urlopen(URL).read()
        soup = bs.BeautifulSoup(source, 'lxml')
        site_name = soup.find_all('h1', {'itemprop' : 'name'})
        if len(site_name) == 0:
            return None, None
        site_name = site_name[0].text.strip()
        if site_name == name:
            break

    return URL, soup

def parse_table(table, pos):
    if pos == 'QB':
        return parse_qb_table(table)
    elif pos == 'RB':
        return parse_rb_table(table)
    elif pos == 'WR':
        return parse_wr_table(table)
    return None

def parse_qb_table(table):
    tds = []
    yards = []
    av = []
    probowls = 0
    allpros = 0

    for row in table:
        gs = int(row.find('td', {'data-stat' : 'gs'}).string)
        if gs < 10:
            continue
        
        year = row.find('th', {'data-stat' : 'year_id'}).text
        if '*' in year:
            probowls += 1
        if '+' in year:
            allpros += 1
        
        tds.append(int(row.find('td', {'data-stat' : 'pass_td'}).string))
        yards.append(int(row.find('td', {'data-stat' : 'pass_yds'}).string))
        av.append(int(row.find('td', {'data-stat' : 'av'}).string))

    for i in range(3):
        tds.remove(min(tds))
        yards.remove(min(yards))
        av.remove(min(av))

    ave_tds = sum(tds)/len(tds)
    ave_yds = sum(yards)/len(yards)
    ave_av = sum(av)/len(av)

    # TODO tune weights
    # 1. Tune weights so a list of players matches some established ranking
    # 2. Tune weights such that variance is minimized across a list of players
    metric = 1.4*probowls + 0.6*allpros + 0.85*ave_tds + 0.008*ave_yds + 0.45*ave_av
    return metric

def parse_rb_table(table):
    tds = []
    yards = []
    ypc = []
    attempts = []
    av = []
    probowls = 0
    allpros = 0

    for row in table:
        gs = int(row.find('td', {'data-stat' : 'gs'}).string)
        if gs < 10:
            continue
        
        year = row.find('th', {'data-stat' : 'year_id'}).text
        if '*' in year:
            probowls += 1
        if '+' in year:
            allpros += 1
        
        tds.append(int(row.find('td', {'data-stat' : 'rush_td'}).string))
        yards.append(int(row.find('td', {'data-stat' : 'rush_yds'}).string))
        ypc.append(float(row.find('td', {'data-stat' : 'rush_yds_per_att'}).string))
        attempts.append(float(row.find('td', {'data-stat' : 'rush_att_per_g'}).string))
        av.append(int(row.find('td', {'data-stat' : 'av'}).string))

    for i in range(3):
        tds.remove(min(tds))
        yards.remove(min(yards))
        ypc.remove(min(ypc))
        attempts.remove(min(attempts))
        av.remove(min(av))

    ave_tds = sum(tds)/len(tds)
    ave_yds = sum(yards)/len(yards)
    ave_ypc = sum(ypc)/len(ypc)
    ave_attempts = sum(attempts)/len(attempts)
    ave_av = sum(av)/len(av)

    # TODO tune weights
    # 1. Tune weights so a list of players matches some established ranking
    # 2. Tune weights such that variance is minimized across a list of players
    metric = 2.4*probowls + 0.9*allpros + 1.6*ave_tds + 0.0032*ave_yds + 4*ave_ypc + 0.8*ave_attempts + 0.7*ave_av
    return metric

def parse_wr_table(table):
    tds = []
    yards = []
    rec = []
    av = []
    probowls = 0
    allpros = 0

    for row in table:
        gs = int(row.find('td', {'data-stat' : 'gs'}).string)
        if gs < 10:
            continue
        
        year = row.find('th', {'data-stat' : 'year_id'}).text
        if '*' in year:
            probowls += 1
        if '+' in year:
            allpros += 1
        
        tds.append(int(row.find('td', {'data-stat' : 'rec_td'}).string))
        yards.append(int(row.find('td', {'data-stat' : 'rec_yds'}).string))
        rec.append(int(row.find('td', {'data-stat' : 'rec'}).string))
        av.append(int(row.find('td', {'data-stat' : 'av'}).string))

    for i in range(3):
        tds.remove(min(tds))
        yards.remove(min(yards))
        rec.remove(min(rec))
        av.remove(min(av))

    ave_tds = sum(tds)/len(tds)
    ave_yds = sum(yards)/len(yards)
    ave_rec = sum(rec)/len(rec)
    ave_av = sum(av)/len(av)

    # TODO tune weights
    # 1. Tune weights so a list of players matches some established ranking
    # 2. Tune weights such that variance is minimized across a list of players
    metric = 1.9*probowls + 0.6*allpros + 1.1*ave_tds + 0.02*ave_yds + 0.9*ave_av
    return metric

# get_player_stats('Peyton Manning')
# get_player_stats('Jay Cutler')
# get_player_stats('Russell Wilson')
# TODO doesn't work if another player has same name
# get_player_stats('Alex Smith')

# get_player_stats('Larry Fitzgerald')
# get_player_stats('Randy Moss')
# get_player_stats('Michael Crabtree')

# get_player_stats('LaDainian Tomlinson')


import bs4 as bs
import urllib.request
import re

def get(year):
    trades = [year]
    URL = 'http://www.prosportstransactions.com/football/DraftTrades/Years/' + str(year) + '.htm'
    source = urllib.request.urlopen(URL).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    for tr in soup.find_all("tr"):
        transaction = {}
        teams = [div.text.strip() for div in tr.find_all("div", "textrightoflogo")]
        trade = [p.text.strip() for p in tr.find_all("p", "bodyCopySm")]
        transaction['overall_num'] = tr.find("td").text
        transaction['teams'] = teams
        transaction['trades'] = trade
        if trade:
            trades.append(transaction)
    filter(None, trades)
    return trades

def sort(all_trades):
    all_data = []
    for year_data in all_trades:
        year = year_data[0]
        transactions = year_data[1:]
        for tx in transactions:
            acquisitions = {}
            allTeams = tx['teams']
            mainTeam = tx['teams'][0]
            otherTeams = tx['teams'][1:]
            overall_num = tx['overall_num']
            trades = tx['trades']
            for name in allTeams:
                acquisitions[name] = []

            for i in range(0, len(otherTeams)):
                pattern = re.compile('\((#[^)]+)\)|to (\w+)')
                match = pattern.findall(trades[i])
                if match[0][0] == "":
                    break
                otherTeam = ""
                for pair in match:
                    if pair[1] != "":
                        otherTeam = pair[1]
                addTo = otherTeam

                for player in match:
                    if player[1] != "":
                        addTo = otherTeams[i]
                        continue
                    else:
                        acquisitions[addTo].append(player[0])
                data = [year, overall_num, acquisitions]
                all_data.append(data)
    return all_data




years = [2013]
result = []
for year in years:
    result.append(get(year))


#
# pattern = re.compile('\((#[^)]+)\)|to (\w+)')
# match = pattern.findall('Traded 2012 seventh round pick (#211-Scott Solomon) to Titans for 2013 sixth round pick (#176-David Quessenberry) on 2012-04-28')
# print(match)
# otherTeam = ""
# for pair in match:
#     if pair[1] != "":
#         otherTeam = pair[1]



print(sort(result))


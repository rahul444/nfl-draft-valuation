import scrape_player_data as stats
# import scrape_transaction as trades

DRAFT_CHART = [3000, 2600, 2200, 1800, 1700, 1600, 1500, 1400, 1350, 1300, 1250, 1200, 1150, 1100, 1050, 1000, 950, 900, 875, 850, 800, 780, 760, 740, 720, 700, 680, 660, 640, 620, 600, 590]

def calc_points_from_draft_chart(pick):
    return DRAFT_CHART[pick - 1]

print(stats.get_player_stats('Peyton Manning'))
# print(trades.get(2013))
import clustering as clst
import top_trading_cycles as ttc

exper_data = [[float(num) for num in lines] for lines in open("Auction.txt").read().splitlines()]
teams,users = clst.kmeans_assignment(exper_data)
ttc.team_swap(teams,users)
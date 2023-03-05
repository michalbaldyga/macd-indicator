from functions import *

N = 1000
macd_results = [None] * N
signal_results = [None] * N
stock = 1000

df = read_data('data.csv')

calculate_indicators(macd_results, signal_results, df.Zamkniecie, N)

draw_plots(df, macd_results, signal_results)

make_decision(macd_results, signal_results, stock, N, df.Zamkniecie)

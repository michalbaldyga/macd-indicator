import pandas as pd


def compute_ema(periods_no, samples, curr_sample):
    alfa = 2/(periods_no + 1)
    numerator = 0.0
    denominator = 0.0

    for i in range(periods_no + 1):
        if (curr_sample - i) >= 0:
            numerator += pow((1 - alfa), i) * samples[curr_sample - i]
            denominator += pow((1 - alfa), i)

    return numerator/denominator


def compute_macd(samples, curr_sample):
    ema_12 = compute_ema(12, samples, curr_sample)
    ema_26 = compute_ema(26, samples, curr_sample)
    return ema_12 - ema_26


def compute_signal(macd_samples, curr_sample):
    return compute_ema(9, macd_samples, curr_sample)


def read_data(path):
    return pd.read_csv(path)


def draw_plots(df, macd, signal):
    df.plot(x="Data", y="Zamkniecie", title="WIG20", xlabel="Dzień", ylabel="Cena zamknięcia")
    output_data = {
        'Data': df.Data,
        'MACD': macd,
        'SIGNAL': signal
    }
    df_output = pd.DataFrame(output_data)
    df_output.plot(x="Data", y=["MACD", "SIGNAL"], title="MACD/SIGNAL", xlabel="Dzień")


def calculate_indicators(macd, signal, samples, periods_no):
    for i in range(periods_no):
        macd[i] = compute_macd(samples, i)
    for i in range(periods_no):
        signal[i] = compute_signal(macd, i)


def make_decision(macd, signal, stock_no, periods_no, samples):
    pocket = stock_no * samples[0]  # aktualny kapitał
    stock_no = 0  # akutalna liczba posiadanych akcji
    investment_percent = 0.5  # 50%
    is_macd_higher = False  # określa czy MACD jest wyżej niż SIGNAL
    if macd[1] > signal[1]:
        is_macd_higher = True

    for i in range(2, periods_no):
        if macd[i] < signal[i] and is_macd_higher:
            # SELL
            pocket += stock_no * samples[i]
            stock_no = 0
            is_macd_higher = False
        elif macd[i] > signal[i] and is_macd_higher is False:
            # BUY
            stock_no += investment_percent * pocket / samples[i]
            pocket -= investment_percent * pocket
            is_macd_higher = True

    pocket += stock_no * samples[periods_no-1]
    income = pocket / (1000 * samples[0])
    print(f'Kapitał początkowy: {1000 * samples[0]}')
    print(f'Kapitał końcowy: {round(pocket,2)}')
    print(f'Zysk: {income}')

import logging
import pandas as pd


def data_setup():
    """
    데이터 파일 추가
    :return:
    """
    E1h = pd.DataFrame(
        columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'EMA5', 'EMA10', 'EMA20', 'EMA60', 'MACD',
                 'MACDsignal',
                 'MACD-S'])
    E1h.set_index(['Time'])
    E1h.to_csv('Every1Hour.csv', index=False)
    E15m = pd.DataFrame(
        columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'EMA5', 'EMA10', 'EMA20', 'EMA60', 'MACD',
                 'MACDsignal',
                 'MACD-S'])
    E15m.set_index(['Time'])
    E15m.to_csv('Every15Minutes.csv', index=False)


def add_EMAs(filename):
    """
    MACD > 0 ? 상승 : 하락
    :return: None
    """
    df = pd.read_csv(filename, delimiter=',')
    df.iloc[:, 2:6].astype('float')
    print(df.iloc[:, [4]].columns)
    print(df.iloc[:, [10]].columns)
    df['EMA5'] = df.iloc[:, [4]].ewm(span=5, adjust=False).mean()
    df['EMA10'] = df.iloc[:, [4]].ewm(span=10, adjust=False).mean()
    df['EMA20'] = df.iloc[:, [4]].ewm(span=20, adjust=False).mean()
    df['EMA60'] = df.iloc[:, [4]].ewm(span=60, adjust=False).mean()
    df['MACD'] = df.iloc[:, [4]].ewm(span=12, adjust=False).mean() - df.iloc[:, [4]].ewm(span=26, adjust=False).mean()
    df['MACDsignal'] = df.iloc[:, [10]].ewm(span=9, adjust=False).mean()
    df['MACD-S'] = df['MACD'] - df['MACDsignal']
    logging.info(df)
    df.to_csv(filename, index=False, encoding='UTF-8')


def getData(filename):
    result = pd.read_csv(filename, delimiter=',')
    return result.tail(200)

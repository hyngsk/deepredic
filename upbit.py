import datetime

from upbitpy import Upbitpy
import pandas as pd


class Upbit:
    def __init__(self):
        self.__upbit = Upbitpy()
        self.__krw_markets = self.__get_krw_markets()

    def __get_krw_markets(self):
        krw_markets = dict()
        all_markets = self.__upbit.get_market_all()
        for market in all_markets:
            if market['market'].startswith('KRW-'):
                krw_markets[market['market']] = market
        # print(krw_markets)
        return krw_markets

    def get_15minutes_candle(self, market):
        '''
        주어진 코인명에 대하여 15분 봉의 200개 캔들을 조회
        :param market: 마켓 네임
        :return: 데이터 프레임 columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close"})
        '''
        if market not in self.__krw_markets.keys():
            return None
        candles = self.__upbit.get_minutes_candles(15, market, count=1)
        dt_list = [datetime.datetime.strptime(x['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S") for x in candles]
        df = pd.DataFrame(candles, columns=['opening_price', 'high_price', 'low_price', 'trade_price'], index=dt_list)
        df = df.rename(
            columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close"})
        # print(candles, type(candles))
        return df

    def get_1hour_candle(self, market):
        '''
        주어진 코인명에 대하여 1시 봉의 1개 캔들을 조회
        :param market: 마켓 네임
        :return: 데이터 프레임 columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close"})
        '''
        if market not in self.__krw_markets.keys():
            return None
        candles = self.__upbit.get_minutes_candles(60, market, count=1)
        dt_list = [datetime.datetime.strptime(x['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S") for x in candles]
        df = pd.DataFrame(candles, columns=['opening_price', 'high_price', 'low_price', 'trade_price'], index=dt_list)
        df = df.rename(
            columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close"})
        # print(candles, type(candles))
        return df


    def get_current_price(self, market):
        cp = self.__upbit.get_ticker(market)
        #print(cp)
        return cp

    def get_hour_candles(self, market):
        if market not in self.__krw_markets.keys():
            return None
        candles = self.__upbit.get_minutes_candles(15, market, count=60)
        #print(candles)
        return candles

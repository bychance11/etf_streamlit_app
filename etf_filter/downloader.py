# etf_filter/downloader.py

import yfinance as yf
import pandas as pd
import ssl

# SSL 인증서 오류 우회 (사내망 대응용)
ssl._create_default_https_context = ssl._create_unverified_context

def get_price_on_date(ticker, date):
    try:
        # 앞뒤 2일 범위로 요청하여 주말/공휴일 문제 회피
        df = yf.download(ticker, start=date - pd.Timedelta(days=2), end=date + pd.Timedelta(days=2), progress=False)
        if df.empty:
            return None
        # 가장 가까운 날짜 기준 종가 사용
        nearest_date = min(df.index, key=lambda d: abs(d.date() - date))
        return df.loc[nearest_date]['Adj Close']
    except Exception as e:
        print(f"⚠️ {ticker} 실패: {e}")
        return None

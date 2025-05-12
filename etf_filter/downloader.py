# etf_filter/downloader.py

import yfinance as yf
import pandas as pd
import ssl

# SSL 인증서 오류 우회 (사내망 대응용)
ssl._create_default_https_context = ssl._create_unverified_context

def get_price_on_date(ticker, date):
    try:
        df = yf.download(ticker, start=date, end=date + pd.Timedelta(days=1), progress=False)
        if df.empty:
            return None
        return df['Adj Close'].iloc[0]
    except Exception as e:
        print(f"{ticker} 다운로드 실패: {e}")
        return None

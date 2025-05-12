# etf_filter/etf_universe.py

import yfinance as yf
import pandas as pd
import ssl
from config.settings import ETF_CSV_PATH

# SSL 인증서 오류 우회 (사내망 대응용)
ssl._create_default_https_context = ssl._create_unverified_context

# 기본 ETF 후보 리스트 (거래량 상위 가능성 높은 ETF)
ETF_CANDIDATES = [
    'SPY', 'QQQ', 'DIA', 'IWM', 'TLT', 'HYG', 'XLF', 'XLK', 'XLY', 'XLI', 'XLV', 'XLE',
    'ARKK', 'VTI', 'IEMG', 'EFA', 'VWO', 'GDX', 'GLD', 'SLV', 'USO', 'XBI', 'SOXX', 'SMH',
    'BITO', 'SCHD', 'JEPI', 'VOO', 'VEA', 'VXUS', 'BND', 'LQD', 'EMB', 'SHV', 'XLC', 'XLRE'
]

def update_etf_csv(top_n=300):
    etf_data = []

    for ticker in ETF_CANDIDATES:
        try:
            df = yf.download(ticker, period='1d', progress=False)
            if df.empty:
                continue
            volume = df['Volume'].iloc[-1]
            volume = volume.item() if hasattr(volume, 'item') else volume  # fix: ensure scalar
            etf_data.append((ticker, volume))
        except Exception as e:
            print(f"{ticker} 실패: {e}")
            continue

    sorted_etfs = sorted(etf_data, key=lambda x: x[1], reverse=True)
    top_etfs = sorted_etfs[:top_n]

    df_out = pd.DataFrame(top_etfs, columns=['Ticker', 'Volume'])
    df_out.to_csv(ETF_CSV_PATH, index=False, encoding='cp949')
    print(f"✅ ETF 목록이 {ETF_CSV_PATH}에 저장되었습니다.")

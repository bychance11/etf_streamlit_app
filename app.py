# app.py

import streamlit as st
from etf_filter.calculator import run_filter_and_return
from etf_filter.etf_universe import update_etf_csv

st.set_page_config(page_title="ETF 추세 필터", layout="centered")
st.title("📈 ETF 추세 필터 웹앱")

st.markdown("""
이 앱은 최근 주간 수익률 기준으로 '하락 후 반등'한 ETF를 자동으로 분석합니다.\
`yfinance` 데이터를 기반으로 작동하며, 거래량 상위 ETF 목록도 갱신할 수 있습니다.
""")

x = st.number_input("최근 주 수 (x)", min_value=1, max_value=12, value=1)
y = st.number_input("그 이전 주 수 (y)", min_value=1, max_value=12, value=2)
update_flag = st.checkbox("📌 거래량 기준 ETF 티커 업데이트")

if st.button("🔍 분석 시작"):
    if update_flag:
        update_etf_csv()
        st.success("✅ ETF 목록이 성공적으로 갱신되었습니다.")

    result_df = run_filter_and_return(x, y)

    if result_df.empty:
        st.warning("조건에 맞는 ETF가 없습니다.")
    else:
        st.success(f"{len(result_df)}개 ETF가 조건에 부합합니다.")
        st.dataframe(result_df)

        # 결과 다운로드 버튼
        st.download_button(
            label="📥 결과 다운로드 (.csv)",
            data=result_df.to_csv(index=False).encode('utf-8-sig'),
            file_name="filtered_etfs.csv",
            mime="text/csv"
        )

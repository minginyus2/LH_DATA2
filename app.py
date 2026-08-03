import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------
# 1. Streamlit 페이지 기본 설정
# --------------------------------
st.set_page_config(
    page_title="서울시 구급활동 분석",
    page_icon="🚑",
    layout="wide"
)

# --------------------------------
# 2. 제목과 설명
# --------------------------------
st.title("🚑 서울시 구급활동 분석")

st.write(
    """
    서울시 자치구별로 구급대가 현장에 도착한 이후,
    환자에게 접촉하기까지 걸린 평균시간을 비교한 결과입니다.
    """
)

# --------------------------------
# 3. CSV 데이터 불러오기
# --------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("district_access_summary.csv")


df = load_data()

# --------------------------------
# 4. 데이터 확인
# --------------------------------
st.subheader("자치구별 분석 결과")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------
# 5. 자치구별 평균시간 정렬
# --------------------------------
district_mean = df.sort_values(
    "평균시간",
    ascending=True
)

# --------------------------------
# 6. 그래프 만들기
# --------------------------------
fig, ax = plt.subplots(figsize=(10, 9))

ax.barh(
    district_mean["시군구명"],
    district_mean["평균시간"]
)

ax.set_title(
    "서울시 자치구별 현장도착 후 환자접촉 평균시간",
    fontsize=15
)

ax.set_xlabel("평균 소요시간(분)")
ax.set_ylabel("자치구")

# 막대 끝에 숫자 표시
for index, value in enumerate(district_mean["평균시간"]):
    ax.text(
        value + 0.02,
        index,
        f"{value:.2f}",
        va="center",
        fontsize=9
    )

plt.tight_layout()

# --------------------------------
# 7. Streamlit에 그래프 출력
# --------------------------------
st.subheader("자치구별 평균시간 비교")

st.pyplot(fig)

# --------------------------------
# 8. 결과 해석
# --------------------------------
slowest = df.loc[df["평균시간"].idxmax()]
fastest = df.loc[df["평균시간"].idxmin()]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="평균시간이 가장 긴 지역",
        value=slowest["시군구명"],
        delta=f'{slowest["평균시간"]:.2f}분'
    )

with col2:
    st.metric(
        label="평균시간이 가장 짧은 지역",
        value=fastest["시군구명"],
        delta=f'{fastest["평균시간"]:.2f}분'
    )

st.info(
    """
    막대가 길수록 구급대의 현장 도착 이후 환자 접촉까지
    평균적으로 더 많은 시간이 소요되었음을 의미합니다.
    """
)

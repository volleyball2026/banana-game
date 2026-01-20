import streamlit as st
import random
import pandas as pd
import time

# 페이지 기본 설정
st.set_page_config(page_title="확률 시뮬레이션: 팬케이크와 바나나", layout="wide", page_icon="🎲")

st.title("🎲 확률과 직관: 시뮬레이션 실험실")
st.markdown("수학적 확률(Theoretical)과 경험적 확률(Empirical)의 관계를 탐구해 봅시다.")

# 탭 구성
tab1, tab2 = st.tabs(["🥞 블루베리 팬케이크 문제", "🍌 마지막 바나나 게임"])

# ==============================================================================
# TAB 1: 블루베리 팬케이크 시뮬레이션
# ==============================================================================
with tab1:
    st.header("Case Study 1: 블루베리 팬케이크 문제")
    st.info("""
    **상황:** 로봇 팔이 6개의 팬케이크 위에 **20개의 블루베리**를 무작위로 뿌립니다.
    
    **핵심 질문:** 블루베리가 하나도 없는 **'빈 팬케이크'**가 나올 확률은 얼마일까요?
    """)

    # 1. 설정 영역
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("⚙️ 설정")
        pancake_trials = st.number_input("시뮬레이션 횟수 (N)", min_value=10, max_value=10000, value=100, step=10, key="p_trials")
        pancake_berries = st.slider("뿌릴 블루베리 개수", 10, 50, 20, key="p_berries", help="기본 설정은 20개입니다.")
        pancake_run_btn = st.button("팬케이크 굽기 시작! 🥞", key="p_btn")

    # 2. 시뮬레이션 실행 및 결과
    if pancake_run_btn:
        empty_pancake_event = 0 # 빈 팬케이크가 발생한 횟수
        pancake_results = []

        # 진행바
        progress_bar = st.progress(0)
        
        for i in range(1, pancake_trials + 1):
            # 6개의 팬케이크 (초기화)
            plates = [0] * 6 
            
            # 블루베리 뿌리기 (독립시행)
            for _ in range(pancake_berries):
                target_plate = random.randint(0, 5) # 0~5번 접시 중 하나 선택
                plates[target_plate] += 1
            
            # 빈 팬케이크가 있는지 확인 (0이 하나라도 있으면 True)
            is_empty_exist = 0 in plates
            
            if is_empty_exist:
                empty_pancake_event += 1
            
            pancake_results.append({
                "시도": i,
                "빈 팬케이크 발생 여부": "발생" if is_empty_exist else "없음",
                "경험적 확률(누적)": empty_pancake_event / i,
                "접시 상태": plates # 나중에 샘플 확인용
            })
            
            if i % (pancake_trials // 10) == 0:
                progress_bar.progress(i / pancake_trials)
        
        progress_bar.empty()
        
        # 데이터프레임 생성
        df_pancake = pd.DataFrame(pancake_results)
        final_prob = df_pancake["경험적 확률(누적)"].iloc[-1]

        # 3. 결과 시각화
        with col2:
            st.metric(
                label=f"{pancake_trials}번 시도 후 '빈 팬케이크'가 나올 확률", 
                value=f"{final_prob*100:.1f}%",
                delta="수학적 확률은 약 21.4% (20개 기준)"
            )
            
            st.subheader("📈 시행 횟수에 따른 확률 변화 (큰 수의 법칙)")
            st.line_chart(df_pancake.set_index("시도")["경험적 확률(누적)"], color="#5DADE2")
            st.caption("시행 횟수가 늘어날수록 그래프가 특정한 값(약 21%)에 수렴하나요?")

        # 4. 상세 분석 (마지막 시도 샘플 보여주기)
        st.divider()
        st.subheader("🔍 마지막 시도 자세히 보기")
        last_plates = pancake_results[-1]["접시 상태"]
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.write("마지막 시도의 접시별 블루베리 개수:")
            chart_data = pd.DataFrame({
                "접시 번호": ["1번", "2번", "3번", "4번", "5번", "6번"],
                "블루베리 수": last_plates
            })
            st.bar_chart(chart_data.set_index("접시 번호"), color="#8E44AD")
        
        with c2:
            if 0 in last_plates:
                st.error(f"결과: 빈 팬케이크가 **{last_plates.count(0)}개** 있습니다! (이벤트 발생)")
            else:
                st.success("결과: 모든 팬케이크에 블루베리가 있습니다! (이벤트 미발생)")


# ==============================================================================
# TAB 2: 마지막 바나나 게임
# ==============================================================================
with tab2:
    st.header("Case Study 2: 마지막 바나나 게임")
    st.info("""
    **규칙:** 두 개의 주사위를 던져 **더 큰 숫자(최댓값)**를 확인합니다.
    * 최댓값이 **1, 2, 3, 4** 👉 Player A 승리
    * 최댓값이 **5, 6** 👉 Player B 승리
    
    **질문:** 숫자가 4개인 A가 유리할까요, 2개인 B가 유리할까요?
    """)

    # 1. 설정 영역
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("⚙️ 설정")
        banana_trials = st.number_input("시뮬레이션 횟수 (N)", min_value=10, max_value=10000, value=100, step=10, key="b_trials")
        banana_run_btn = st.button("게임 시작! 🍌", key="b_btn")

    # 2. 시뮬레이션 실행
    if banana_run_btn:
        results = []
        win_a_count = 0
        win_b_count = 0
        
        for i in range(1, banana_trials + 1):
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            max_val = max(dice1, dice2)
            
            winner = "B"
            if max_val <= 4:
                winner = "A"
                win_a_count += 1
            else:
                win_b_count += 1
                
            results.append({
                "시도": i,
                "A 승률(누적)": win_a_count / i,
                "B 승률(누적)": win_b_count / i
            })

        df_banana = pd.DataFrame(results)
        
        # 3. 결과 시각화
        with col2:
            m1, m2, m3 = st.columns(3)
            m1.metric("총 게임 횟수", f"{banana_trials}회")
            m2.metric("A 승리 (이론: 44.4%)", f"{win_a_count}회", f"{win_a_count/banana_trials*100:.1f}%")
            m3.metric("B 승리 (이론: 55.6%)", f"{win_b_count}회", f"{win_b_count/banana_trials*100:.1f}%")

            st.subheader("📈 승률 변화 그래프")
            st.line_chart(df_banana.set_index("시도")[["A 승률(누적)", "B 승률(누적)"]], color=["#FF9F36", "#4B4B4B"])
            st.caption("초반에는 승률이 요동치지만, 횟수가 늘어날수록 선이 평평해집니다.")

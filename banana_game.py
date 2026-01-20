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
# TAB 1: 블루베리 팬케이크 시뮬레이션 (수정됨)
# ==============================================================================
with tab1:
    st.header("Case Study 1: 블루베리 팬케이크 문제")
    st.info("""
    **알고리즘 (The Algorithm):**
    1. **로봇 팔의 1회 행동**은 **주사위 1번 던지기(1~6)**와 같습니다.
    2. 주사위 눈금과 같은 번호의 팬케이크에 블루베리를 1개 올립니다.
    3. 이 행동을 **20번 반복**합니다. (블루베리 20개)
    
    **핵심 질문:** 과연 블루베리가 하나도 없는 **'빈 팬케이크'**가 생길까요?
    """)

    # 1. 설정 영역
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("⚙️ 설정")
        pancake_trials = st.number_input("시뮬레이션 횟수 (N)", min_value=10, max_value=10000, value=100, step=10, key="p_trials")
        # 수업 상황(20개)을 기본값으로 두되, 학생이 바꿔볼 수 있게 함
        pancake_berries = st.slider("블루베리 개수 (주사위 던지는 횟수)", 10, 50, 20, key="p_berries")
        pancake_run_btn = st.button("팬케이크 굽기 시작! 🥞", key="p_btn")

    # 2. 시뮬레이션 실행 및 결과
    if pancake_run_btn:
        empty_pancake_event = 0 # 빈 팬케이크가 발생한 사건 횟수
        pancake_results = []

        # 진행바
        progress_bar = st.progress(0)
        
        for i in range(1, pancake_trials + 1):
            # 6개의 팬케이크 접시 준비 (초기화: 0개)
            # 인덱스 0~5를 사용하되, 표기할 때는 1~6번 접시로 매핑
            plates = [0] * 6 
            
            # 선생님 요청 알고리즘 적용:
            # 주사위를 'pancake_berries'번(20번) 던짐
            for _ in range(pancake_berries):
                dice_number = random.randint(1, 6) # 1~6 주사위 굴리기
                plate_index = dice_number - 1      # 리스트 인덱스는 0부터 시작하므로 -1
                plates[plate_index] += 1           # 해당 접시에 블루베리 추가
            
            # 빈 팬케이크 확인 (접시에 0이 하나라도 있으면 True)
            is_empty_exist = 0 in plates
            
            if is_empty_exist:
                empty_pancake_event += 1
            
            pancake_results.append({
                "시도": i,
                "빈 팬케이크 여부": "있음" if is_empty_exist else "없음",
                "경험적 확률(누적)": empty_pancake_event / i,
                "접시 상태": plates 
            })
            
            # 진행바 업데이트 (속도 조절을 위해 간헐적 업데이트)
            if i % (pancake_trials // 10) == 0:
                progress_bar.progress(i / pancake_trials)
        
        progress_bar.empty()
        
        # 데이터프레임 변환
        df_pancake = pd.DataFrame(pancake_results)
        final_prob = df_pancake["경험적 확률(누적)"].iloc[-1]

        # 3. 결과 시각화
        with col2:
            st.metric(
                label=f"N={pancake_trials}번 시뮬레이션 결과: '빈 팬케이크'가 발생할 확률", 
                value=f"{final_prob*100:.1f}%",
                delta="이론적 확률: 약 21.4% (블루베리 20개 기준)"
            )
            
            st.subheader("📈 시행 횟수에 따른 확률 수렴 (큰 수의 법칙)")
            st.line_chart(df_pancake.set_index("시도")["경험적 확률(누적)"], color="#5DADE2")
            
        # 4. 상세 분석 (마지막 샘플 시각화)
        st.divider()
        st.subheader("🔍 마지막 시도(Sample) 결과 확인")
        st.caption("방금 로봇이 마지막으로 만든 팬케이크 접시들의 상태입니다.")
        
        last_plates = pancake_results[-1]["접시 상태"]
        
        # 차트 데이터 생성 (X축을 1~6번 접시로 명확히 표기)
        chart_data = pd.DataFrame({
            "팬케이크 번호": ["1번", "2번", "3번", "4번", "5번", "6번"],
            "블루베리 개수": last_plates
        })
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.bar_chart(chart_data.set_index("팬케이크 번호"), color="#8E44AD")
        
        with c2:
            st.write(" **[접시별 블루베리 현황]**")
            for idx, count in enumerate(last_plates):
                msg = f"{idx+1}번 팬케이크: {count}개"
                if count == 0:
                    st.error(msg + " (빈 접시! 😲)")
                else:
                    st.text(msg)


# ==============================================================================
# TAB 2: 마지막 바나나 게임 (기존 코드 유지)
# ==============================================================================
with tab2:
    st.header("Case Study 2: 마지막 바나나 게임")
    st.info("""
    **규칙:** 두 개의 주사위를 던져 **더 큰 숫자(최댓값)**를 확인합니다.
    * 최댓값이 **1, 2, 3, 4** 👉 Player A 승리
    * 최댓값이 **5, 6** 👉 Player B 승리
    """)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("⚙️ 설정")
        banana_trials = st.number_input("시뮬레이션 횟수 (N)", min_value=10, max_value=10000, value=100, step=10, key="b_trials")
        banana_run_btn = st.button("게임 시작! 🍌", key="b_btn")

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
        
        with col2:
            m1, m2, m3 = st.columns(3)
            m1.metric("총 게임 횟수", f"{banana_trials}회")
            m2.metric("A 승리 (이론: 44.4%)", f"{win_a_count}회", f"{win_a_count/banana_trials*100:.1f}%")
            m3.metric("B 승리 (이론: 55.6%)", f"{win_b_count}회", f"{win_b_count/banana_trials*100:.1f}%")

            st.subheader("📈 승률 변화 그래프")
            st.line_chart(df_banana.set_index("시도")[["A 승률(누적)", "B 승률(누적)"]], color=["#FF9F36", "#4B4B4B"])

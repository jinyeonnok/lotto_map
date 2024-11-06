# 로또추첨.py

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import urllib.parse


from pages.functions.get_data import Lotto_class
from pages.tabs_view.tab1 import display_current_numbers 
from pages.tabs_view.tab2 import display_past_records    
from pages.tabs_view.tab3 import draw_number    





# Lotto_class의 인스턴스 생성
lotto_instance = Lotto_class()

# 전체 기록을 캐시하는 함수
@st.cache_data
def load_all_records():
    최근회차 = lotto_instance.최근회차()
    전체기록 = pd.DataFrame(lotto_instance.download_records(1, 최근회차)).transpose()
    전체기록.index = 전체기록.index.str.replace('회차', '').astype(int)
    return 전체기록

# 전체 기록을 한 번만 불러오기
전체기록 = load_all_records()
최근회차 = lotto_instance.최근회차()

st.title('이번주 당첨번호')
st.title(f'최근 회차 : {최근회차}')




# Selectbox로 메뉴 선택
selected_option = st.selectbox("메뉴 선택", ["당첨 번호", "과거 당첨 기록", "AI 로또 추첨기", "당첨 주소"])

if selected_option == "당첨 번호":
    display_current_numbers(lotto_instance, 최근회차, 전체기록)

elif selected_option == "과거 당첨 기록":
    display_past_records(lotto_instance, 최근회차)

elif selected_option == "AI 로또 추첨기":
    st.markdown(
        """
        <style>
        div.stTextInput > label { margin-top: -10px; }
        </style>
        
        <div style="line-height:1.2;">
            고정 번호를 선택하시겠습니까?<br>
            <span style="font-size: 0.9em; color: gray;">(예: 공백 또는 3, 5, 12)</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 고정 번호 입력 (숫자만 허용)
    input_numbers = st.text_input("")

    # 사용자가 몇 개의 번호를 추첨할지 입력할 수 있는 텍스트 입력 필드 추가
    num_draws = st.number_input('몇 개의 추가 번호를 뽑으시겠습니까?', min_value=1, max_value=10, value=3)

    # 생성 버튼 추가
    if st.button('번호 생성'):
        st.write("생성된 번호 :")

        # 입력한 숫자 리스트로 변환
        if input_numbers:
            # 쉼표를 기준으로 나누고, 숫자로 변환 후 리스트 생성
            picked_num = [int(num.strip()) for num in input_numbers.split(',') if num.strip().isdigit()]
        else:
            picked_num = None  # 입력이 없으면 빈 리스트
        
        draw_number(최근회차, 전체기록, picked_num, num_draws)  # 입력받은 숫자를 draw_number 함수에 전달

elif selected_option == "당첨 주소":
                
    
        
    st.title("당첨 지점")
    
      # 4개의 마커 좌표
    coordinates = [
        (37.5665, 126.978),  # 서울
        (37.567, 126.979),  # 서울2
        (37.565, 126.977),  # 서울3
        (37.564, 126.975),  # 서울4
    ]
    
    # 마커를 포함한 Google Maps Embed URL 생성
    base_url = "https://www.google.com/maps/embed/v1/view?"
    markers = []
    for lat, lon in coordinates:
        markers.append(f"markers={lat},{lon}")
    
    # 마커들을 URL에 추가
    marker_str = '&'.join(markers)
    url = f"{base_url}key=YOUR_API_KEY&{marker_str}&zoom=14"
    
    # HTML iframe 코드
    iframe_code = f"""
    <iframe src="{url}" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
    """
    
    # Streamlit에 지도 표시
    st.markdown(iframe_code, unsafe_allow_html=True)

    
        
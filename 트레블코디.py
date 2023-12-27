import streamlit as st
import requests
from bs4 import BeautifulSoup
from joblib import dump, load
import pandas as pd
import os
def main():
    loaded_model = load('model.joblib')
    st.set_page_config(layout="wide")  

    st.title("트래블 코디")

    
    col1, col3 = st.columns([2, 6])

   
    with col1:
        destination = st.text_input("여행지", "서울")
        month, day = st.columns([1,1])
        with month:
            Mon = st.text_input("Month", 1)
        with day:
            Da = st.text_input("Day", 2)
        if len(Mon)==1:
            Month = '0'+Mon
        else: Month = Mon
        if len(Da)==1:
            Day = '0'+Da
        else: Day=Da
        Date = f"2022-{Month}-{Day}"
        #st.write(f'{Date} 기준 데이터 입니다.')
        style_keyword = st.selectbox("스타일", ["추천","미니멀", "모던", "스트릿", "빈티지", "캐주얼", "러블리", "클래식"])
               
        # style_keyword = st.selectbox("CODE", ["추천","캐주얼","클래식","러블리","모던","스트릿","미니멀","힙"])
        
        
        personal_color =st.selectbox("personal color", ["warm tone","cool tone"])
    
    with col3:
        st.markdown(f"<h3>여행지: {destination}</h3>", unsafe_allow_html=True)
        st.write(f"<h5>여행 날짜: {Month}월 {Day}일</h5>", unsafe_allow_html=True)
        st.write(f"<h3>날씨 정보</h3>", unsafe_allow_html=True)

        
        if destination=='서울':
            
            new_data = pd.read_csv('s_wd.csv')
        if destination=='파리':
            
            new_data = pd.read_csv('p_wd.csv')

        
        input_date = Date
        
        selected_data = new_data[new_data['data'] == input_date]
        selected_data = selected_data[['temp', 'min_temp', 'max_temp','wind_speed']]
        
        st.write(f"""<h5>평균기온: {selected_data['temp'].values[0]}, 
        최저기온: {selected_data['min_temp'].values[0]}, 
        최고기온: {selected_data['max_temp'].values[0]}, 
        풍속: {selected_data['wind_speed'].values[0]} 입니다.</h5>""", unsafe_allow_html=True)
        st.write(f'*{Date} 기준 데이터 입니다.*')
       
        prediction = loaded_model.predict(selected_data)
        recommendation = recommend_style(style_keyword, prediction[0])
        cody=prediction[0]  # 
        cody_test='스트릿'
        st.write(f"<h3>추천 여행 스타일: {cody}</h3>", unsafe_allow_html=True)
        style_df = None
        
              
        
        
        s = cody_test
        c1 = '없음'
        c2 = '반소매'
        c3 = '치마'
    
        style_selected(s, c1, c2, c3)
        #st.write(img_list)
        z1, z2, z3 = st.columns([1, 1, 1])
        for i in range(min(len(img_list), 3)):
            with z1 if i == 0 else z2 if i == 1 else z3:
                st.image(img_list[i], caption=f"{cody_test} 스타일 {i + 1}", width=200)
            
from IPython.display import display, Image
def style_selected(style, outerwear, topwear, bottomwear):
    csv_name=f'코디맵{style}_완성.csv'
    style_df=pd.read_csv(csv_name)
    
    # 조건을 만족하는 행 선택
    selected_rows = style_df.loc[(style_df['스타일'] == style) & (style_df['외투'] == outerwear) & (style_df['상의'] == topwear) & (style_df['하의'] == bottomwear)]

    # 결과 출력
    global img_list
    img_list=[]
    #st.write(selected_rows)
    for index, row in selected_rows.iterrows():
        
        path = row['사진']
        image_path = os.path.relpath(path, "C:/Users/user/python02/빅프로젝트")
        img_list.append(image_path)
        
        
def recommend_style(style_keyword, prediction):
    if style_keyword == "추천":
        return f"트래블 코디는 {prediction[0]}입니다. "
    elif style_keyword == "로맨틱":
        return "로맨틱한 분위기의 여행을 즐기세요."
    elif style_keyword == "모던":
        return "모던하고 세련된 여행을 즐기세요."
    elif style_keyword == "어반":
        return "도시 생활을 경험하세요."
    elif style_keyword == "클래식":
        return "클래식한 여행을 즐기세요."
    else:
        return "추천 정보 없음"

if __name__ == "__main__":
    main()

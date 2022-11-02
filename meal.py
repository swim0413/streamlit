import json
import streamlit as st
import streamlit.components.v1 as components
import requests

st.set_page_config(
    #layout='wide',
    #initial_sidebar_state='collapsed',
    page_title='급식 검색',
    page_icon='🍚',
)

def openJsonFile(path):
    with open(path) as res:
        result = json.loads(res.read())
    return result

st.sidebar.subheader('급식 정보')
date = st.sidebar.date_input('날짜 선택', help='날짜선택')
school = st.sidebar.selectbox('학교 선택', openJsonFile('./schoolinfo.json').keys(), help='학교이름 적기')
trimDate = str(date).replace('-','')
st.sidebar.subheader('시간표')
col1, col2, col3, col4 = st.columns(4)
with col1:
    ay = st.sidebar.number_input('학년도', step=1, value=2022, min_value=2022, help='학년도 선택')
with col2:
    sem = st.sidebar.number_input('학기', step=1, value=1, min_value=1, max_value=2, help='학기 선택')
with col3:
    grade = st.sidebar.number_input('학년', step=1, value=1, min_value=1, max_value=3, help='학년 선택')
with col4:
    classNum = st.sidebar.number_input('반', step=1, value=1, min_value=1, help='반 선택')


def getSchoolData(schoolName):
    data = openJsonFile('./schoolinfo.json')
    sc = data[schoolName]['schoolcode']
    oc = data[schoolName]['officecode']
    return sc, oc

def getMeal(schoolCode, officeCode, date):
    try:
        KEY = '376c66873c3845a485f42bc79baa29ce'
        URL = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
        params = {'Type':'json', 'KEY':KEY, 'pIndex':'1', 'Size':'100', 'ATPT_OFCDC_SC_CODE':officeCode, 'SD_SCHUL_CODE':schoolCode, 'MLSV_YMD':date}
        data = requests.get(URL, params=params)
        data = data.json()['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        #data = str(data).replace('<br/>', '\n')
    except Exception as e:
        data = '급식정보가 없습니다'
    return data

def getSchedule(officeCode,schoolCode, ay, sem, date, grade, classNum):
    try:
        KEY = '376c66873c3845a485f42bc79baa29ce'
        URL = 'https://open.neis.go.kr/hub/hisTimetable'
        params = {'Type':'json','KEY':KEY, 'ATPT_OFCDC_SC_CODE':officeCode, 'SD_SCHUL_CODE':schoolCode, 'AY':ay, 'SEM':sem, 'ALL_TI_YMD':date,'GRADE':grade, 'CLASS_NM': classNum, 'TI_FROM_YMD': date, 'TI_TO_YMD':date }
        data = requests.get(URL, params=params)
        data = data.json()['hisTimetable'][1]['row']
        res = []
        for value in data:
            res.append(value['ITRT_CNTNT'])
    except Exception as e:
        res = '없는 시간표 입니다'
    return res

meal = getMeal(getSchoolData(school)[0], getSchoolData(school)[1], trimDate)
schedule = getSchedule(getSchoolData(school)[1], getSchoolData(school)[0], ay, sem, trimDate,grade, classNum)
schedule = '->'.join(schedule)
components.html(
    f"""
    <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
            #meal{{
                font-family: 'Jua', sans-serif;
                text-align: center;
                font-size: 30px;
                border: none;
                color: black;
                background-color: rgb(214, 230, 245);
                
                padding: 10px;
                width: fit-content;
                height: fit-content;
                border-radius: 10px;
            }}
            
            #schedule{{
                padding: 10px;
                width: fit-content;
                height: fit-content;
                border-radius: 10px;
               
                background-color: rgb(214, 230, 245);
                font-family: 'Jua', sans-serif;
                font-size: 30px;
            }}
            
            h1{{
                margin-top: 40px;
            }}
        </style>
        <body>
            <h1>{school} 급식 {date}</h1>
            <div id="meal">
                {meal}
            </div>
            <h1>{grade}학년 {classNum}반 시간표</h1>
            <div id="schedule">
                 {schedule}
            </div>
        </body>
    </html>
    """,
    height=600,
    width=1000,
)


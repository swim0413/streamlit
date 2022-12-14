import json
import streamlit as st
import streamlit.components.v1 as components
import requests

st.set_page_config(
    #layout='wide',
    #initial_sidebar_state='collapsed',
    page_title='κΈμ κ²μ',
    page_icon='π',
)

def openJsonFile(path):
    with open(path) as res:
        result = json.loads(res.read())
    return result

st.sidebar.subheader('κΈμ μ λ³΄')
date = st.sidebar.date_input('λ μ§ μ ν', help='λ μ§μ ν')
school = st.sidebar.selectbox('νκ΅ μ ν', openJsonFile('./schoolinfo.json').keys(), help='νκ΅μ΄λ¦ μ κΈ°')
trimDate = str(date).replace('-','')
st.sidebar.subheader('μκ°ν')
col1, col2, col3, col4 = st.columns(4)
with col1:
    ay = st.sidebar.number_input('νλλ', step=1, value=2022, min_value=2022, help='νλλ μ ν')
with col2:
    sem = st.sidebar.number_input('νκΈ°', step=1, value=1, min_value=1, max_value=2, help='νκΈ° μ ν')
with col3:
    grade = st.sidebar.number_input('νλ', step=1, value=1, min_value=1, max_value=3, help='νλ μ ν')
with col4:
    classNum = st.sidebar.number_input('λ°', step=1, value=1, min_value=1, help='λ° μ ν')


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
        data = 'κΈμμ λ³΄κ° μμ΅λλ€'
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
        res = 'μλ μκ°ν μλλ€'
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
                font-family: 'Jua', sans-serif;
            }}
        </style>
        <body>
            <h1>{school} κΈμ {date}</h1>
            <div id="meal">
                {meal}
            </div>
            <h1>{grade}νλ {classNum}λ° μκ°ν</h1>
            <div id="schedule">
                 {schedule}
            </div>
        </body>
    </html>
    """,
    height=600,
    width=1000,
)


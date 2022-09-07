import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox('학년',['1','2','3'])
with col2:
    group = st.selectbox('반',['1','2','3','4','5','6','7','8'])
with col3:
    number = st.number_input('번호', step=1)

선택1 = st.radio('1. 2학년 1학기 영어, 수학 과목 중 1과목 선택', ('기하', '수학과제 탐구', '영어권 문화'))
선택2 = st.radio('2. 2학년 2학기 영어, 수학 과목 중 1과목 선택', ('진로영어', '심화 수학1'))
st.write('3. 탐구 일반 과목 중 4과목 선택(학기 구분 없음)[택4]')
c1, c2 = st.columns(2)
with c1:
    세계지리 = st.checkbox('세계지리')
    세계사 = st.checkbox('세계사')
    윤리와사상 = st.checkbox('윤리와사상')
    정치와법 = st.checkbox('정치와법')
with c2:
    물리학1 = st.checkbox('물리학1')
    화학1 = st.checkbox('화학1')
    생명과학1 = st.checkbox('생명과학1')
    지구과학1 = st.checkbox('지구과학1')

st.write('4. 생활교양 과목 중 2과목 선택(학기 구분 없음)[택2]')
일본어1 = st.checkbox('일본어1')
중국어1 = st.checkbox('중국어1')
한문1 = st.checkbox('한문1')

btn = st.button('제출')

탐구일반과목 = list()
생활교양과목 = list()
if btn:
    st.write(선택1)
    st.write(선택2)
    if 세계지리:
        탐구일반과목.append('세계지리')
    if 세계사:
        탐구일반과목.append('세계사')
    if 윤리와사상:
        탐구일반과목.append('윤리와사상')
    if 정치와법:
        탐구일반과목.append('정치와법')
    if 물리학1:
        탐구일반과목.append('물리학1')
    if 화학1:
        탐구일반과목.append('화학1')
    if 생명과학1:
        탐구일반과목.append('생명과학1')
    if 지구과학1:
        탐구일반과목.append('지구과학1')

    if 일본어1:
        생활교양과목.append('일본어1')
    if 중국어1:
        생활교양과목.append('중국어1')
    if 한문1:
        생활교양과목.append('한문1')

    if len(탐구일반과목) != 4:
        st.error('탐구일반과목을 4과목을 선택해야합니다.')
    elif len(생활교양과목) !=2:
        st.error('생활교양과목을 2과목을 선택해야합니다.')
    else:
        st.success('과목선택이 완료되었습니다.')
        st.success(f'선택한 과목은 {선택1}, {선택2}, {탐구일반과목}, {생활교양과목}')

# show.py
import streamlit as st
from detail import show_details
from display_recipi import display_recipi

# 初期設定
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# テスト用
selected_allergies = ['卵', 'ピーナッツ']
recipi_name = 'ケーキ'
result = [
    {
        'title': 'イチゴケーキ',
        'image': 'https://img.cpcdn.com/recipes/7813040/894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=11756033&p=1714165191',
        'ingredients': ['卵', '砂糖', 'バター'],
        'url': 'https://cookpad.com/recipe/7813040',
    },
    {
        'title': 'いちごけーき',
        'image': 'https://img.cpcdn.com/recipes/7781284/894x1461s/9b37148a4668a565830b9514d3af1a74?u=9240495&p=1711003018',
        'ingredients': ['卵', '牛乳', 'バニラ'],
        'url': 'https://cookpad.com/recipe/7781284',
    },
]

# ページ切り替え
if st.session_state.page == 'main':
    display_recipi(selected_allergies, recipi_name, result)
elif st.session_state.page == 'details':
    show_details()

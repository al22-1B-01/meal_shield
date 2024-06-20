from pathlib import Path

import requests
import streamlit as st
from PIL import Image

from display_recipi import display_recipi
from meal_shield.env import PACKAGE_DIR

API_URL = 'https://api.cookpad.com/search/recipes'


def fetch_recipes(recipe_name, allergies: list[str]) -> list[dict[str, any]]:

    params = {'name': recipe_name, 'allergies': allergies}

    response = requests.post(API_URL, json=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"エラーが発生しました: {response.status_code}")
        return None


def search_recipe_entrypoint() -> None:

    # アレルギー品目の選択肢
    allergy_option = [
        {'name': 'たまご', 'file': 'egg.png'},
        {'name': '牛乳', 'file': 'milk.png'},
        {'name': '小麦', 'file': 'mugi.png'},
        {'name': 'そば', 'file': 'soba.png'},
        {'name': 'えび', 'file': 'ebi.png'},
        {'name': 'かに', 'file': 'kani.png'},
        {'name': '落花生', 'file': 'cashew.png'},
        {'name': 'アーモンド', 'file': 'almond.png'},
        {'name': 'あわび', 'file': 'awabi.png'},
        {'name': 'いか', 'file': 'ika.png'},
        {'name': 'いくら', 'file': 'ikura.png'},
        {'name': 'オレンジ', 'file': 'mikan.png'},
        {'name': 'カシューナッツ', 'file': 'cashew.png'},
        {'name': 'キウイフルーツ', 'file': 'kiwi.png'},
        {'name': '牛肉', 'file': 'gyuniku.png'},
        {'name': 'くるみ', 'file': 'kurumi.png'},
        {'name': 'ごま', 'file': 'goma.png'},
        {'name': 'さけ', 'file': 'sake.png'},
        {'name': 'さば', 'file': 'saba.png'},
        {'name': '大豆', 'file': 'daizu.png'},
        {'name': '鶏肉', 'file': 'toriniku.png'},
        {'name': 'バナナ', 'file': 'banana.png'},
        {'name': '豚肉', 'file': 'pig.png'},
        {'name': 'まつたけ', 'file': 'matsutake.png'},
        {'name': '桃', 'file': 'momo.png'},
        {'name': 'やまいも', 'file': 'yamaimo.png'},
        {'name': 'りんご', 'file': 'ringo.png'},
        {'name': 'ゼラチン', 'file': 'gelatine.png'},
    ]

    st.subheader('除去したい品目を選択してください')

    if 'allergy_list' not in st.session_state:
        st.session_state.allergy_list = []

    cols = st.columns(7)
    for index, item in enumerate(allergy_option):
        col = cols[index % 7]
        image = Image.open(PACKAGE_DIR / f'data/images/{item["file"]}')

        if col.button(f'{item["name"]}'):
            if item['name'] in st.session_state.allergy_list:
                st.session_state.allergy_list.remove(item['name'])
            else:
                st.session_state.allergy_list.append(item['name'])

        col.image(image, use_column_width=True, output_format='PNG')

    st.subheader('選択されたアレルギー品目')
    for allergy in st.session_state.allergy_list:
        st.markdown(
            f'<span style="background-color: black; padding: 5px;">{allergy}</span>',
            unsafe_allow_html=True,
        )

    st.subheader('レシピ検索')
    recipe_name = st.text_input('レシピ名を入力してください')

    if st.button('検索'):
        recipes = fetch_recipes(recipe_name, st.session_state.allergy_list)
        st.session_state.recipes = recipes
        st.session_state.page = '検索結果'
        st.session_state.recipe_name = recipe_name
        st.experimental_rerun()
        return st.session_state.allergy_list, recipe_name, recipes
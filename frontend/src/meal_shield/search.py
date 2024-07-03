import requests
import streamlit as st
from PIL import Image

from meal_shield.env import PACKAGE_DIR
from meal_shield.display_recipe import get_recipe_summary

base_url = 'http://localhost:8000'


def fetch_recipe_detail(recipe_name: str, allergies: list[str]) -> list:
    params = {'recipe': recipe_name, 'allergy_list': allergies}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'エラーが発生しました: {response.status_code}')
        return None


# アレルギー品目の選択肢
ALLERGY_OPTION = [
    {'name': 'えび', 'file': 'ebi.png'},
    {'name': 'かに', 'file': 'kani.png'},
    {'name': 'いか', 'file': 'ika.png'},
    {'name': '小麦', 'file': 'mugi.png'},
    {'name': 'たまご', 'file': 'egg.png'},
    {'name': '乳', 'file': 'milk.png'},
    {'name': 'アーモンド', 'file': 'almond.png'},
    {'name': '落花生', 'file': 'rakkasei.png'},
    {'name': 'そば', 'file': 'soba.png'},
    {'name': 'あわび', 'file': 'awabi.png'},
    {'name': '大豆', 'file': 'daizu.png'},
    {'name': 'くるみ', 'file': 'kurumi.png'},
    {'name': 'ごま', 'file': 'goma.png'},
    {'name': 'カシューナッツ', 'file': 'cashew.png'},
    {'name': '牛肉', 'file': 'gyuniku.png'},
    {'name': '鶏肉', 'file': 'toriniku.png'},
    {'name': '豚肉', 'file': 'pig.png'},
    {'name': 'さけ', 'file': 'sake.png'},
    {'name': 'さば', 'file': 'saba.png'},
    {'name': 'まつたけ', 'file': 'matsutake.png'},
    {'name': 'やまいも', 'file': 'yamaimo.png'},
    {'name': 'ゼラチン', 'file': 'gelatine.png'},
    {'name': 'オレンジ', 'file': 'mikan.png'},
    {'name': 'バナナ', 'file': 'banana.png'},
    {'name': 'いくら', 'file': 'ikura.png'},
    {'name': 'もも', 'file': 'momo.png'},
    {'name': 'りんご', 'file': 'ringo.png'},
    {'name': 'キウイフルーツ', 'file': 'kiwi.png'},
]


def search_recipe_entrypoint() -> None:
    st.subheader('除去したい品目を選択してください')

    if 'allergy_list' not in st.session_state:
        st.session_state.allergy_list = []

    cols = st.columns(7)
    for index, item in enumerate(ALLERGY_OPTION):
        st.markdown(
            """
            <style>
            .stButton button {
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        col = cols[index % 7]
        image = Image.open(PACKAGE_DIR / f'data/images/{item["file"]}')

        if col.button(item['name']):
            if item['name'] in st.session_state.allergy_list:
                st.session_state.allergy_list.remove(item['name'])
            else:
                st.session_state.allergy_list.append(item['name'])

        col.image(image, use_column_width=True, width=100)

    st.subheader('選択されたアレルギー品目')
    for allergy in st.session_state.allergy_list:
        st.markdown(
            f'<span style="background-color: red;padding: 5px;font-size: 14px;'
            f'">'
            f'{allergy}'
            f'</span>',
            unsafe_allow_html=True,
        )

    st.subheader('レシピ検索')
    recipe_name = st.text_input('レシピ名を入力してください')

    if st.button('検索'):
        if not st.session_state.allergy_list:
            st.session_state.page = ''
            st.error('アレルギー品目が入力されていません.')

        else:
            recipes = fetch_recipe_detail(recipe_name, st.session_state.allergy_list)
            st.session_state.recipes = recipes
            st.session_state.page = '検索結果'
            st.session_state.recipe_name = recipe_name
            st.rerun()
            return st.session_state.allergy_list, recipe_name, recipes


def validate_input_data(recipe_name: str, allergies_list: list[str]) -> None:
    if not allergies_list:
        st.error('アレルギー品目が入力されていません.')
        # search_recipe_entrypoint()
    if not recipe_name:
        st.error('レシピが入力されていません.')
        # search_recipe_entrypoint()
    if not st.session_state.recipes:
        st.error('検索結果が存在しません.')
        # search_recipe_entrypoint()
    get_recipe_summary(
        allergy_list=st.session_state.allergy_list,
        recipe_name=st.session_state.recipe_name,
        recipes=st.session_state.recipes,
    )

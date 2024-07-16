import time
from typing import Final

import requests
import streamlit as st

BASE_URL: Final[str] = 'http://backend:8000'


BASE_IMAGE_URL: Final[
    str
] = 'https://raw.githubusercontent.com/al22-1B-01/meal_shield/main/frontend/data/images/'
# アレルギー品目の選択肢
_ALLERGY_OPTION: Final[list[dict[str, str]]] = [
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
    {'name': '牛', 'file': 'gyuniku.png'},
    {'name': '鶏', 'file': 'toriniku.png'},
    {'name': '豚', 'file': 'pig.png'},
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
ALLERGY_OPTION: Final[list[dict[str, str]]] = [
    {'name': item['name'], 'file': BASE_IMAGE_URL + item['file']}
    for item in _ALLERGY_OPTION
]


def fetch_recipe_detail(recipe_name: str, allergies: list[str]) -> list:
    """
    指定されたレシピ名とアレルギーリストに基づいてレシピの詳細を取得します。

    :param str recipe_name: 検索するレシピの名前
    :param list[str] allergies: 除去したいアレルギー品目のリスト
    :return: レシピの詳細を含む辞書のリスト。エラーが発生した場合はNoneを返します。
    :rtype: Optional[list]
    :raises requests.exceptions.RequestException: リクエスト中にエラーが発生した場合
    """
    params = {'recipe': recipe_name, 'allergy_list': allergies}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        # st.error(f'エラーが発生しました: {response.status_code}')
        return None


def search_recipe_entrypoint() -> None:
    """
    ユーザーにアレルギー品目を選択させ、レシピ名を入力させるためのエントリーポイントを提供します。

    この関数は、各アレルギー品目のチェックボックスとレシピ名の入力フィールドを表示します。
    検索ボタンがクリックされると、選択されたアレルギー品目とレシピ名をセッション状態に保存します。
    """
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

        if col.button(item['name']):
            if item['name'] in st.session_state.allergy_list:
                st.session_state.allergy_list.remove(item['name'])
            else:
                st.session_state.allergy_list.append(item['name'])

        col.image(item['file'], use_column_width=True, width=100)

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
        st.session_state.page = '検索結果'
        st.session_state.recipe_name = recipe_name
        st.rerun()


def validate_input_data(recipe_name: str, allergies_list: list[str]) -> None:
    """
    入力データ（レシピ名とアレルギーリスト）を検証し、不正なデータがある場合にエラーメッセージを表示してリセットします。

    :param str recipe_name: 検索するレシピの名前
    :param list[str] allergies_list: 除去したいアレルギー品目のリスト
    :return: None
    :raises ValueError: アレルギー品目リストまたはレシピ名が空の場合
    """

    def show_error_and_reset_session(error_message: str):
        """
        エラーメッセージを表示し、セッションをリセットします。

        :param str error_message: 表示するエラーメッセージ
        :return: None
        """
        st.error(error_message)
        del st.session_state.page
        time.sleep(3)
        st.rerun()

    # Check if allergies list or recipe name is empty
    if not allergies_list:
        show_error_and_reset_session('アレルギー品目が入力されていません.')
    elif not recipe_name:
        show_error_and_reset_session('レシピが入力されていません.')

    if (
        not st.session_state.get('recipes')
        or not st.session_state.recipes
        or st.session_state.recipes[0].get('status') == 'error'
    ):
        recipes = fetch_recipe_detail(recipe_name, st.session_state.allergy_list)
        st.session_state.recipes = recipes

        # 再度チェックを行う前に、recipesがNoneでないか、かつ空でないかを確認する
        if (
            not st.session_state.recipes
            or st.session_state.recipes[0].get('status') == 'error'
        ):
            show_error_and_reset_session('検索結果が存在しません.')
            del st.session_state.recipes

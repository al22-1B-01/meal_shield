import streamlit as st

from meal_shield.detail import display_recipe_detail_entrypoint
from meal_shield.display_recipe import get_recipe_summary
from meal_shield.search import search_recipe_entrypoint, validate_input_data

# インポートしたモジュールの説明
# display_recipe_detail_entrypoint: レシピの詳細を表示する関数
# get_recipe_summary: レシピの概要を表示する関数
# search_recipe_entrypoint: ユーザーにアレルギー品目とレシピ名を入力させる関数
# validate_input_data: 入力されたレシピ名とアレルギー品目を検証する関数


def app() -> None:
    """
    Streamlitアプリケーションのエントリーポイント。

    この関数は、アプリケーションの現在の状態に応じて異なるページを表示します。
    初期状態ではレシピ検索ページを表示し、検索結果が存在する場合は結果の概要を表示します。
    詳細ページが要求された場合は、レシピの詳細を表示します。
    """
    if 'page' not in st.session_state:
        search_recipe_entrypoint()

    elif st.session_state.page == '検索結果':
        validate_input_data(
            recipe_name=st.session_state.recipe_name,
            allergies_list=st.session_state.allergy_list,
        )
        get_recipe_summary(
            allergy_list=st.session_state.allergy_list,
            recipe_name=st.session_state.recipe_name,
            recipes=st.session_state.recipes,
        )
    elif st.session_state.page == 'details':
        display_recipe_detail_entrypoint()


if __name__ == '__main__':
    app()

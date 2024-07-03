import streamlit as st

from meal_shield.detail import display_recipe_detail_entrypoint
from meal_shield.display_recipe import display_recipe


def main():
    # 初期設定
    if 'page' not in st.session_state:
        st.session_state.page = '検索結果'
    if 'selected_item' not in st.session_state:
        st.session_state.selected_item = None

    # テスト用データ
    selected_allergies = ['卵', 'ピーナッツ']
    recipe_name = 'ケーキ'
    result = [
        {
            'recipe_title': 'イチゴケーキ',
            'recipe_image_url': 'https://img.cpcdn.com/recipes/7813040/'
            '894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=117'
            '56033&p=1714165191',
            'recipe_ingredients': ['卵', '砂糖', 'バター'],
            'recipe_url': 'https://cookpad.com/recipe/7813040',
        },
        {
            'recipe_title': 'いちごけーき',
            'recipe_image_url': 'https://img.cpcdn.com/recipes/7781284/'
            '894x1461s/9b37148a4668a565830b9514d3af1a74?u=9240495'
            '&p=1711003018',
            'recipe_ingredients': ['卵', '牛乳', 'バニラ'],
            'recipe_url': 'https://cookpad.com/recipe/7781284',
        },
    ]

    # ページ切り替え
    if st.session_state.page == '検索結果':
        display_recipe(selected_allergies, recipe_name, result)
    elif st.session_state.page == 'details':
        display_recipe_detail_entrypoint()


if __name__ == '__main__':
    main()

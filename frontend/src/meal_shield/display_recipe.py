"""概要

説明
ランク付けされたレシピを表示する
関数get_recipe_summaryでレシピの取得と表示する
関数make_recipe_summaryでレシピ表示時に必要な情報作成
    
"""
from typing import Union

import streamlit as st


def get_recipe_summary(
    allergy_list: list[str],
    recipe_name: str,
    recipes: list[dict[str, Union[str, list[str]]]],
) -> None:
    """概要

    説明

    param:allergy_list:前頁で選択されたアレルギー
    type:allergy_list:list[str]:
    param:recipe_name;入力されたレシピ名
    type:recipe_name:str
    param:recipes:除外されたレシピが順位にソート
    type:recipes:list[dict[str, Union[str, list[str]]]]
    return:None

    """
    st.title('選択されたアレルギー品目')
    selected_list = ', '.join(allergy_list)

    box_style = """
    <div
    style='border: 1px solid #ddd; padding:
    10px; border-radius: 5px; background-color: #f9f9f9;'
    >
    {content}
    </div>
    """
    st.markdown(box_style.format(content=selected_list), unsafe_allow_html=True)
    st.title('料理名')
    st.markdown(box_style.format(content=recipe_name), unsafe_allow_html=True)
    button_css = """
    <style>
    dic.stButton > button:first-child  {{
        front.weight : bold;
        width : 800px;
        height : 50px;
    }}
    </style>
    """
    for idex, item in enumerate(recipes):
        new_recipe, recipe_img_url = make_recipe_summary(
            allergy_list, recipe_name, item
        )
        button_key = f'{recipe_name}_{idex}'
        st.write(f"{idex + 1}位  {new_recipe['recipe_title']}")
        st.markdown(button_css, unsafe_allow_html=True)
        st.image(recipe_img_url, width=300)

        if st.button(f"{new_recipe['recipe_title']}", key=button_key):
            st.session_state.page = 'details'
            st.session_state.selected_item = new_recipe
            st.rerun()  # ページをリロードして変更を反映


def make_recipe_summary(
    allergy_list: list[str],
    recipe_name: str,
    recipes: dict[str, Union[str, list[str]]],
) -> tuple[dict[str, Union[str, list[str]]], str]:
    """概要

    説明

    param:allergy_list:前ページで選択されたアレルギー
    type:allergy_list:list[str]:
    param:recipe_name;入力されたレシピ名
    type:recipe_name:str
    param:recipes:除外されたレシピ
    type:recipes:dict[str, Union[str, list[str]]]
    return:tuple[dict[str, Union[str, list[str]]], str]:

    """

    recipe_img_url = recipes.get('recipe_image_url')
    search_result = recipes
    search_result['allergy_list'] = [allergy_list]
    return recipes, recipe_img_url

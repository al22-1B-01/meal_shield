from typing import Union

import streamlit as st


def display_recipi(
    allergy_list: list[str],
    recipe_name: str,
    recipes: list[dict[str, Union[str, list[str]]]],
) -> None:
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
        button_key = f'{recipe_name}_{idex}'
        st.write(f"{idex + 1}位  {item['recipe_title']}")
        st.markdown(button_css, unsafe_allow_html=True)
        st.image(item['recipe_image_url'], width=300)

        if st.button(f"{item['recipe_title']}", key=button_key):
            st.session_state.page = 'details'
            st.session_state.selected_item = item
            st.rerun()  # ページをリロードして変更を反映

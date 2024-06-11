# dd.py
from typing import Union

import streamlit as st
from PIL import Image


def display_recipi(
    selected_allergies: list[str],
    recipi_name: str,
    result: list[dict[str, Union[str, list[str]]]],
):
    st.title("選択されたアレルギー品目")
    allergy_list = ",".join(selected_allergies)

    box_style = """
    <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">
    {content}
    </div>
    """

    st.markdown(box_style.format(content=allergy_list), unsafe_allow_html=True)
    st.markdown(box_style.format(content=recipi_name), unsafe_allow_html=True)

    button_css = f"""
    <style>
    dic.stButton > button:first-child  {{
        front.weight : bold;
        width : 800px;
        height : 50px;
    }}
    </style>
    """

    for idex, item in enumerate(result):
        st.write(f"{idex + 1}位")
        st.markdown(button_css, unsafe_allow_html=True)
        # st.image(item["image"], width=300)

        if st.button(f"{item['title']}の詳細を見る", item["image"], width=300):
            st.session_state.page = "details"
            st.session_state.selected_item = item
            st.experimental_rerun()  # ページをリロードして変更を反映

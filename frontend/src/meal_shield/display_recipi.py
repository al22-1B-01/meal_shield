import requests
import streamlit as st

# from typing import Union


def display_recipi(
    selected_allergies: list[str],
    recipi_name: str,
    # result: list[dict[str, Union[str, list[str]]]],
    backend_url: str = "http://localhost:8000",
) -> None:
    st.title('選択されたアレルギー品目')
    allergy_list = ', '.join(selected_allergies)

    box_style = '''
    <div style='border: 1px solid #ddd; padding:
    10px; border-radius: 5px; background-color: #f9f9f9;'>
    {content}
    </div>
    '''

    st.markdown(box_style.format(content=allergy_list), unsafe_allow_html=True)
    st.title('料理名')
    st.markdown(box_style.format(content=recipi_name), unsafe_allow_html=True)

    response = requests.get(
        backend_url, params={'recipi': recipi_name, 'allergy_list': selected_allergies}
    )

    if response.status_code == 200:
        result = response.json().get('data', [])
    else:
        st.error('データの取得に失敗しました')
        return

    button_css = '''
    <style>
    dic.stButton > button:first-child  {{
        front.weight : bold;
        width : 800px;
        height : 50px;
    }}
    </style>
    '''

    for idex, item in enumerate(result):
        st.write(f"{idex + 1}位  {item['title']}")
        st.markdown(button_css, unsafe_allow_html=True)
        st.image(item['image'], width=300)

        if st.button(f"{item['title']}"):
            st.session_state.page = 'details'
            st.session_state.selected_item = item
            st.experimental_rerun()  # ページをリロードして変更を反映

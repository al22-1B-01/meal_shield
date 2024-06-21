import streamlit as st
from detail import show_details
from display_recipi import display_recipi
from search import search_recipe_entrypoint


def main():
    if 'page' not in st.session_state:
        search_recipe_entrypoint()

    elif st.session_state.page == '検索結果':
        if st.session_state.recipes:
            display_recipi(
                st.session_state.allergy_list,
                st.session_state.recipe_name,
                st.session_state.recipes,
            )
        else:
            st.write("レシピが見つかりませんでした。")

    elif st.session_state.page == 'details':
        show_details()


if __name__ == "__main__":
    main()

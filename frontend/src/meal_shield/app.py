import streamlit as st

from meal_shield.detail import show_details
from meal_shield.display_recipe import display_recipe
from meal_shield.search import search_recipe_entrypoint, validate_input_data



def main():
    if 'page' not in st.session_state:
        search_recipe_entrypoint()

    elif st.session_state.page == '検索結果':
        validate_input_data(
            recipe_name=st.session_state.recipe_name,
            allergies_list=st.session_state.allergy_list,
        )
        display_recipe(
            allergy_list=st.session_state.allergy_list,
            recipe_name=st.session_state.recipe_name,
            recipes=st.session_state.recipes,
        )


    elif st.session_state.page == 'details':
        display_recipe_detail_entrypoint()


if __name__ == '__main__':
    main()

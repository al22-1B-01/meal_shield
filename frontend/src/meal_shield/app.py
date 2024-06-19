import streamlit as st
from search import search_recipe_entrypoint
from detail import show_details

def main():
    if 'page' not in st.session_state:
        search_recipe_entrypoint()
    
    
    #elif st.session_state.page == '検索':
        #display_recipi()



    elif st.session_state.page == '検索結果':
        display_recipi()
    elif st.session_state.page == 'details':
        show_details()

if __name__ == "__main__":
    main()
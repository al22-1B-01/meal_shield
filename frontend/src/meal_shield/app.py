from search import search_recipe_entrypoint

def main():
    if 'page' not in st.session_state:
        st.session_state.page = '検索'

    if st.session_state.page == '検索':
        search_recipe_entrypoint()
    elif st.session_state.page == '検索結果':
        show_search_results()
    elif st.session_state.page == '詳細':
        show_details()

if __name__ == "__main__":
    main()
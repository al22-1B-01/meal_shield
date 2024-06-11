import streamlit as st


def show_details() -> None:
    selected_item = st.session_state.selected_item
    if selected_item:
        st.image(selected_item['image'], width=300)
        st.title(f"{selected_item['title']}の詳細表示")
        st.write(f"レシピ名: {selected_item['title']}")
        st.write(f"材料: {', '.join(selected_item['ingredients'])}")
        st.write(f"url: [レシピリンク]({selected_item['url']})")
        if st.button('検索結果画面に戻る'):
            st.session_state.page = 'main'
            st.experimental_rerun()  # ページをリロードして変更を反映
    else:
        st.write('詳細を表示するレシピが選択されていません。')
        if st.button('検索結果画面に戻る'):
            st.session_state.page = 'main'
            st.experimental_rerun()  # ページをリロードして変更を反映

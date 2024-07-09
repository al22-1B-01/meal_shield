import streamlit as st


def display_recipe_detail_entrypoint() -> None:
    
    """概要
    引数なし
    返り値:None
    recipe_image_url:画像の表示
    recipi_titile:クックパッドのレシピ名
    recipi_url:クックパッドへのリンク
    詳細がない場合は”詳細を表示するレシピが選択されていません”を表示
    """
    
    selected_item = st.session_state.selected_item
    if selected_item:
        st.image(selected_item['recipe_image_url'], width=300)
        st.write(
            f"### [{selected_item['recipe_title']}]({selected_item['recipe_url']})"
        )
        st.write(f"材料: {', '.join(selected_item['recipe_ingredients'])}")
        if st.button('検索結果画面に戻る'):
            st.session_state.page = '検索結果'
            st.rerun()  # ページをリロードして変更を反映
    else:
        st.write('詳細を表示するレシピが選択されていません。')
        if st.button('検索結果画面に戻る'):
            st.session_state.page = '検索結果'
            st.rerun()  # ページをリロードして変更を反映

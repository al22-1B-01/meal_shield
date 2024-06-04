import streamlit as st
import requests

#変更
from PIL import Image



def fetch_recipes(recipe_name, allergies):
    # APIエンドポイントとパラメータを設定します（仮のURLです）
    api_url = "https://api.example.com/recipes"
    params = {
        "name": recipe_name,
        "allergies": ",".join(allergies)
    }
    
    # APIリクエストを送信します
    response = requests.get(api_url, params=params)
    
    # レスポンスをJSON形式で解析します
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return []

def search_recipe_entrypoint():
    st.title("レシピ検索アプリ")

    # アレルギー品目の選択肢
    allergies_list = [
        "たまご", "牛乳", "小麦", "そば", "えび", "かに", "落花生", "アーモンド", 
        "あわび", "いか", "いくら", "オレンジ", "カシューナッツ", "キウイフルーツ",
        "牛肉", "くるみ", "ごま", "さけ", "さば", "大豆", "鶏肉", "バナナ", 
        "豚肉", "まつたけ", "桃", "やまいも", "りんご", "ゼラチン"
    ]

    st.subheader("除去したい品目を選択してください")
    selected_allergies = st.multiselect("", allergies_list)
    
    # 選択されたアレルギー品目の表示
    #st.write("選択されたアレルギー品目:", selected_allergies)

    st.subheader("レシピ検索")
    # ユーザーからレシピ名を入力として受け取ります
    recipe_name = st.text_input("レシピ名を入力してください")

    if st.button("検索"):
        recipes = fetch_recipes(recipe_name, selected_allergies)
        
        if recipes:
            st.success(f"検索結果: {len(recipes)}件のレシピが見つかりました")
            
            for recipe in recipes:
                with st.expander(recipe['name']):
                    st.write(f"名前: {recipe['name']}")
                    st.write(f"材料: {recipe['ingredients']}")
                    st.write(f"手順: {recipe['instructions']}")
        else:
            st.warning("レシピが見つかりませんでした")

def display_recipe():
    recipes = st.session_state.get('recipes', [])
    st.title("レシピ検索結果")
    
    if recipes:
        for recipe in recipes:
            with st.expander(recipe['name']):
                st.write(f"名前: {recipe['name']}")
                st.write(f"材料: {recipe['ingredients']}")
                st.write(f"手順: {recipe['instructions']}")
    else:
        st.warning("検索結果が見つかりませんでした")

def display_recipe_detail(recipe_name):
    st.title("レシピ詳細")
    
    recipes = st.session_state.get('recipes', [])
    recipe = next((r for r in recipes if r['name'] == recipe_name), None)
    
    if recipe:
        st.write(f"名前: {recipe['name']}")
        st.write(f"材料: {recipe['ingredients']}")
        st.write(f"手順: {recipe['instructions']}")
        st.image(recipe['image_url'])
        st.markdown(f"[クックパッドのページ]({recipe['url']})")
    else:
        st.warning("レシピが見つかりませんでした")

def main():
    st.sidebar.title("メニュー")
    page = st.sidebar.selectbox("ページを選択", ["レシピ検索", "検索結果", "レシピ詳細"])

    if page == "レシピ検索":
        search_recipe_entrypoint()
    elif page == "検索結果":
        display_recipe()
    elif page == "レシピ詳細":
        recipe_name = st.sidebar.text_input("レシピ名を入力してください")
        if recipe_name:
            display_recipe_detail(recipe_name)

if __name__ == "__main__":
    main()



import streamlit as st
import requests
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
        {"name": "たまご", "file": "egg.png"},
        {"name": "牛乳", "file": "milk.png"},
        {"name": "小麦", "file": "mugi.png"},
        {"name": "そば", "file": "soba.png"},
        {"name": "えび", "file": "ebi.png"},
        {"name": "かに", "file": "kani.png"},
        {"name": "落花生", "file": "cashew.png"},
        {"name": "アーモンド", "file": "almond.png"},
        {"name": "あわび", "file": "awabi.png"},
        {"name": "いか", "file": "ika.png"},
        {"name": "いくら", "file": "ikura.png"},
        {"name": "オレンジ", "file": "mikan.png"},
        {"name": "カシューナッツ", "file": "cashew.png"},
        {"name": "キウイフルーツ", "file": "kiwi.png"},
        {"name": "牛肉", "file": "gyuniku.png"},
        {"name": "くるみ", "file": "kurumi.png"},
        {"name": "ごま", "file": "goma.png"},
        {"name": "さけ", "file": "sake.png"},
        {"name": "さば", "file": "saba.png"},
        {"name": "大豆", "file": "daizu.png"},
        {"name": "鶏肉", "file": "toriniku.png"},
        {"name": "バナナ", "file": "banana.png"},
        {"name": "豚肉", "file": "pig.png"},
        {"name": "まつたけ", "file": "matsutake.png"},
        {"name": "桃", "file": "momo.png"},
        {"name": "やまいも", "file": "yamaimo.png"},
        {"name": "りんご", "file": "ringo.png"},
        {"name": "ゼラチン", "file": "gelatine.png"}
    ]


    st.subheader("除去したい品目を選択してください")
    selected_allergies = []
    
    # 選択されたアレルギー品目の表示
    #st.write("選択されたアレルギー品目:", selected_allergies)
#########################################
    cols = st.columns(7)
    for index, item in enumerate(allergies_list):
        col = cols[index % 7]
        image = Image.open(f"images/{item['file']}")
        if col.button("", key=item['name']):
            if item['name'] in st.session_state:
                st.session_state.pop(item['name'])
            else:
                st.session_state[item['name']] = True
        
        if item['name'] in st.session_state:
            col.image(image, caption=item['name'], use_column_width=True, output_format='PNG')
            selected_allergies.append(item['name'])
        else:
            col.image(image, caption=item['name'], use_column_width=True, output_format='PNG')

#########################################  


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

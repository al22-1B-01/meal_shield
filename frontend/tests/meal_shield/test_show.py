# # test_detail.py
# import sys
# import os

# # プロジェクトのルートディレクトリをsys.pathに追加
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
# if project_root not in sys.path:
#     sys.path.append(project_root)

# from streamlit.testing.v1 import AppTest
# import streamlit as st
# from typing import Union
# from meal_shield.display_recipe import display_recipe


# def test_display_recipe():

#     # テストデータの準備
#     selected_allergies = ['卵', '乳製品']
#     recipe_name = 'ケーキ'
#     result = [
#         {
#             'title': 'イチゴケーキ',
#             'image': 'https://img.cpcdn.com/recipes/7813040/'
#             '894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=117'
#             '56033&p=1714165191',
#             'ingredients': ['卵', '砂糖', 'バター'],
#             'url': 'https://cookpad.com/recipe/7813040',
#         },
#         {
#             'title': 'いちごけーき',
#             'image': 'https://img.cpcdn.com/recipes/7781284/'
#             '894x1461s/9b37148a4668a565830b9514d3af1a74?u=9240495'
#             '&p=1711003018',
#             'ingredients': ['卵', '牛乳', 'バニラ'],
#             'url': 'https://cookpad.com/recipe/7781284',
#         },
#     ]

#     # Streamlit AppTestをセットアップ
#     at = AppTest.from_function(
#         display_recipe,
#         selected_allergies=selected_allergies,
#         recipe_name=recipe_name,
#         result=result,
#     )

#     # テストを実行して検証
#     result = at.run()

#     # エラーメッセージが発生していないことを確認
#     assert not result.exception, f"Exception occurred: {result.exception}"

#     # アレルギーリストが正しく表示されていることを確認
#     assert "卵, 乳製品" in result.html, "Selected allergies not displayed correctly"

#     # レシピ名が正しく表示されていることを確認
#     assert "オムレツ" in result.html, "Recipe name not displayed correctly"

#     # レシピのタイトルが正しく表示されていることを確認
#     for item in result:
#         assert (
#             item['title'] in result.html
#         ), f"Recipe title '{item['title']}' not displayed correctly"

#     # 画像が正しく表示されていることを確認
#     for item in result:
#         assert (
#             item['image'] in result.html
#         ), f"Image '{item['image']}' not displayed correctly"


# if __name__ == "__main__":
#     test_display_recipe()

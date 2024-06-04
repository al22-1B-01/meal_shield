from logging import getLogger       # add (0.1->0.2): loggingパッケージのimport
logger = getLogger(__name__)        # add (0.1->0.2):


###################################################################################################
# 指定されたアレルギー品目とレシピのリストを取得する関数
###################################################################################################
from typing import Union        # fix (0.1->0.2): List, Dictはpython3.9以降だとtypingからimportせずに
                                # 小文字でそのまま扱う

def get_allergies_and_recipes(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str]]]]
) -> (list[str], list[dict[str, Union[str, list[str]]]]):
    """
    指定されたアレルギー品目とレシピのリストを取得する関数。
    
    :param allergies_list: アレルギー品目のデータを持つリスト
    :param excluded_recipes_list: レシピのデータを持ったリスト
    :return: アレルギー品目リストとレシピデータリストのタプル
    """

    # ここでC5から指定されたアレルギー品目とレシピのリストを受け取る

    return allergies_list, excluded_recipes_list


# fix(0.1->0.2): 使用例は関数のテスト用なのでコメントアウト
##################################################
# 使用例
##################################################
# allergies = ["Peanuts", "Gluten", "Dairy"]
# recipes = [
#     {
#         "recipe_title": "Peanut Butter Cookies",
#         "recipe_ingredients": ["Peanut Butter", "Sugar", "Eggs"],
#         "recipe_url": "http://example.com/peanut_butter_cookies",
#         "recipe_image_url": "http://example.com/images/peanut_butter_cookies.jpg"
#     },
#     {
#         "recipe_title": "Gluten-Free Bread",
#         "recipe_ingredients": ["Gluten-Free Flour", "Water", "Yeast"],
#         "recipe_url": "http://example.com/gluten_free_bread",
#         "recipe_image_url": "http://example.com/images/gluten_free_bread.jpg"
#     }
# ]

# allergies_list, excluded_recipes_list = get_allergies_and_recipes(allergies, recipes)
# logger.debug(allergies_list)
# logger.debug(excluded_recipes_list)
##################################################
# 使用例：ここまで
##################################################

####################################################################################################
# 指定されたアレルギー品目とレシピのリストを取得する関数：ここまで
####################################################################################################



###################################################################################################
# 各レシピに対してスコアリングを行う関数
###################################################################################################
# fix (0.1->0.2): https://weel.co.jp/media/tech/text-embedding-3/ を参考にして作り直し
import os
os.environ["OPENAI_API_KEY"] = "Your OpenAPI Key"

from openai import OpenAI
client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


text = "porcine pals"
len(get_embedding(text))
get_embedding(text)


import numpy as np

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity

# 例として2つのベクトルを定義
# vector1 = np.array(get_embedding("文章1"))
# vector2 = np.array(get_embedding("文章2"))

# コサイン類似度の計算
# similarity = cosine_similarity(vector1, vector2)
# print(f"コサイン類似度: {similarity}")
# fix: ここまで


# fix (0.1->0.2): 出力の型がない
def score_allergens(recipes, allergens, model_name="text-embedding-3-small"
) -> (float):
    allergen_embeddings = get_embeddings(allergens, model_name)
    scores = {}

    for recipe in recipes:
        recipe_title = recipe['recipe_title']
        ingredients = recipe['recipe_ingredients']
        ingredient_embeddings = get_embeddings(ingredients, model_name)
        max_scores = []

        for allergen_embedding in allergen_embeddings:
            similarity_scores = cosine_similarity(ingredient_embeddings, [allergen_embedding])
            max_score = np.max(similarity_scores)
            max_scores.append(max_score)

        scores[recipe_title] = max_scores

    return scores


# fix(0.1->0.2): 使用例は関数のテスト用なのでコメントアウト
##################################################
# 例の使用方法
##################################################
# recipes = [
#     {
#         "recipe_title": "レシピ1",
#         "recipe_ingredients": ["ミルク", "卵", "小麦粉"],
#         "recipe_url": "http://example.com/recipe1",
#         "recipe_image_url": "http://example.com/recipe1.jpg"
#     },
#     {
#         "recipe_title": "レシピ2",
#         "recipe_ingredients": ["ピーナッツ", "砂糖", "バター"],
#         "recipe_url": "http://example.com/recipe2",
#         "recipe_image_url": "http://example.com/recipe2.jpg"
#     },
#     {
#         "recipe_title": "レシピ3",
#         "recipe_ingredients": ["大豆", "小麦", "鶏肉"],
#         "recipe_url": "http://example.com/recipe3",
#         "recipe_image_url": "http://example.com/recipe3.jpg"
#     }
# ]

# allergens = ["ミルク", "ピーナッツ", "大豆"]

# scores = score_allergens(recipes, allergens)
# logger.debug(scores)
##################################################
# 使用例：ここまで
##################################################

####################################################################################################
# 各レシピに対してスコアリングを行う関数：ここまで
####################################################################################################



####################################################################################################
# スコアリング結果に基づいてソートを行う関数
####################################################################################################
# fix (0.1->0.2): 出力の型がない
def sort_recipes_by_allergy_score(scores
) -> (list[str], list[dict[str, Union[str, list[str]]]]):
    # 各レシピのスコアを合計して、(レシピタイトル, 合計スコア)のリストを作成
    total_scores = [(recipe_title, sum(allergen_scores)) for recipe_title, allergen_scores in scores.items()]
    
    # 合計スコアでソート（スコアが高い順）
    sorted_recipes = sorted(total_scores, key=lambda x: x[1], reverse=True)
    
    return sorted_recipes


# fix(0.1->0.2): 使用例は関数のテスト用なのでコメントアウト
##################################################
# スコアリング結果の例
##################################################
# scores = {
#     "レシピ1": [0.8, 0.2, 0.1],
#     "レシピ2": [0.3, 0.9, 0.4],
#     "レシピ3": [0.1, 0.3, 0.8]
# }

# sorted_recipes = sort_recipes_by_allergy_score(scores)
# logger.debug(sorted_recipes)
##################################################
# スコアリング結果の例：ここまで
##################################################



####################################################################################################
# メイン関数：上の各関数を呼び出す
####################################################################################################
def main():
    # アレルギー品目とレシピデータの取得
    # 正式実装の際は、get_allergies_and_recipes関数内でC5から受け取る
    # allergies_list, excluded_recipes_list = get_allergies_and_recipes(allergies, recipes)
    allergies_list = ["ミルク", "ピーナッツ", "大豆"]
    excluded_recipes_list = [
        {
            "recipe_title": "レシピ1",
            "recipe_ingredients": ["ミルク", "卵", "小麦粉"],
            "recipe_url": "http://example.com/recipe1",
            "recipe_image_url": "http://example.com/recipe1.jpg"
        },
        {
            "recipe_title": "レシピ2",
            "recipe_ingredients": ["ピーナッツ", "砂糖", "バター"],
            "recipe_url": "http://example.com/recipe2",
            "recipe_image_url": "http://example.com/recipe2.jpg"
        },
        {
            "recipe_title": "レシピ3",
            "recipe_ingredients": ["大豆", "小麦", "鶏肉"],
            "recipe_url": "http://example.com/recipe3",
            "recipe_image_url": "http://example.com/recipe3.jpg"
        }
    ]

    # スコアリング関数の呼び出し
    scores = score_allergens(excluded_recipes_list, allergies_list)

    # スコアリング結果のソート
    sorted_recipes = sort_recipes_by_allergy_score(scores)

    # ソート結果の表示
    for recipe_title, total_score in sorted_recipes:
        logger.info(f"レシピ名: {recipe_title}, アレルギースコア合計: {total_score}")

if __name__ == "__main__":
    main()


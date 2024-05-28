from typing import List, Dict, Union

def get_allergies_and_recipes(
    allergies_list: List[str],
    excluded_recipes_list: List[Dict[str, Union[str, List[str]]]]
) -> (List[str], List[Dict[str, Union[str, List[str]]]]):
    """
    指定されたアレルギー品目とレシピのリストを取得する関数。
    
    :param allergies_list: アレルギー品目のデータを持つリスト
    :param excluded_recipes_list: レシピのデータを持ったリスト
    :return: アレルギー品目リストとレシピデータリストのタプル
    """
    return allergies_list, excluded_recipes_list

# 使用例
allergies = ["Peanuts", "Gluten", "Dairy"]
recipes = [
    {
        "recipe_title": "Peanut Butter Cookies",
        "recipe_ingredients": ["Peanut Butter", "Sugar", "Eggs"],
        "recipe_url": "http://example.com/peanut_butter_cookies",
        "recipe_image_url": "http://example.com/images/peanut_butter_cookies.jpg"
    },
    {
        "recipe_title": "Gluten-Free Bread",
        "recipe_ingredients": ["Gluten-Free Flour", "Water", "Yeast"],
        "recipe_url": "http://example.com/gluten_free_bread",
        "recipe_image_url": "http://example.com/images/gluten_free_bread.jpg"
    }
]

allergies_list, excluded_recipes_list = get_allergies_and_recipes(allergies, recipes)
print(allergies_list)
print(excluded_recipes_list)



###################################################################################################



import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

def get_embeddings(texts, model_name="text-embedding-ada-002"):
    embedder = pipeline("feature-extraction", model=model_name)
    return np.array([np.mean(embedder(text), axis=0) for text in texts])

def score_allergens(recipes, allergens, model_name="text-embedding-ada-002"):
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

# 例の使用方法
recipes = [
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

allergens = ["ミルク", "ピーナッツ", "大豆"]

scores = score_allergens(recipes, allergens)
print(scores)



###################################################################################################



def sort_recipes_by_allergy_score(scores):
    # 各レシピのスコアを合計して、(レシピタイトル, 合計スコア)のリストを作成
    total_scores = [(recipe_title, sum(allergen_scores)) for recipe_title, allergen_scores in scores.items()]
    
    # 合計スコアでソート（スコアが高い順）
    sorted_recipes = sorted(total_scores, key=lambda x: x[1], reverse=True)
    
    return sorted_recipes

# スコアリング結果の例
scores = {
    "レシピ1": [0.8, 0.2, 0.1],
    "レシピ2": [0.3, 0.9, 0.4],
    "レシピ3": [0.1, 0.3, 0.8]
}

sorted_recipes = sort_recipes_by_allergy_score(scores)
print(sorted_recipes)



###################################################################################################



def main():
    # アレルギー品目とレシピデータの取得
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
        print(f"レシピ名: {recipe_title}, アレルギースコア合計: {total_score}")

if __name__ == "__main__":
    main()


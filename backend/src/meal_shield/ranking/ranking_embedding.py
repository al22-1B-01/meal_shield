# TODO: 内部設計書等を参照して関数名、変数名などを変更。コードの各位置を編集する（まとめる）
import logging
import os
from typing import Any

import numpy as np
from openai import OpenAI

from meal_shield.env import OPENAI_API_KEY

from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Make OpenAI text embdding score func


os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()

# 埋め込みを取得する関数
def get_embedding(text, model='text-embedding-3-small') -> Any:
    response = openai.Embedding.create(
        model=model,
        input=[text]
    )
    return response['data'][0]['embedding']

# レシピごとにアレルギーのスコアを計算する関数
def calculate_allergen_score(recipe, allergens):
    ingredient_embeddings = [get_embedding(ingredient) for ingredient in recipe['ingredients']]
    allergen_embeddings = [get_embedding(allergen) for allergen in allergens]

    # 材料のアレルギーへの類似度の平均を計算
    scores = []
    for ingredient_embedding in ingredient_embeddings:
        similarities = cosine_similarity([ingredient_embedding], allergen_embeddings)
        scores.append(np.mean(similarities))

    return np.mean(scores)

def score_allergens_by_embedding(
    recipes, allergens, model_name='text-embedding-3-small'
) -> dict[str, list[float]]:
    # 各レシピにアレルギースコアを追加
    for recipe in recipes:
        recipe['allergen_score'] = calculate_allergen_score(recipe, allergens)

    # TODO: update return data
    # max_score = np.max(similarity_scores)
    # max_scores.append(max_score)
    # scores[recipe_title] = max_scores

    return recipe

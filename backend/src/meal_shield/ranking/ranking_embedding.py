# TODO: 内部設計書等を参照して関数名、変数名などを変更。コードの各位置を編集する（まとめる）
import logging
import os
from typing import Any

import numpy as np
from openai import OpenAI

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Make OpenAI text embdding score func


os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()


def get_embedding(text, model='text-embedding-3-small') -> Any:
    text = text.replace('\n', ' ')
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def cosine_similarity(vec1, vec2) -> float:
    '''
    例として2つのベクトルを定義

    Usage:
    vector1 = np.array(get_embedding('文章1'))
    vector2 = np.array(get_embedding('文章2'))

    コサイン類似度の計算
    similarity = cosine_similarity(vector1, vector2)
    print(f'コサイン類似度: {similarity}')
    '''
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity


# fix (0.1->0.2): 出力の型がない
def score_allergens_by_embedding(
    recipes, allergens, model_name='text-embedding-3-small'
) -> dict[str, list[float]]:
    scores = {}

    allergen_embedding = get_embedding(', '.join(allergens))
    for recipe in recipes:
        recipe_ingredients_embedding = get_embedding(
            ', '.join(recipe['recipe_ingredients'])
        )
        sim_score = cosine_similarity(allergen_embedding, recipe_ingredients_embedding)
        # TODO: update return data
        # max_score = np.max(similarity_scores)
        # max_scores.append(max_score)
        # scores[recipe_title] = max_scores

    return scores

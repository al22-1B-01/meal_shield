import logging
import os
from typing import Any, Optional, Union

import numpy as np
from openai import OpenAI
from tqdm import tqdm

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()

# NOTE: デバッグ用
logger.debug('ranking_embedding.py was imported!')


def get_embedding(
    text: str,
    model_name: Optional[str] = 'text-embedding-3-small',
) -> Any:
    # 次元埋め込みを取得する関数
    embedding_response = client.embeddings.create(
        model=model_name,
        input=text,
    )

    return embedding_response.data[0].embedding


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity


def calc_allergens_include_score_by_embedding(
    allergies_list: list[str],
    recipe: dict[str, Union[str, list[str], float]],
) -> float:
    ingredient_embedding = get_embedding(','.join(recipe['recipe_ingredients']))
    allergen_embedding = get_embedding(','.join(allergies_list))

    # 指定されたアレルギー品目に対する材料の類似度を計算
    recipe_score = cosine_similarity(ingredient_embedding, allergen_embedding)

    return recipe_score


def scoring_embedding(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name: Optional[str] = 'text-embedding-3-small',
) -> list[dict[str, Union[str, list[str], float]]]:
    # 次元埋め込みを用いて各レシピのスコアを算出する
    for recipe in tqdm(excluded_recipes_list):
        recipe['recipe_score'] = calc_allergens_include_score_by_embedding(
            allergies_list, recipe
        )

    return excluded_recipes_list

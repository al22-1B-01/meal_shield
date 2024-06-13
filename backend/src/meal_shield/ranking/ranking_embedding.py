import logging
import os
from typing import Any, Optional, Union

from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()

# NOTE: デバッグ用info
logger.info('ranking_embedding.py was imported!')


def get_embedding(
    text: str,
    model_name: Optional[str] = 'text-embedding-3-small',
) -> Any:
    # 次元埋め込みを取得する関数
    embedding_response = client.embeddings.create(model=model_name, input=text)

    return embedding_response.data[0].embedding


def calc_allergens_include_score_by_embedding(
    allergies_list: list[str],
    recipe: dict[str, Union[str, list[str], float]],
) -> float:
    ingredient_embedding = get_embedding(''.join(recipe['recipe_ingredients']))
    allergen_embedding = get_embedding(''.join(allergies_list))

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

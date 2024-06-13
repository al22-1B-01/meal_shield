import logging
import os
from typing import Any, Union

from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()

# NOTE: デバッグ用info
logger.info('ranking_embedding.py was imported!')


def get_embedding(
    text: str,
    model_name='text-embedding-3-small',
) -> Any:
    # 次元埋め込みを取得する関数
    embedding_response = client.embeddings.create(model=model_name, input=text)

    return embedding_response.data[0].embedding


def calc_allergens_include_score(
    allergies_list: list[str],
    recipe: dict[str, Union[str, list[str], float]],
) -> float:
    ingredient_embeddings = get_embedding(''.join(recipe['recipe_ingredients']))
    allergen_embeddings = get_embedding(''.join(allergies_list))

    # 指定されたアレルギー品目に対する材料の類似度を計算
    recipe_score = cosine_similarity(ingredient_embeddings, allergen_embeddings)

    return recipe_score


def scoring_embedding(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name='text-embedding-3-small',
) -> list[dict[str, Union[str, list[str], float]]]:
    # 次元埋め込みを用いて各レシピのスコアを算出する
    for recipe in excluded_recipes_list:
        recipe['recipe_score'] = calc_allergens_include_score(allergies_list, recipe)

    return excluded_recipes_list

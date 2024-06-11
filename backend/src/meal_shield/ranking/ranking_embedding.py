import logging
import os
from typing import Any

from dotenv import load_dotenv
load_dotenv()

import numpy as np
from openai import OpenAI

from meal_shield.env import OPENAI_API_KEY

from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()

# NOTE: デバッグ用info
logger.info('ranking_embedding is running!')


def get_embedding(
    model_name='text-embedding-3-small',
    text: str,
) -> Any:
    # 次元埋め込みを取得する関数
    embedding_response = client.embeddings.create(
        model = model_name,
        input = text
    )

    return embedding_response.data[0].embedding


def calc_allergens_include_score(
    allergies_list: list[str],
    recipe: dict[str, Union[str, list[str], float]],
) -> float:
    pass


def scoring_embedding(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name='text-embedding-3-small'
) -> list[dict[str, Union[str, list[str], float]]]:
    # 次元埋め込みを用いて各レシピのスコアを算出する
    for recipe in excluded_recipes_list:
        recipe['recipe_score'] = calc_allergens_include_score(allergies_list, recipe)

    return excluded_recipes_list


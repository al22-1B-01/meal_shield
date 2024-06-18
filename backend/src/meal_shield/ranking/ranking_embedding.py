import asyncio
from typing import Any, Optional, Union, Final

import aiohttp
import numpy as np
from tqdm.asyncio import tqdm

from meal_shield.env import OPENAI_API_KEY


OPENAI_EMBEDDING_URL: Final[str] = "https://api.openai.com/v1/embeddings"

async def get_embedding(
    session: aiohttp.ClientSession,
    text: str,
    model_name: Optional[str] = 'text-embedding-3-small',
) -> Any:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {"model": model_name, "input": text}
    async with session.post(OPENAI_EMBEDDING_URL, json=data, headers=headers) as response:
        response_json = await response.json()
        return response_json['data'][0]['embedding']


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity


async def calc_allergens_include_score_by_embedding(
    session: aiohttp.ClientSession,
    allergies_list: list[str],
    recipe: dict[str, Union[str, list[str], float]],
    model_name: Optional[str] = 'text-embedding-3-small',
) -> float:
    ingredient_embedding = await get_embedding(
        session, ','.join(recipe['recipe_ingredients']), model_name
    )
    allergen_embedding = await get_embedding(
        session, ','.join(allergies_list), model_name
    )

    recipe_score = cosine_similarity(ingredient_embedding, allergen_embedding)
    return recipe_score


async def scoring_embedding_async(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name: Optional[str] = 'text-embedding-3-small',
    score_column: Optional[str] = 'recipe_score',
) -> list[dict[str, Union[str, list[str], float]]]:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for recipe in excluded_recipes_list:
            task = calc_allergens_include_score_by_embedding(
                session, allergies_list, recipe, model_name
            )
            tasks.append(task)

        recipe_scores = await tqdm.gather(
            *tasks, desc="Processing recipes by embedding"
        )

        for i, recipe in enumerate(excluded_recipes_list):
            recipe[score_column] = recipe_scores[i]

    return excluded_recipes_list


def scoring_embedding(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name: Optional[str] = 'text-embedding-3-small',
    score_column: Optional[str] = 'recipe_score',
) -> list[dict[str, Union[str, list[str], float]]]:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        scoring_embedding_async(
            allergies_list=allergies_list,
            excluded_recipes_list=excluded_recipes_list,
            model_name=model_name,
            score_column=score_column,
        )
    )

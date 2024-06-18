import asyncio
import logging
import re
from typing import Union

import aiohttp
from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm.asyncio import tqdm_asyncio

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NOTE: デバッグ用
logger.debug('ranking_chatgpt.py was imported!')

PATTERN = re.compile(r'score=(\d+)')


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
async def fetch_score(
    session: aiohttp.ClientSession, allergies_list: list[str], ingredient: list[str]
) -> float:
    # ChatGPTへのプロンプトを作成
    prompt = '{}にアレルギーがあります。\n{}を使った料理を作ります。\nこの料理の材料に含まれるアレルギー品目の割合を教えてください。回答は以下のフォーマットで答えてください：\n\nscore=XX%'
    organized_prompt = prompt.format(','.join(allergies_list), ','.join(ingredient))

    async with session.post(
        'https://api.openai.com/v1/chat/completions',
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': organized_prompt}],
        },
        headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
    ) as response:
        data = await response.json()
        res = data['choices'][0]['message']['content']
        logger.debug(res)

        try:
            m = re.match(PATTERN, res)
            score = float(m.group(1))
            return score
        except Exception as e:
            logger.error(f"Failed to parse score: {e}")
            return 101.0


async def calc_allergens_include_score_by_chatgpt(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
) -> list[dict[str, Union[str, list[str], float]]]:
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_score(session, allergies_list, recipe['recipe_ingredients'])
            for recipe in excluded_recipes_list
        ]
        scores = await tqdm_asyncio.gather(*tasks, desc="Processing recipes")

        for recipe, score in zip(excluded_recipes_list, scores):
            recipe['recipe_score'] = score

    return excluded_recipes_list


def scoring_chatgpt(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name='gpt-3.5-turbo',
) -> list[dict[str, Union[str, list[str], float]]]:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        calc_allergens_include_score_by_chatgpt(allergies_list, excluded_recipes_list)
    )

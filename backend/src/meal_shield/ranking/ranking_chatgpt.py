import logging
import os
import re
from typing import Union

from openai import OpenAI
from tqdm import tqdm

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()

# NOTE: デバッグ用
logger.debug('ranking_chatgpt.py was imported!')

PATTERN = r'score=(\d+)'


def calc_allergens_include_score_by_chatgpt(
    allergies_list: list[str],
    ingredient: list[str],
) -> float:
    # ChatGPTへのプロンプトを作成
    # TODO: より精度の高いプロンプトの考案
    prompt = '{}にアレルギーがあります。\n{}を使った料理を作ります。\nこの料理の材料に含まれるアレルギー品目の割合を教えてください。回答は以下のフォーマットで答えてください：\n\nscore=XX%'
    organized_prompt = prompt.format(','.join(allergies_list), ','.join(ingredient))

    response = client.chat.completions.create(
        model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': organized_prompt}]
    )
    # response.choices[0].message.content で答えが返る
    res = response.choices[0].message.content
    # NOTE: デバッグ用
    logger.debug(res)

    try:
        m = re.match(PATTERN, res)
        score = m.group(1)

        return float(score)
    except Exception as e:
        logger.info(e)


def scoring_chatgpt(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name='text-embedding-3-small',
) -> list[dict[str, Union[str, list[str], float]]]:
    # ChatGPTを用いて各レシピのスコアを算出する
    for recipe in tqdm(excluded_recipes_list):
        score: float = calc_allergens_include_score_by_chatgpt(
            allergies_list, recipe['recipe_ingredients']
        )
        recipe['recipe_score'] = score

    return excluded_recipes_list

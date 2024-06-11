import logging
import os

from openai import OpenAI

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()

# NOTE: デバッグ用info
logger.info('ranking_chatgpt is running!')


def calc_allergens_include_score(
    allergies_list: list[str],
    ingredient: str
) -> float:
    # ChatGPTへのプロンプトを作成
    # TODO: プロンプトでの結果、具体的な数字になるよう数字の幅、出力形式を決める
    prompt = ''

    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = prompt,
    )
    # res.choices[0].message.content で答えが返る

    # TODO: float変換したスコアを返す
    # NOTE: prompt -> 仮置き
    return prompt


def scoring_chatgpt(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name='text-embedding-3-small'
) -> list[dict[str, Union[str, list[str], float]]]:
    # ChatGPTを用いて各レシピのスコアを算出する
    for recipe in excluded_recipes_list:
        score: float = calc_allergens_include_score(allergies_list, recipe['ingredients'])
        recipe[recipe_score] = score
    
    return excluded_recipes_list

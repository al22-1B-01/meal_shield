import asyncio
import logging
import re
from typing import Final, Optional, Union

import aiohttp
from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm.asyncio import tqdm_asyncio

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CHATGPT_SCORE: Final[str] = r'score=(\d+)'
CHATGPT_SCORE_PATTERN: Final[re.Pattern] = re.compile(CHATGPT_SCORE)
CHATGPT_URL: Final[str] = 'https://api.openai.com/v1/chat/completions'
PROMPT_TEMPLATE: Final[
    str
] = '{}にアレルギーがあります。\n{}を使った料理を作ります。\nこの料理の材料に含まれるアレルギー品目の割合を教えてください。回答は以下のフォーマットで答えてください：\n\nscore=XX%'


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
async def fetch_score(
    session: aiohttp.ClientSession,
    allergies_list: list[str],
    ingredient: list[str],
    model_name: Optional[str] = 'gpt-3.5-turbo',
) -> float:
    '''ChatGPTからスコアを取得する関数。

    指定されたアレルギー品目と材料に基づき、ChatGPTからスコアを取得する。

    :param aiohttp.ClientSession session: HTTPセッションを管理するaiohttpクライアントセッション
    :param list[str] allergies_list: 指定されたアレルギー品目のデータをもったリスト
    :param list[str] ingredient: レシピの材料のリスト
    :param Optional[str] model_name: ChatGPTのモデルを設定する引数
    :return: スコア
    :rtype: float
    '''
    organized_prompt = PROMPT_TEMPLATE.format(
        ','.join(allergies_list), ','.join(ingredient)
    )

    async with session.post(
        CHATGPT_URL,
        json={
            'model': model_name,
            'messages': [{'role': 'user', 'content': organized_prompt}],
        },
        headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
    ) as response:
        data = await response.json()
        res = data['choices'][0]['message']['content']
        logger.debug(res)

        try:
            match = re.match(CHATGPT_SCORE_PATTERN, res)
            score = float(match.group(1))
            return score
        except Exception as e:
            logger.error(f"Failed to parse score: {e}")
            return 101.0


async def calc_allergens_include_score_by_chatgpt(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name: Optional[str] = 'gpt-3.5-turbo',
    score_column: Optional[str] = 'recipe_score',
) -> list[dict[str, Union[str, list[str], float]]]:
    '''非同期処理で各レシピに対してスコアリングを行う関数

    各レシピに対してChatGPTを利用して非同期処理でスコアリングを行う。

    :param list[str] allergies_list: 指定されたアレルギー品目のデータをもったリスト
    :param excluded_recipes_list: アレルギー除去処理を行ったレシピのデータをもったリスト
    :type excluded_recipes_list: list[dict[str, Union[str, list[str], float]]]
    :param Optional[str] model_name: ChatGPTのモデルを設定する引数
    :param Optional[str] score_column: 出力の辞書キー名を設定する変数
    :return: スコアリング済みの、アレルギー除去処理を行ったレシピのデータをもったリスト
    :rtype: list[dict[str, Union[str, list[str], float]]]
    '''
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_score(
                session, allergies_list, recipe['recipe_ingredients'], model_name
            )
            for recipe in excluded_recipes_list
        ]
        scores = await tqdm_asyncio.gather(*tasks, desc="Processing recipes by ChatGPT")

        for recipe, score in zip(excluded_recipes_list, scores):
            recipe[score_column] = score

    return excluded_recipes_list


async def scoring_chatgpt(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name: Optional[str] = 'gpt-3.5-turbo',
    score_column: Optional[str] = 'recipe_score',
) -> list[dict[str, Union[str, list[str], float]]]:
    '''ChatGPTによるスコアリングを行う関数。

    アレルギー除去処理を行ったレシピに対し、ChatGPTによるスコアリングを行う。

    :param list[str] allergies_list: 指定されたアレルギー品目のデータをもったリスト
    :param excluded_recipes_list: アレルギー除去処理を行ったレシピのデータをもったリスト
    :type excluded_recipes_list: list[dict[str, Union[str, list[str], float]]]
    :param Optional[str] model_name: ChatGPTのモデルを設定する引数
    :param Optional[str] score_column: 出力の辞書キー名を設定する変数
    :return: スコアリング済みの、アレルギー除去処理を行ったレシピのデータをもったリスト
    :rtype: list[dict[str, Union[str, list[str], float]]]
    '''
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        calc_allergens_include_score_by_chatgpt(
            allergies_list=allergies_list,
            excluded_recipes_list=excluded_recipes_list,
            model_name=model_name,
            score_column=score_column,
        )
    )

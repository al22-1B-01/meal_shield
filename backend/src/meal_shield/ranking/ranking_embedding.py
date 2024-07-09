import asyncio
from typing import Any, Final, Optional, Union

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
    '''次元埋め込みで言語情報をベクトル化する関数。

    次元埋め込みを用いて言語情報をベクトル化する。

    :param aiohttp.ClientSession session: HTTPセッションを管理するaiohttpクライアントセッション
    :param str text: ベクトル化する言語情報
    :param Optional[str] model_name: 次元埋め込みのモデルを設定する引数
    '''
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {"model": model_name, "input": text}
    async with session.post(
        OPENAI_EMBEDDING_URL, json=data, headers=headers
    ) as response:
        response_json = await response.json()
        return response_json['data'][0]['embedding']


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    '''コサイン類似度を計算する関数。

    レシピの材料と指定されたアレルギー品目に対するコサイン類似度を計算する。

    :param list[float] vec1: ベクトル化したレシピの材料のリスト
    :param list[float] vec2: ベクトル化したアレルギー品目のリスト
    :return: コサイン類似度の計算結果
    :rtype: float
    '''
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # 0除算対策
    if norm_vec1 * norm_vec2 != 0:
        similarity = dot_product / (norm_vec1 * norm_vec2)
        return similarity
    else:
        return 0.0


async def calc_allergens_include_score_by_embedding(
    session: aiohttp.ClientSession,
    allergies_list: list[str],
    recipe: dict[str, Union[str, list[str], float]],
    model_name: Optional[str] = 'text-embedding-3-small',
) -> float:
    '''実際にスコアリングを行う関数。

    コサイン類似度を用いてレシピのスコアリングを行う。

    :param aiohttp.ClientSession session: HTTPセッションを管理するaiohttpクライアントセッション
    :param list[str] allergies_list: 指定されたアレルギー品目のデータをもったリスト
    :param dict[str, Union[str, list[str], float]] recipe: スコアリング対象となるレシピ単体
    :param Optional[str] model_name: 次元埋め込みのモデルを設定する引数
    :return: スコア
    :rtype: float
    '''
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
    '''非同期処理で各レシピにスコアリングを行う関数。

    各レシピに対して次元埋め込みを利用して非同期処理でスコアリングを行う。

    :param list[str] allergies_list: 指定されたアレルギー品目のデータをもったリスト
    :param excluded_recipes_list: アレルギー除去処理を行ったレシピのデータをもったリスト
    :type excluded_recipes_list: list[dict[str, Union[str, list[str], float]]]
    :param Optional[str] model_name: 次元埋め込みのモデルを設定する引数
    :param Optional[str] score_column: 出力の辞書キー名を設定する変数
    :return: スコアリング済みの、アレルギー除去処理を行ったレシピのデータをもったリスト
    :rtype: list[dict[str, Union[str, list[str], float]]]
    '''
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


async def scoring_embedding(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    model_name: Optional[str] = 'text-embedding-3-small',
    score_column: Optional[str] = 'recipe_score',
) -> list[dict[str, Union[str, list[str], float]]]:
    '''次元埋め込みによるスコアリングを行う関数。

    アレルギー除去処理を行ったレシピに対し、次元埋め込みによるスコアリングを行う。

    :param list[str] allergies_list: 指定されたアレルギー品目のデータをもったリスト
    :param excluded_recipes_list: アレルギー除去処理を行ったレシピのデータをもったリスト
    :type excluded_recipes_list: list[dict[str, Union[str, list[str], float]]]
    :param Optional[str] model_name: 次元埋め込みのモデルを設定する引数
    :param Optional[str] score_column: 出力の辞書キー名を設定する変数
    :return: スコアリング済みの、アレルギー除去処理を行ったレシピのデータをもったリスト
    :rtype: list[dict[str, Union[str, list[str], float]]]
    '''
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        scoring_embedding_async(
            allergies_list=allergies_list,
            excluded_recipes_list=excluded_recipes_list,
            model_name=model_name,
            score_column=score_column,
        )
    )

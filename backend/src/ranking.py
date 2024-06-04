# TODO: 内部設計書等を参照して関数名、変数名などを変更。コードの各位置を編集する（まとめる）
import logging
import os
from typing import Any, Optional, Union

import numpy as np
from openai import OpenAI

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_allergies_and_recipes(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str]]]],
) -> (list[str], list[dict[str, Union[str, list[str]]]]):
    '''
    指定されたアレルギー品目とレシピのリストを取得する関数。

    :param allergies_list: アレルギー品目のデータを持つリスト
    :param excluded_recipes_list: レシピのデータを持ったリスト
    :return: アレルギー品目リストとレシピデータリストのタプル
    '''

    # ここでC5から指定されたアレルギー品目とレシピのリストを受け取る

    return allergies_list, excluded_recipes_list


# TODO: Make rule base count score func


def score_allergens(recipes, allergens) -> dict[str, list[float]]:
    pass


# TODO: Make OpenAI text embdding score func


os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()


def get_embedding(text, model='text-embedding-3-small') -> Any:
    text = text.replace('\n', ' ')
    return client.embeddings.create(input=[text], model=model).data[0].embedding


# TODO: Make OpenAI Chatgpt scoring func

def cosine_similarity(vec1, vec2) -> float:
    '''
    例として2つのベクトルを定義

    Usage:
    vector1 = np.array(get_embedding('文章1'))
    vector2 = np.array(get_embedding('文章2'))

    コサイン類似度の計算
    similarity = cosine_similarity(vector1, vector2)
    print(f'コサイン類似度: {similarity}')
    '''
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity


# fix (0.1->0.2): 出力の型がない
def score_allergens_by_embedding(
    recipes, allergens, model_name='text-embedding-3-small'
) -> dict[str, list[float]]:
    scores = {}

    allergen_embedding = get_embedding(', '.join(allergens))
    for recipe in recipes:
        recipe_ingredients_embedding = get_embedding(
            ', '.join(recipe['recipe_ingredients'])
        )
        sim_score = cosine_similarity(allergen_embedding, recipe_ingredients_embedding)
        # TODO: update return data
        # max_score = np.max(similarity_scores)
        # max_scores.append(max_score)
        # scores[recipe_title] = max_scores

    return scores


def score_allergens_by_chatgpt(
    recipes, allergens, model_name='text-embedding-3-small'
) -> dict[str, list[float]]:
    pass


def sort_recipes_by_allergy_score(
    scores,
) -> (list[str], list[dict[str, Union[str, list[str]]]]):
    # 各レシピのスコアを合計して、(レシピタイトル, 合計スコア)のリストを作成
    total_scores = [
        (recipe_title, sum(allergen_scores))
        for recipe_title, allergen_scores in scores.items()
    ]

    # 合計スコアでソート（スコアが高い順）
    sorted_recipes = sorted(total_scores, key=lambda x: x[1], reverse=True)

    return sorted_recipes


def ranking_recipe(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str]]]],
    ranking_method: Optional[str] = 'defalt',
) -> dict[str, Union[str, list[str]]]:
    # スコアリング関数の呼び出し
    if ranking_method == 'defalt':
        scores = score_allergens(excluded_recipes_list, allergies_list)
    elif ranking_method == 'embedding':
        scores = score_allergens_by_embedding(excluded_recipes_list, allergies_list)
    elif ranking_method == 'chatgpt':
        scores = score_allergens_by_chatgpt(excluded_recipes_list, allergies_list)

    # スコアリング結果のソート
    sorted_recipes = sort_recipes_by_allergy_score(scores)

    return sorted_recipes


def main():
    # アレルギー品目とレシピデータの取得
    # 正式実装の際は、get_allergies_and_recipes関数内でC5から受け取る
    # allergies_list, excluded_recipes_list = get_allergies_and_recipes(allergies, recipes)
    allergies_list = ['ミルク', 'ピーナッツ', '大豆']
    excluded_recipes_list = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['ミルク', '卵', '小麦粉'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['ピーナッツ', '砂糖', 'バター'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['大豆', '小麦', '鶏肉'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
        },
    ]

    sorted_recipes = ranking_recipe(
        allergies_list=allergies_list,
        excluded_recipes_list=excluded_recipes_list,
    )

    # ソート結果の表示
    for recipe_title, total_score in sorted_recipes:
        logger.info(f'レシピ名: {recipe_title}, アレルギースコア合計: {total_score}')


if __name__ == '__main__':
    ranking_recipe()

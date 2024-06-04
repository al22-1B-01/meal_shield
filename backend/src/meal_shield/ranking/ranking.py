import logging
from typing import Optional, Union

from meal_shield.ranking.ranking_chatgpt import score_allergens_by_chatgpt
from meal_shield.ranking.ranking_count import score_allergens
from meal_shield.ranking.ranking_embedding import score_allergens_by_embedding

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

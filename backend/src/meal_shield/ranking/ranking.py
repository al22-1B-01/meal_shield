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

    # ここでC5から指定されたアレルギー品目とレシピのリストを受け取る

    return allergies_list, excluded_recipes_list


def sort_recipes_by_allergy_score(
    scores: dict[str, float],
) -> (list[str], list[dict[str, Union[str, list[str]]]]):
    # スコアが低い順にソートする
    sorted_recipes = dict(sorted(scores.items(), key=lambda item: item[1]))
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
    allergies_list = ['かに', '乳', '大豆']
    excluded_recipes_list = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['カニ', '卵', '小麦粉'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['かに', 'チーズ', '砂糖'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['大豆', 'ヨーグルト', '蟹'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
        },
    ]

    # スコアリング関数の呼び出し
    sorted_recipes = ranking_recipe(
        allergies_list=allergies_list,
        excluded_recipes_list=excluded_recipes_list,
    )

    # ソート結果の表示
    for recipe_title, total_score in sorted_recipes.items():
        logger.info(f'レシピ名: {recipe_title}, アレルギースコア合計: {total_score}')


if __name__ == '__main__':
    main()

import logging
from typing import Optional, Union

# from meal_shield.ranking.ranking_chatgpt import scoring_chatgpt
from meal_shield.ranking.ranking_count import scoring_count
from meal_shield.ranking.ranking_embedding import scoring_embedding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sort_recipes_by_allergy_score(
    scored_recipes_list: list[dict[str, Union[str, list[str], float]]],
) -> list[dict[str, Union[str, list[str], float]]]:
    # スコアが低い順にソートする
    sorted_excluded_recipes_list = sorted(
        scored_recipes_list, key=lambda x: x['recipe_score']
    )

    return sorted_excluded_recipes_list


def ranking_recipe(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    ranking_method: Optional[str] = 'embedding',
) -> list[dict[str, Union[str, list[str]]]]:
    '''
    scored_recipes_list: list[dict[str, Union[str, list[str], float]]]
        スコアリング済みのレシピデータをもつリスト
    '''
    # スコアリング関数の呼び出し
    if ranking_method == 'default':
        scored_recipes_list = scoring_count(allergies_list, excluded_recipes_list)
    elif ranking_method == 'embedding':
        scored_recipes_list = scoring_embedding(allergies_list, excluded_recipes_list)
    elif ranking_method == 'chatgpt':
        scored_recipes_list = scoring_chatgpt(allergies_list, excluded_recipes_list)

    # スコアに基づいたソートを行う
    sorted_excluded_recipes_list = sort_recipes_by_allergy_score(scored_recipes_list)

    return sorted_excluded_recipes_list


def main():
    '''
    allergies_list: list[str], 指定されたアレルギー品目のデータをもつリスト
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    除去処理を行った（辞書型の）レシピデータをもつリスト
    '''
    # アレルギー品目とレシピデータを取得
    # TODO: 正式実装の際はC5から受け取り、レシピデータのリストに新たにrecipe_scoreを追加
    allergies_list = ['かに', '乳', '大豆']
    excluded_recipes_list = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['カニ', '卵', '小麦粉'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
            'recipe_score': 0.0,
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['かに', 'チーズ', '砂糖'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
            'recipe_score': 0.0,
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['大豆', 'ヨーグルト', '蟹'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
            'recipe_score': 0.0,
        },
    ]

    # 各レシピに対してスコアリングを行い、スコアに基づいたソートを行う
    sorted_excluded_recipes_list = ranking_recipe(
        allergies_list=allergies_list,
        excluded_recipes_list=excluded_recipes_list,
    )

    # ソート結果の表示
    # TODO: 正式実装の際は、ranking_recipe関数内でC3に結果を渡す
    for recipe in sorted_excluded_recipes_list:
        recipe_title = recipe.get("recipe_title")
        recipe_score = recipe.get("recipe_score")
        logger.info(f'レシピ名: {recipe_title}, アレルギースコア合計: {recipe_score}')


if __name__ == '__main__':
    main()

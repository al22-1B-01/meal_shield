import logging
from typing import Optional, Union

from meal_shield.ranking.ranking_chatgpt import scoring_chatgpt
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

from typing import Optional, Union

from meal_shield.ranking.ranking_chatgpt import scoring_chatgpt
from meal_shield.ranking.ranking_count import scoring_count
from meal_shield.ranking.ranking_embedding import scoring_embedding


def calc_normalized_score(
    recipes_list: list[dict[str, Union[str, list[str], float]]],
    score_column: Optional[str] = 'recipe_score',
) -> list[dict[str, Union[str, list[str], float]]]:
    max_score = max([recipe[score_column] for recipe in recipes_list])

    for recipe in recipes_list:
        recipe[score_column] = recipe[score_column] / max_score

    return recipes_list


def calc_hybrid_score(
    scored_recipes_list: list[dict[str, Union[str, list[str], float]]],
    score_columns: list[str],
) -> list[dict[str, Union[str, list[str], float]]]:
    for score_column in score_columns:
        scored_recipes_list = calc_normalized_score(scored_recipes_list, score_column)
    for scored_recipe in scored_recipes_list:
        scored_recipe['recipe_score'] = sum(
            [scored_recipe[score_column] for score_column in score_columns]
        )
    for score_column in score_columns:
        for scored_recipe in scored_recipes_list:
            del scored_recipe[score_column]

    return scored_recipes_list


def ranking_recipe(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    ranking_method: Optional[str] = 'hybrid',
) -> list[dict[str, Union[str, list[str]]]]:
    if ranking_method == 'default':
        scored_recipes_list = scoring_count(allergies_list, excluded_recipes_list)
    elif ranking_method == 'embedding':
        scored_recipes_list = scoring_embedding(allergies_list, excluded_recipes_list)
    elif ranking_method == 'chatgpt':
        scored_recipes_list = scoring_chatgpt(allergies_list, excluded_recipes_list)
    elif ranking_method == 'hybrid':
        scored_recipes_list = scoring_chatgpt(
            allergies_list,
            excluded_recipes_list,
            model_name='gpt-3.5-turbo',
            score_column='chatgpt_score',
        )
        scored_recipes_list = scoring_embedding(
            allergies_list,
            excluded_recipes_list,
            model_name='text-embedding-3-small',
            score_column='embedding_score',
        )
        scored_recipes_list = scoring_count(
            allergies_list, excluded_recipes_list, score_column='count_score'
        )
        score_columns = ['chatgpt_score', 'embedding_score', 'count_score']
        scored_recipes_list = calc_hybrid_score(scored_recipes_list, score_columns)

    sorted_excluded_recipes_list = sorted(
        scored_recipes_list, key=lambda x: x['recipe_score']
    )

    return sorted_excluded_recipes_list

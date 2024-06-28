from unittest.mock import AsyncMock, patch

import pytest

from meal_shield.ranking.ranking_chatgpt import fetch_score, scoring_chatgpt

ALLERGIES = ['えび', 'かに', '小麦']
RECIPES = [
    {
        'recipe_title': 'レシピ1',
        'recipe_ingredients': ['えび', 'かに', '小麦'],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
    },
    {
        'recipe_title': 'レシピ2',
        'recipe_ingredients': ['エビ', 'カニ', 'しょうゆ'],
        'recipe_url': 'http://example.com/recipe2',
        'recipe_image_url': 'http://example.com/recipe2.jpg',
    },
    {
        'recipe_title': 'レシピ3',
        'recipe_ingredients': ['海老', '蟹', '醤油'],
        'recipe_url': 'http://example.com/recipe3',
        'recipe_image_url': 'http://example.com/recipe3.jpg',
    },
]


@patch('meal_shield.ranking.ranking_chatgpt.fetch_score')
def test_scoring_chatgpt(mock_fetch_score):
    mock_fetch_score.return_value = 50.0

    result_with_model_name = scoring_chatgpt(
        ALLERGIES, RECIPES, model_name='gpt-3.5-turbo'
    )
    result_with_score_column = scoring_chatgpt(
        ALLERGIES, RECIPES, score_column='recipe_score'
    )
    result_with_optional = scoring_chatgpt(
        ALLERGIES, RECIPES, model_name='gpt-3.5-turbo', score_column='recipe_score'
    )
    result_without_optional = scoring_chatgpt(ALLERGIES, RECIPES)

    expected_result = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['えび', 'かに', '小麦'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
            'recipe_score': 50.0,
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['エビ', 'カニ', 'しょうゆ'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
            'recipe_score': 50.0,
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['海老', '蟹', '醤油'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
            'recipe_score': 50.0,
        },
    ]

    assert result_with_model_name == expected_result
    assert result_with_score_column == expected_result
    assert result_with_optional == expected_result
    assert result_without_optional == expected_result

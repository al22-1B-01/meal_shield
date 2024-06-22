from unittest.mock import patch

import pytest

from meal_shield.ranking.ranking import calc_hybrid_score, ranking_recipe
from meal_shield.ranking.ranking_chatgpt import scoring_chatgpt
from meal_shield.ranking.ranking_count import scoring_count
from meal_shield.ranking.ranking_embedding import scoring_embedding


@patch('meal_shield.ranking.ranking.calc_hybrid_score')
@patch('meal_shield.ranking.ranking.scoring_chatgpt')
@patch('meal_shield.ranking.ranking.scoring_embedding')
@patch('meal_shield.ranking.ranking.scoring_count')
def test_ranking_recipe(
    mock_scoring_count,
    mock_scoring_embedding,
    mock_scoring_chatgpt,
    mock_calc_hybrid_score,
):
    mock_scoring_chatgpt.return_value = [
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
    mock_scoring_embedding.return_value = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['えび', 'かに', '小麦'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
            'recipe_score': 0.5,
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['エビ', 'カニ', 'しょうゆ'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
            'recipe_score': 0.5,
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['海老', '蟹', '醤油'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
            'recipe_score': 0.5,
        },
    ]
    mock_scoring_count.return_value = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['えび', 'かに', '小麦'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
            'recipe_score': 3.0,
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['エビ', 'カニ', 'しょうゆ'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
            'recipe_score': 3.0,
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['海老', '蟹', '醤油'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
            'recipe_score': 3.0,
        },
    ]
    mock_calc_hybrid_score.return_value = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['えび', 'かに', '小麦'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
            'recipe_score': 17.83,
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['エビ', 'カニ', 'しょうゆ'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
            'recipe_score': 17.83,
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['海老', '蟹', '醤油'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
            'recipe_score': 17.83,
        },
    ]

    allergies = ['えび', 'かに', '小麦']
    recipes = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['えび', 'かに', '小麦'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
            'recipe_score': 0.0,
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['エビ', 'カニ', 'しょうゆ'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
            'recipe_score': 0.0,
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['海老', '蟹', '醤油'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
            'recipe_score': 0.0,
        },
    ]

    result_chatgpt = ranking_recipe(allergies, recipes, ranking_method='chatgpt')
    result_embedding = ranking_recipe(allergies, recipes, ranking_method='embedding')
    result_count = ranking_recipe(allergies, recipes, ranking_method='default')
    result_hybrid = ranking_recipe(allergies, recipes, ranking_method='hybrid')

    expected_result_chatgpt = [
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
    expected_result_embedding = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['えび', 'かに', '小麦'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
            'recipe_score': 0.5,
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['エビ', 'カニ', 'しょうゆ'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
            'recipe_score': 0.5,
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['海老', '蟹', '醤油'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
            'recipe_score': 0.5,
        },
    ]
    expected_result_count = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['えび', 'かに', '小麦'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
            'recipe_score': 3.0,
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['エビ', 'カニ', 'しょうゆ'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
            'recipe_score': 3.0,
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['海老', '蟹', '醤油'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
            'recipe_score': 3.0,
        },
    ]
    expected_result_hybrid = [
        {
            'recipe_title': 'レシピ1',
            'recipe_ingredients': ['えび', 'かに', '小麦'],
            'recipe_url': 'http://example.com/recipe1',
            'recipe_image_url': 'http://example.com/recipe1.jpg',
            'recipe_score': 17.83,
        },
        {
            'recipe_title': 'レシピ2',
            'recipe_ingredients': ['エビ', 'カニ', 'しょうゆ'],
            'recipe_url': 'http://example.com/recipe2',
            'recipe_image_url': 'http://example.com/recipe2.jpg',
            'recipe_score': 17.83,
        },
        {
            'recipe_title': 'レシピ3',
            'recipe_ingredients': ['海老', '蟹', '醤油'],
            'recipe_url': 'http://example.com/recipe3',
            'recipe_image_url': 'http://example.com/recipe3.jpg',
            'recipe_score': 17.83,
        },
    ]

    assert result_chatgpt == expected_result_chatgpt
    assert result_embedding == expected_result_embedding
    assert result_count == expected_result_count
    assert result_hybrid == expected_result_hybrid

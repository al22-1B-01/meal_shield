from unittest.mock import patch

import nest_asyncio
import pytest
from fastapi.testclient import TestClient

from meal_shield.app import app

nest_asyncio.apply()

ALLERGIES = ['えび', 'かに', '小麦']
RECIPES = [
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


@pytest.mark.asyncio
@patch('meal_shield.app.scraping_and_excluding')
@patch('meal_shield.app.ranking_recipe')
async def test_get_recipe(mock_ranking_recipe, mock_scraping_and_excluding):
    # 正常パターン
    mock_scraping_and_excluding.return_value = RECIPES
    mock_ranking_recipe.return_value = [
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

    client = TestClient(app)

    response = client.get(
        "/?recipe=sample_recipe&allergy_list=えび&allergy_list=かに&allergy_list=小麦"
    )
    assert response.status_code == 200
    assert response.json() == [
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

    # エラーパターン: アレルギーリストが空
    response = client.get("/?recipe=sample_recipe")
    assert response.status_code == 200
    assert response.json() == [
        {'status': 'error', 'message': 'No allergy list', 'data': []}
    ]

    # エラーパターン: レシピが見つからない
    mock_scraping_and_excluding.return_value = None
    response = client.get(
        "/?recipe=sample_recipe&allergy_list=えび&allergy_list=かに&allergy_list=小麦"
    )
    assert response.status_code == 200
    assert response.json() == [{'status': 'error', 'message': 'No recipe', 'data': []}]

from unittest.mock import patch

import nest_asyncio
import numpy as np
import pytest

nest_asyncio.apply()

from meal_shield.ranking.ranking_embedding import cosine_similarity, scoring_embedding

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


@pytest.mark.asyncio
@patch(
    'meal_shield.ranking.ranking_embedding.calc_allergens_include_score_by_embedding'
)
async def test_scoring_embedding(mock_calc_allergens_include_score_by_embedding):
    mock_calc_allergens_include_score_by_embedding.return_value = 0.5

    result_with_model_name = await scoring_embedding(
        ALLERGIES, RECIPES, model_name='text-embedding-3-small'
    )
    result_with_score_column = await scoring_embedding(
        ALLERGIES, RECIPES, score_column='recipe_score'
    )
    result_with_optional = await scoring_embedding(
        ALLERGIES,
        RECIPES,
        model_name='text-embedding-3-small',
        score_column='recipe_score',
    )
    result_without_optional = await scoring_embedding(ALLERGIES, RECIPES)

    expected_result = [
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

    assert result_with_model_name == expected_result
    assert result_with_score_column == expected_result
    assert result_with_optional == expected_result
    assert result_without_optional == expected_result


# cosine_similarity関数の単体テストに関する関数群
def test_cosine_similarity():
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([4, 5, 6])
    result = cosine_similarity(vec1, vec2)
    expected_result = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    assert result == pytest.approx(
        expected_result
    ), f'Expected {expected_result}, got {result}'


def test_cosine_similarity_zero_vector():
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([0, 0, 0])
    result = cosine_similarity(vec1, vec2)
    expected_result = 0.0
    assert result == expected_result, f'Expected {expected_result}, got {result}'


def test_cosine_similarity_identical_vectors():
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([1, 2, 3])
    result = cosine_similarity(vec1, vec2)
    expected_result = 1.0
    assert result == expected_result, f'Expected {expected_result}, got {result}'


def test_cosine_similarity_orthogonal_vectors():
    vec1 = np.array([1, 0])
    vec2 = np.array([0, 1])
    result = cosine_similarity(vec1, vec2)
    expected_result = 0.0
    assert result == expected_result, f'Expected {expected_result}, got {result}'

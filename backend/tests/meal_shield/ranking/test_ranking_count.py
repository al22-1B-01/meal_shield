import pytest

from meal_shield.ranking.ranking_count import scoring_count


def test_scoring_count():
    # テスト用のアレルギー品目とレシピ
    allergies = ['えび', "かに", '小麦']
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

    # 関数実行
    result = scoring_count(allergies, recipes)

    # 期待される結果
    expected_result = [
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

    assert result == expected_result

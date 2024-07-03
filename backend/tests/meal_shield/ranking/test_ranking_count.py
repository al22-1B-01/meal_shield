from meal_shield.ranking.ranking_count import (
    WORDS,
    extract_allergy_words,
    scoring_count,
    scoring_recipe,
)

# テスト用のアレルギー品目とレシピ
ALLERGIES = ['えび', "かに", '小麦']
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


def test_scoring_count():
    # 関数実行
    result_with_optional = scoring_count(
        ALLERGIES, RECIPES, score_column='recipe_score'
    )
    result_without_optional = scoring_count(ALLERGIES, RECIPES)

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

    assert result_with_optional == expected_result
    assert result_without_optional == expected_result


# scoring_recipe関数の単体テストに関する関数群
def test_scoring_recipe_no_allergens():
    allergies = ['卵', '牛乳']
    recipe = {
        'recipe_title': 'アレルギー該当なし',
        'recipe_ingredients': ['小麦', '水', '砂糖'],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
    }
    result_with_optional = scoring_recipe(
        recipe, allergies, score_column='recipe_score'
    )
    result_without_optional = scoring_recipe(recipe, allergies)
    expected_result = {
        'recipe_title': 'アレルギー該当なし',
        'recipe_ingredients': ['小麦', '水', '砂糖'],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
        'recipe_score': 0.0,
    }
    assert (
        result_with_optional == expected_result
    ), f'Expected {expected_result}, got {result_with_optional}'
    assert (
        result_without_optional == expected_result
    ), f'Expected {expected_result}, got {result_without_optional}'


def test_scoring_recipe_some_allergens():
    allergies = ['卵', '牛乳']
    recipe = {
        'recipe_title': 'アレルギー一つ',
        'recipe_ingredients': ['小麦', '水', '卵'],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
    }
    result_with_optional = scoring_recipe(
        recipe, allergies, score_column='recipe_score'
    )
    result_without_optional = scoring_recipe(recipe, allergies)
    expected_result = {
        'recipe_title': 'アレルギー一つ',
        'recipe_ingredients': ['小麦', '水', '卵'],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
        'recipe_score': 1.0,
    }
    assert (
        result_with_optional == expected_result
    ), f'Expected {expected_result}, got {result_with_optional}'
    assert (
        result_without_optional == expected_result
    ), f'Expected {expected_result}, got {result_without_optional}'


def test_scoring_recipe_all_allergens():
    allergies = ['卵', '牛乳']
    recipe = {
        'recipe_title': 'アレルギー全該当',
        'recipe_ingredients': ['卵', '水', '牛乳'],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
    }
    result_with_optional = scoring_recipe(
        recipe, allergies, score_column='recipe_score'
    )
    result_without_optional = scoring_recipe(recipe, allergies)
    expected_result = {
        'recipe_title': 'アレルギー全該当',
        'recipe_ingredients': ['卵', '水', '牛乳'],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
        'recipe_score': 2.0,
    }
    assert (
        result_with_optional == expected_result
    ), f'Expected {expected_result}, got {result_with_optional}'
    assert (
        result_without_optional == expected_result
    ), f'Expected {expected_result}, got {result_without_optional}'


def test_scoring_recipe_no_ingredients():
    allergies = ['卵', '牛乳']
    recipe = {
        'recipe_title': '材料なし',
        'recipe_ingredients': [],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
    }
    result_with_optional = scoring_recipe(
        recipe, allergies, score_column='recipe_score'
    )
    result_without_optional = scoring_recipe(recipe, allergies)
    expected_result = {
        'recipe_title': '材料なし',
        'recipe_ingredients': [],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
        'recipe_score': 0.0,
    }
    assert (
        result_with_optional == expected_result
    ), f'Expected {expected_result}, got {result_with_optional}'
    assert (
        result_without_optional == expected_result
    ), f'Expected {expected_result}, got {result_without_optional}'


def test_scoring_recipe_no_allergies():
    allergies = []
    recipe = {
        'recipe_title': 'アレルギーなし',
        'recipe_ingredients': ['小麦', '水', '砂糖'],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
    }
    result_with_optional = scoring_recipe(
        recipe, allergies, score_column='recipe_score'
    )
    result_without_optional = scoring_recipe(recipe, allergies)
    expected_result = {
        'recipe_title': 'アレルギーなし',
        'recipe_ingredients': ['小麦', '水', '砂糖'],
        'recipe_url': 'http://example.com/recipe1',
        'recipe_image_url': 'http://example.com/recipe1.jpg',
        'recipe_score': 0.0,
    }
    assert (
        result_with_optional == expected_result
    ), f'Expected {expected_result}, got {result_with_optional}'
    assert (
        result_without_optional == expected_result
    ), f'Expected {expected_result}, got {result_without_optional}'


def test_extract_allergy_words():
    result = extract_allergy_words(WORDS, ALLERGIES)
    expected_result = ['えび', 'エビ', '海老', 'かに', 'カニ', '蟹', '小麦', '醤油', 'しょうゆ', '小麦粉']
    assert result == expected_result

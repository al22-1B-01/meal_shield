# test_fetch_recipes.py
from unittest.mock import patch

import pytest
import requests
import streamlit as st

from meal_shield.env import PACKAGE_DIR

base_url = 'http://backend:8000'


def fetch_recipes(recipe_name, allergies: list[str]) -> list:
    params = {'recipi': recipe_name, 'allergy_list': allergies}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'エラーが発生しました: {response.status_code}')
        return None


@pytest.fixture
def mock_response_success():
    return {
        "recipes": [
            {
                "recipe_title": "イチゴケーキ",
                "recipe_image_url": "https://img.cpcdn.com/recipes/7813040/"
                "894x1461s/952f6a9105c7b1d250853791cc4b08fd?u=117"
                "56033&p=1714165191",
                "recipe_ingredients": ["卵", "砂糖", "バター"],
                "recipe_url": "https://cookpad.com/recipe/7813040",
            },
            {
                "recipe_title": "いちごけーき",
                "recipe_image_url": "https://img.cpcdn.com/recipes/7781284/"
                "894x1461s/9b37148a4668a565830b9514d3af1a74?u=9240495"
                "&p=1711003018",
                "recipe_ingredients": ["卵", "牛乳", "バニラ"],
                "recipe_url": "https://cookpad.com/recipe/7781284",
            },
        ]
    }


@pytest.fixture
def mock_response_failure():
    return {"error": "Not Found"}


@patch("requests.get")
def test_fetch_recipes_success(mock_get, mock_response_success):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response_success

    recipe_name = "ケーキ"
    allergies = ["卵", "乳"]
    result = fetch_recipes(recipe_name, allergies)

    assert result == mock_response_success


@patch("requests.get")
def test_fetch_recipes_failure(mock_get, mock_response_failure):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = mock_response_failure

    recipe_name = "ケーキ"
    allergies = ["卵", "乳"]
    result = fetch_recipes(recipe_name, allergies)

    assert result is None

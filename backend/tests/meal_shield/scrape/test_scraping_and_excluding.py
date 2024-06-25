import os
from unittest.mock import Mock, patch

import pytest
import requests
from bs4 import BeautifulSoup

from meal_shield.scrape.scraping_and_excluding import (
    excluding_recipe,
    scraping_and_excluding,
)


# テキストファイルからHTMLを取得
def load_mock_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # レスポンスごとに分割
    responses = content.split('\n\n# ')
    return [resp.strip() for resp in responses if resp.strip()]


mock_data_file_path = os.path.join(os.path.dirname(__file__), 'mock_data.txt')
mock_data = load_mock_data(mock_data_file_path)
# モックHTMLデータ
mock_response_recipe_page_1 = Mock()
mock_response_recipe_page_1.text = mock_data[0]
mock_response_recipe_page_1.content = mock_response_recipe_page_1.text.encode('utf-8')

mock_response_recipe_page_2 = Mock()
mock_response_recipe_page_2.text = mock_data[1]
mock_response_recipe_page_2.content = mock_response_recipe_page_2.text.encode('utf-8')

mock_response_recipe_1 = Mock()
mock_response_recipe_1.text = mock_data[2]
mock_response_recipe_1.content = mock_response_recipe_1.text.encode('utf-8')

mock_response_recipe_2 = Mock()
mock_response_recipe_2.text = mock_data[3]
mock_response_recipe_2.content = mock_response_recipe_2.text.encode('utf-8')


# モックのサイドエフェクト関数を定義
def mock_side_effect(url, *args, **kwargs):
    if url == 'https://cookpad.com/search/ココナッツカレー':
        return mock_response_recipe_page_1
    elif url == 'https://cookpad.com/search/ココナッツカレー?page=1':
        return mock_response_recipe_page_1
    elif url == 'https://cookpad.com/search/ココナッツカレー?page=2':
        return mock_response_recipe_page_2
    elif url == 'https://cookpad.com/recipe/7836445':
        return mock_response_recipe_1
    elif url == 'https://cookpad.com/recipe/7850799':
        return mock_response_recipe_2
    else:
        raise requests.exceptions.ConnectionError


# 材料にアレルギーを含む要素を除外
def test_excluding_recipe_normal():
    allergy_list = ['いか']
    recipe_data_list = [
        {
            'recipe_title': 'ホットクックで簡単ココナッツカレー',
            'recipe_ingredients': ['玉ねぎ', 'にんじん'],
            'recipe_url': 'recipe_url_1',
            'recipe_image_url': 'recipe_image_url_1',
        },
        {
            'recipe_title': '絶品！シーフードココナッツカレー',
            'recipe_ingredients': ['いか', '海老'],
            'recipe_url': 'recipe_url_2',
            'recipe_image_url': 'recipe_image_url_2',
        },
    ]
    excluded_recipe_data_list = excluding_recipe(allergy_list, recipe_data_list)
    assert excluded_recipe_data_list == [
        {
            'recipe_title': 'ホットクックで簡単ココナッツカレー',
            'recipe_ingredients': ['玉ねぎ', 'にんじん'],
            'recipe_url': 'recipe_url_1',
            'recipe_image_url': 'recipe_image_url_1',
        }
    ]


# エラーがない場合正しくデータを取得しているか確認
def test_scraping_and_excluding_normal():
    recipe_name = 'ココナッツカレー'
    recipe_url_1 = 'https://cookpad.com/recipe/7836445'
    recipe_url_2 = 'https://cookpad.com/recipe/7850799'
    recipe_image_url_1 = 'https://img.cpcdn.com/recipes/7836445/test_img_1'
    recipe_image_url_2 = 'https://img.cpcdn.com/recipes/7850799/test_img_2'
    allergy_list = ['いか']
    with patch('requests.get', side_effect=mock_side_effect):
        with patch('meal_shield.scrape.cookpad.Pool') as mock_pool:
            mock_pool.return_value.__enter__.return_value.map.side_effect = (
                lambda func, urls: [func(url) for url in urls]
            )
            excluded_recipe_data_list = scraping_and_excluding(
                allergy_list, recipe_name
            )

            assert excluded_recipe_data_list == [
                {
                    'recipe_title': 'ホットクックで簡単ココナッツカレー',
                    'recipe_ingredients': ['玉ねぎ', 'にんじん'],
                    'recipe_url': recipe_url_1,
                    'recipe_image_url': recipe_image_url_1,
                }
            ]


# ネットワーク接続エラーを補足するか確認
def test_scraping_and_excluding_connection_rror():
    recipe_name = 'ココナッツカレー'
    allergy_list = ['いか']

    # requests.get をモック化し、ConnectionError を発生させる
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        assert scraping_and_excluding(allergy_list, recipe_name) is None

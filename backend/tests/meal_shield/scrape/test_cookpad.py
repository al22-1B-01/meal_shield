import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests
from bs4 import BeautifulSoup

from meal_shield.scrape.cookpad import (
    make_url_list,
    scraping_cookpad,
    scraping_recipe_data,
    scraping_recipe_url,
)


# テキストファイルからHTMLを取得
def load_mock_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # レスポンスごとに分割
    responses = content.split('\n\n# ')
    return [resp.strip() for resp in responses if resp.strip()]


script_dir = Path(__file__).resolve().parent
mock_data_file_path = script_dir / 'test_case' / 'mock_data.txt'
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


# エラーがない場合正しくデータを取得しているか確認
def test_make_url_list_normal():
    recipe_name = 'ココナッツカレー'
    search_url = f'https://cookpad.com/search/{recipe_name}'
    with patch('requests.get', side_effect=mock_side_effect):
        url_list = make_url_list(recipe_name)
        assert url_list == [f'{search_url}?page=1', f'{search_url}?page=2']


# ネットワーク接続エラーを捕捉するか確認
def test_make_url_list_():
    recipe_name = 'カレー'
    # requests.get をモック化し、ConnectionError を発生させる
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        assert make_url_list(recipe_name) is None


# エラーがない場合正しくデータを取得しているか確認
def test_scraping_recipe_url_normal():
    url = 'https://cookpad.com/search/ココナッツカレー?page=1'
    with patch('requests.get', side_effect=mock_side_effect):
        recipe_url_list = scraping_recipe_url(url)
        assert recipe_url_list == ['https://cookpad.com/recipe/7836445']


# ネットワーク接続エラーを捕捉するか確認
def test_scraping_recipe_url_connection_error():
    url = 'https://cookpad.com/search/ココナッツカレー?page=1'
    # requests.get をモック化し、ConnectionError を発生させる
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        assert scraping_recipe_url(url) is None


# エラーがない場合正しくデータを取得しているか確認
def test_scraping_recipe_data_normal():
    url = 'https://cookpad.com/recipe/7836445'
    recipe_image_url = 'https://img.cpcdn.com/recipes/7836445/test_img_1'
    with patch('requests.get', side_effect=mock_side_effect):
        recipe_data = scraping_recipe_data(url)
        assert recipe_data == {
            'recipe_title': 'ホットクックで簡単ココナッツカレー',
            'recipe_ingredients': ['玉ねぎ', 'にんじん'],
            'recipe_url': url,
            'recipe_image_url': recipe_image_url,
        }


# ネットワーク接続エラーを補足するか確認
def test_scraping_recipe_data_connection_error():
    url = 'https://example.com/recipe'
    # requests.get をモック化し、ConnectionError を発生させる
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        assert scraping_recipe_data(url) is None


# エラーがない場合正しくデータを取得しているか確認
def test_scraping_cookpad_normal():
    recipe_name = 'ココナッツカレー'
    recipe_url_1 = 'https://cookpad.com/recipe/7836445'
    recipe_url_2 = 'https://cookpad.com/recipe/7850799'
    recipe_image_url_1 = 'https://img.cpcdn.com/recipes/7836445/test_img_1'
    recipe_image_url_2 = 'https://img.cpcdn.com/recipes/7850799/test_img_2'
    with patch('requests.get', side_effect=mock_side_effect):
        with patch('meal_shield.scrape.cookpad.Pool') as mock_pool:
            mock_pool.return_value.__enter__.return_value.map.side_effect = (
                lambda func, urls: [func(url) for url in urls]
            )
            recipes_list = scraping_cookpad(recipe_name)

            assert recipes_list == [
                {
                    'recipe_title': 'ホットクックで簡単ココナッツカレー',
                    'recipe_ingredients': ['玉ねぎ', 'にんじん'],
                    'recipe_url': recipe_url_1,
                    'recipe_image_url': recipe_image_url_1,
                },
                {
                    'recipe_title': '絶品！シーフードココナッツカレー',
                    'recipe_ingredients': ['いか', '海老'],
                    'recipe_url': recipe_url_2,
                    'recipe_image_url': recipe_image_url_2,
                },
            ]


# ネットワーク接続エラーを補足するか確認
def test_scraping_cookpad_conection_error():
    recipe_name = 'ココナッツカレー'
    # requests.get をモック化し、ConnectionError を発生させる
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        assert scraping_cookpad(recipe_name) is None

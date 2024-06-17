from unittest.mock import Mock, patch

import pytest
import requests
from bs4 import BeautifulSoup

from src.meal_shield.scrape.cookpad import (
    make_url_list,
    scraping_cookpad,
    scraping_recipe_data,
    scraping_recipe_url,
)

# モックHTMLデータ
mock_response_1 = Mock()
mock_response_1.text = '''
<html>
<body>
<div class='number_of_pages'>
1 / 2
</div>
<a class='recipe-title' id='recipe_title_7836445' href='/recipe/7836445'>ホットクックで簡単ココナッツカレー</a>
</body>
</html>
'''
mock_response_1.content = mock_response_1.text.encode('utf-8')

mock_response_2 = Mock()
mock_response_2.text = '''
<html>
<body>
<div class='number_of_pages'>
2 / 2
</div>
<a class='recipe-title' id='recipe_title_7850799' href='/recipe/7850799'>絶品！シーフードココナッツカレー</a>
</body>
</html>
'''
mock_response_2.content = mock_response_2.text.encode('utf-8')

mock_response_3 = Mock()
mock_response_3.text = '''
<html>
<body>
<h1 class='recipe-title'>
ホットクックで簡単ココナッツカレー
</h1>
<div class='ingredient_name'><span class='name'><a class='cookdict_ingredient_link' href='/search/%E7%8E%89%E3%81%AD%E3%81%8E'>玉ねぎ</a></span></div>
<div class='ingredient_name'><span class='name'><a class='cookdict_ingredient_link' href='/search/%E3%81%AB%E3%82%93%E3%81%98%E3%82%93'>にんじん</a></span></div>
<section id='main-photo'>
<img alt='ホットクックで簡単ココナッツカレーの画像' class='photo large_photo_clickable' data-large-photo='https://img.cpcdn.com/recipes/7836445/m/3dbaaed42b5b3c7bc188c23922314e3f?u=58079855&amp;p=1716460548' src='https://img.cpcdn.com/recipes/7836445/894x1461s/3f302487515646e913b639f8c12a210d?u=58079855&amp;p=1716460548' />
</section>
</body>
</html>
'''
mock_response_3.content = mock_response_3.text.encode('utf-8')

mock_response_4 = Mock()
mock_response_4.text = '''
<html>
<body>
<h1 class='recipe-title'>
絶品！シーフードココナッツカレー
</h1>
<div class='ingredient_name'><span class='name'><a class='cookdict_ingredient_link' href='/search/%E3%81%84%E3%81%8B'>いか</a></span></div>
<div class='ingredient_name'><span class='name'><a class='cookdict_ingredient_link' href='/search/%E6%B5%B7%E8%80%81'>海老</a></span></div>
<section id='main-photo'>
<img alt='絶品！シーフードココナッツカレーの画像' class='photo large_photo_clickable' data-large-photo='https://img.cpcdn.com/recipes/7850799/m/f04e522a5acc391dc4d7854b1e59af5e?u=58558241&amp;p=1717844234' src='https://img.cpcdn.com/recipes/7850799/894x1461s/5ad2fb50779e89741675024c20c02586?u=58558241&amp;p=1717844234' />
</section>
</body>
</html>
'''
mock_response_4.content = mock_response_4.text.encode('utf-8')


# モックのサイドエフェクト関数を定義
def mock_side_effect(url, *args, **kwargs):
    if url == 'https://cookpad.com/search/ココナッツカレー':
        return mock_response_1
    elif url == 'https://cookpad.com/search/ココナッツカレー?page=1':
        return mock_response_1
    elif url == 'https://cookpad.com/search/ココナッツカレー?page=2':
        return mock_response_2
    elif url == 'https://cookpad.com/recipe/7836445':
        return mock_response_3
    elif url == 'https://cookpad.com/recipe/7850799':
        return mock_response_4
    else:
        raise requests.exceptions.ConnectionError


def test_make_url_list_エラーがない場合正しくデータを取得しているか確認():
    recipe_name = 'ココナッツカレー'
    search_url = f'https://cookpad.com/search/{recipe_name}'
    with patch('requests.get', side_effect=mock_side_effect):
        url_list = make_url_list(recipe_name)
        assert url_list == [f'{search_url}?page=1', f'{search_url}?page=2']


def test_make_url_list_ネットワーク接続エラーを捕捉するか確認():
    recipe_name = 'カレー'

    # requests.get をモック化し、ConnectionError を発生させる
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(requests.exceptions.ConnectionError):
            make_url_list(recipe_name)


def test_make_url_list_HTTPErrorを捕捉するか確認():
    recipe_name = 'カレー'

    # requests.get をモック化し、HTTPError を発生させる
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Not Found"
        )
        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            make_url_list(recipe_name)


def test_scraping_recipe_url_エラーがない場合正しくデータを取得しているか確認():
    url = 'https://cookpad.com/search/ココナッツカレー?page=1'
    with patch('requests.get', side_effect=mock_side_effect):
        recipe_url_list = scraping_recipe_url(url)
        assert recipe_url_list == ['https://cookpad.com/recipe/7836445']


def test_scraping_recipe_url_ネットワーク接続エラーを捕捉するか確認():
    url = 'https://cookpad.com/search/ココナッツカレー?page=1'
    # requests.get をモック化し、ConnectionError を発生させる
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(requests.exceptions.ConnectionError):
            scraping_recipe_url(url)


def test_scraping_recipe_url_HTTPErrorを捕捉するか確認():
    url = 'https://cookpad.com/search/ココナッツカレー?page=1'
    # requests.get をモック化し、HTTPError を発生させる
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Not Found"
        )
        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            scraping_recipe_url(url)


def test_scraping_recipe_data_エラーがない場合正しくデータを取得しているか確認():
    url = 'https://cookpad.com/recipe/7836445'
    recipe_img_url = 'https://img.cpcdn.com/recipes/7836445/894x1461s/3f302487515646e913b639f8c12a210d?u=58079855&p=1716460548'
    with patch('requests.get', side_effect=mock_side_effect):
        recipe_data = scraping_recipe_data(url)
        assert recipe_data == {
            'recipe_title': 'ホットクックで簡単ココナッツカレー',
            'ingredient_list': ['玉ねぎ', 'にんじん'],
            'recipe_url': url,
            'recipe_img_url': recipe_img_url,
        }


def test_scraping_recipe_data_ネットワーク接続エラーを補足するか確認():
    url = 'https://example.com/recipe'

    # requests.get をモック化し、ConnectionError を発生させる
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(requests.exceptions.ConnectionError):
            scraping_recipe_data(url)


def test_scraping_recipe_data_HTTPErrorを補足するか確認():
    url = 'https://example.com/recipe'

    # requests.get をモック化し、HTTPError を発生させる
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            '404 Not Found'
        )
        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            scraping_recipe_data(url)


def test_scraping_cookpad_エラーがない場合正しくデータを取得しているか確認():
    recipe_name = 'ココナッツカレー'
    recipe_url_1 = 'https://cookpad.com/recipe/7836445'
    recipe_url_2 = 'https://cookpad.com/recipe/7850799'
    recipe_img_url_1 = 'https://img.cpcdn.com/recipes/7836445/894x1461s/3f302487515646e913b639f8c12a210d?u=58079855&p=1716460548'
    recipe_img_url_2 = 'https://img.cpcdn.com/recipes/7850799/894x1461s/5ad2fb50779e89741675024c20c02586?u=58558241&p=1717844234'
    with patch('requests.get', side_effect=mock_side_effect):
        with patch('src.meal_shield.scrape.cookpad.Pool') as mock_pool:
            mock_pool.return_value.__enter__.return_value.map.side_effect = (
                lambda func, urls: [func(url) for url in urls]
            )
            recipe_data_list = scraping_cookpad(recipe_name)

            assert recipe_data_list == [
                {
                    'recipe_title': 'ホットクックで簡単ココナッツカレー',
                    'ingredient_list': ['玉ねぎ', 'にんじん'],
                    'recipe_url': recipe_url_1,
                    'recipe_img_url': recipe_img_url_1,
                },
                {
                    'recipe_title': '絶品！シーフードココナッツカレー',
                    'ingredient_list': ['いか', '海老'],
                    'recipe_url': recipe_url_2,
                    'recipe_img_url': recipe_img_url_2,
                },
            ]


def test_scraping_cookpad_ネットワーク接続エラーを補足するか確認():
    recipe_name = 'ココナッツカレー'

    # requests.get をモック化し、ConnectionError を発生させる
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(requests.exceptions.ConnectionError):
            scraping_cookpad(recipe_name)


def test_scraping_cookpad_HTTPErrorを補足するか確認():
    recipe_name = 'ココナッツカレー'

    # requests.get をモック化し、HTTPError を発生させる
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            '404 Not Found'
        )
        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            scraping_cookpad(recipe_name)

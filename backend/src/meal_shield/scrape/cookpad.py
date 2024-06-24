from multiprocessing import Pool, cpu_count
from typing import Optional, Union

import requests
from bs4 import BeautifulSoup

# 検索上限(page数)
LIMIT_PAGE = 10


def scraping_cookpad(
    recipe_name: str,
) -> Optional[list[dict[str, Union[str, list[str]]]]]:
    # 検索結果ページのURLリストを取得
    page_url_list = make_url_list(recipe_name)
    if page_url_list is None:
        return None
    # それぞれのページのURLからレシピのURLを並列処理で取得
    num_cpu = cpu_count()
    with Pool(num_cpu) as pool:
        recipe_url_lists = pool.map(scraping_recipe_url, page_url_list)
    # URLのリストを結合
    recipe_url_list = [item for sublist in recipe_url_lists for item in sublist]
    # それぞれのレシピのURLからデータを並列処理で取得
    with Pool(num_cpu) as pool:
        recipes_list = pool.map(scraping_recipe_data, recipe_url_list)
    return recipes_list


def make_url_list(recipe_name: str) -> Optional[list[str]]:
    # 検索結果の最初のページのURL
    url = f'https://cookpad.com/search/{recipe_name}'
    response = requests.get(url)

    # 検索結果が存在するとき
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        # 1 / 1,000のような現在のページを表す文字列を取得
        number_of_pages = soup.find(class_='number_of_pages').text
        page_parts = number_of_pages.split(' / ')
        sum_of_pages = int(page_parts[1].replace(',', ''))

        # 検索上限を設定
        if sum_of_pages > LIMIT_PAGE:
            sum_of_pages = LIMIT_PAGE

        url_list = []
        # ページ数分だけURLを作成
        for page_num in range(1, sum_of_pages + 1):
            new_url = f'{url}?page={page_num}'
            url_list.append(new_url)
        return url_list
    else:
        return None


def scraping_recipe_url(url: str) -> list[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    recipe_url_list = []
    # レシピのURLを属性に持つ<a>タグをすべて取得
    a_tags = soup.find_all('a', class_='recipe-title')
    for a_tag in a_tags:
        # 各<a>タグのhref属性(URL)を取得
        href = a_tag.get('href')
        # 会員登録が必要なレシピを除外
        if 'dining' not in href:
            recipe_url_list.append(f'https://cookpad.com{href}')
    return recipe_url_list


def scraping_recipe_data(url: str) -> list[dict[str, Union[str, list[str]]]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    # レシピのタイトルである<h1>タグのテキストを取得
    recipe_title = soup.find('h1', class_='recipe-title').get_text(strip=True)
    # 全角スペースを半角スペースに置き換える
    recipe_title = recipe_title.replace('\u3000', ' ')

    recipe_ingredients = []
    # 材料のデータを含む<span>タグの要素をすべて取得
    spans = soup.find_all('span', class_='name')
    for span in spans:
        # 材料は<span>タグかその中の<a>タグにあるので場合分け
        a_tag = span.find('a')
        if a_tag is None:
            ingredient_name = span.text
        else:
            ingredient_name = a_tag.text
        recipe_ingredients.append(ingredient_name)

    # レシピ画像のURLを属性に持つ<img>タグを含む<section>タグを取得
    section_tag = soup.find('section', id='main-photo')
    # レシピ画像のURLを属性に持つ<img>タグを取得
    img_tag = section_tag.find('img')
    # <img>タグのsrc属性(レシピ画像のURL)を取得
    recipe_image_url = img_tag.get('src')

    recipe_data = {
        'recipe_title': recipe_title,
        'recipe_ingredients': recipe_ingredients,
        'recipe_url': url,
        'recipe_image_url': recipe_image_url,
    }
    return recipe_data

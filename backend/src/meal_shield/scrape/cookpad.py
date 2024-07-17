import asyncio
from typing import Final, Optional, Union

import aiohttp
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm.asyncio import tqdm

# 検索上限(page数)
LIMIT_PAGE: Final[int] = 30
SEMAPHORE_LIMIT: Final[int] = 1000

semaphore: asyncio.Semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)


@retry(stop=stop_after_attempt(1), wait=wait_fixed(1), reraise=True)
async def scraping_cookpad(
    recipe_name: str,
) -> Optional[list[dict[str, Union[str, list[str]]]]]:
    """クックパッドの検索結果を辞書型リストで返す

    recipe_nameで検索した結果の各ページからレシピのURLをスクレイプする。
    そのURLからタイトル、材料、レシピ画像のURLをスクレイプして、
    それらを辞書型リストに格納し値を返す。

    それぞれのスクレイプ実行時に結果が見つからない場合はNoneを返す。

    :param str recipe_name: 検索フィールドに入力されたレシピ名
    :return: クックパッドの検索結果を辞書型のデータとしてで返す
    :rtype: Optional[list[dict[str, Union[str, list[str]]]]]
    """

    # 検索結果ページのURLリストを取得
    page_url_list = make_url_list(recipe_name)
    if page_url_list is None:
        return None
    # それぞれのページのURLからレシピのURLを並列処理で取得
    async with aiohttp.ClientSession() as session:
        tasks = [scraping_recipe_url(session, url) for url in page_url_list]
        recipe_url_lists = []
        for f in tqdm.as_completed(tasks, desc="Fetching recipe_urls"):
            result = await f
            recipe_url_lists.append(result)
    if recipe_url_lists is None:
        return None

    # URLのリストを結合
    recipe_url_list = [item for sublist in recipe_url_lists for item in sublist]
    # それぞれのレシピのURLからデータを並列処理で取得
    async with aiohttp.ClientSession() as session:
        tasks = [scraping_recipe_data(session, url) for url in recipe_url_list]
        recipes_list = []
        for f in tqdm.as_completed(tasks, desc="Fetching recipe_data"):
            result = await f
            recipes_list.append(result)
    if recipes_list is None:
        return None
    else:
        return recipes_list


@retry(stop=stop_after_attempt(1), wait=wait_fixed(1), reraise=True)
def make_url_list(recipe_name: str) -> Optional[list[str]]:
    """レシピ名で検索するURLを作成。

    検索結果がない場合はNoneを返す。

    :param str recipe_name: 入力されたレシピ名
    :return: 検索結果表示ページのURLが格納されたリスト
    :rtype: Optional[list[str]]
    """

    try:
        # 検索結果の最初のページのURL
        url = f'https://cookpad.com/search/{recipe_name}'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml', from_encoding="utf-8")
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
    except Exception as e:
        return None


@retry(stop=stop_after_attempt(1), wait=wait_fixed(1), reraise=True)
async def scraping_recipe_url(
    session: aiohttp.ClientSession, url: str
) -> Optional[list[str]]:
    """検索結果からレシピのURLを取得

    非同期で検索結果ページからレシピのURLを取得する。

    エラーが起きたらNoneを返す。

    :param session: リクエストを行うために使用するaiohttpセッション
    :type session aiohttp.ClientSession
    :return: レシピのURLが格納されたリスト
    :rtype: Optional[list[str]]
    """

    async with semaphore:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                content = await response.text()
                soup = BeautifulSoup(content, 'lxml', from_encoding="utf-8")

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
        except Exception as e:
            return None


@retry(stop=stop_after_attempt(1), wait=wait_fixed(1), reraise=True)
async def scraping_recipe_data(
    session: aiohttp.ClientSession, url: str
) -> Optional[dict[str, Union[str, list[str]]]]:
    """レシピのURLからレシピのデータを取得

    非同期でレシピのURLからレシピのタイトル、材料のリスト、レシピ画像のURLを
    スクレイプし辞書型のリストにこれらとレシピのURLを格納して返す。

    辞書型のキー: {
    'recipe_title': str,
    'recipe_ingredients': list[str],
    'recipe_url': str,
    'recipe_image_url': str
    }


    :param session: リクエストを行うために使用するaiohttpセッション
    :type session aiohttp.ClientSession
    :param str url: レシピのURL
    """

    async with semaphore:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                content = await response.text()

                soup = BeautifulSoup(content, 'lxml')

                # レシピのタイトルである<h1>タグのテキストを取得
                recipe_title = soup.find('h1', class_='recipe-title').get_text(
                    strip=True
                )
                # 全角スペースを半角スペースに置き換える
                recipe_title = recipe_title.replace('\u3000', ' ')

                recipe_ingredients = []
                ingredient_categories = soup.select('.ingredient_category')
                ingredient_names = soup.select('.ingredient_name .name')

                for name in ingredient_names:
                    clean_text = name.text.replace('■', '').replace('☆', '').strip()
                    recipe_ingredients.append(clean_text)

                # カテゴリーを含む場合、材料に'カテゴリー'を追加(除外処理で弾くため)
                if len(ingredient_categories) > 0:
                    recipe_ingredients.append('カテゴリー')

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
        except Exception as e:
            return None

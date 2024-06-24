import logging
from typing import Optional, Union

import requests

from meal_shield.scrape.cookpad import scraping_cookpad

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# テスト用main関数
def main():
    recipe_name = 'ココナッツカレー'
    allergy_list = ['鶏', 'とり']
    recipe_data_list = scraping_and_excluding(allergy_list, recipe_name)
    if recipe_data_list is not None:
        for index, recipe_data in enumerate(recipe_data_list):
            logger.info(index + 1)
            logger.info(recipe_data['recipe_title'])
            logger.info(recipe_data['ingredient_list'])
            logger.info(recipe_data['recipe_url'])
            logger.info(recipe_data['recipe_img_url'])
        logger.info(f'検索結果{len(recipe_data_list)}件')
        logger.info(f'検索レシピ名:{recipe_name}')
        logger.info(f'除外品目:{allergy_list}')
    else:
        logger.error('エラーが起きました')


def scraping_and_excluding(
    allergy_list: list[str], recipe_name: str
) -> Optional[dict[str, Union[str, list[str]]]]:
    recipe_data_list = scraping_cookpad(recipe_name)
    if recipe_data_list is not None:
        excluded_recipe_data_list = excluding(allergy_list, recipe_data_list)
        return excluded_recipe_data_list
    else:
        return None


# 文字列がリストに含まれる文字列を含むか判別
def contains_any(string: str, substrings: list[str]) -> bool:
    return any(substring in string for substring in substrings)


# 文字列リストにリストの文字列が含まれるか判別
def contains_any_in_list(strings: list[str], substrings: list[str]) -> bool:
    return any(contains_any(string, substrings) for string in strings)


def excluding(allergy_list: list[str], recipe_data_list: list[dict]) -> list[dict]:
    # 材料にアレルギーを含む要素を除外
    excluded_recipe_data_list = [
        recipe_data
        for recipe_data in recipe_data_list
        if not contains_any_in_list(recipe_data['ingredient_list'], allergy_list)
    ]
    return excluded_recipe_data_list

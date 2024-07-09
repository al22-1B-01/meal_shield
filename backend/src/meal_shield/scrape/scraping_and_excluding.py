from typing import Final, Optional, Union

import asyncio
from meal_shield.scrape.cookpad import scraping_cookpad
from tqdm.asyncio import tqdm


MAX_RECIPE_SIZE: Final[int] = 100


async def scraping_and_excluding(
    allergy_list: list[str], recipe_name: str
) -> Optional[list[dict[str, Union[str, list[str]]]]]:
    recipes_list = await scraping_cookpad(recipe_name)
    if recipes_list is not None:
        excluded_recipes_list = excluding_recipe(allergy_list, recipes_list)
        return excluded_recipes_list
    else:
        return None


# 文字列がリストに含まれる文字列を含むか判別
def contains_any(string: str, substrings: list[str]) -> bool:
    return any(substring in string for substring in substrings)


# 文字列リストにリストの文字列が含まれるか判別
def contains_any_in_list(strings: list[str], substrings: list[str]) -> bool:
    return any(contains_any(string, substrings) for string in strings)


def excluding_recipe(allergy_list: list[str], recipes_list: list[dict]) -> list[dict]:
    # 材料にアレルギーを含む要素を除外
    excluded_recipes_list = [
        recipe_data
        for recipe_data in tqdm(recipes_list, desc="Filtering recipes")
        if not contains_any_in_list(recipe_data['recipe_ingredients'], allergy_list)
    ]
    return excluded_recipes_list[:MAX_RECIPE_SIZE]

async def main():
    recipes = await scraping_and_excluding(['', '芋', 'チョコ', '鳥'], 'カレー')
    print(len(recipes))

if __name__ == "__main__":
    asyncio.run(main())

from meal_shield.scrape.cookpad import scraping_cookpad


def scraping_and_excluding(allergy_list, recipe_name: str) -> list[dict]:
    recipe_data_list = scraping_cookpad(recipe_name)
    if recipe_data_list is not None:
        excluded_recipe_data_list = excluding(allergy_list, recipe_data_list)
    else:
        return recipe_data_list
    return excluded_recipe_data_list


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

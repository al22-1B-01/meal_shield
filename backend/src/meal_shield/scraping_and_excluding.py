from typing import List

from scrape import cookpad


# テスト用main関数
def main():
    recipe_name = 'ココナッツカレー'
    allergy_list = ['鶏', 'とり']

    recipe_data_list = scraping_and_excluding(allergy_list, recipe_name)
    
    if recipe_data_list is not None:
        for recipe_data in recipe_data_list:
            print(f"{recipe_data['recipe_title']}")
            print(f"{recipe_data['ingredient_list']}")
            print(f"{recipe_data['recipe_url']}")
            print(f"{recipe_data['recipe_img_url']}\n")
        print(f'検索結果{len(recipe_data_list)}件')
        print(f'検索レシピ名:{recipe_name}\n除外品目:\n{allergy_list}')
    else:
        print(recipe_data_list)
        print('検索結果が見つかりませんでした')


def scraping_and_excluding(allergy_list, recipe_name: str):
    recipe_data_list = cookpad.scraping_cookpad(recipe_name)
    if recipe_data_list is not None:
        excluded_recipe_data_list = excluding(allergy_list, recipe_data_list)
    else:
        return recipe_data_list
    return excluded_recipe_data_list


# 文字列がリストに含まれる文字列を含むか判別
def contains_any(string: str, substrings: List[str]) -> bool:
    return any(substring in string for substring in substrings)


# 文字列リストにリストの文字列が含まれるか判別
def contains_any_in_list(strings: List[str], substrings: List[str]) -> bool:
    # リストの要素の判別結果をboolリストに格納
    results = [contains_any(string, substrings) for string in strings]
    for result in results:
        if result:
            return True
    return False


def excluding(allergy_list: List[str], recipe_data_list: List[dict]):
    # 材料にアレルギーを含む要素を除外
    excluded_recipe_data_list = [
        recipe_data for recipe_data in recipe_data_list
        if not contains_any_in_list(
            recipe_data['ingredient_list'], allergy_list
        )
    ]
    return excluded_recipe_data_list


if __name__ == '__main__':
    main()

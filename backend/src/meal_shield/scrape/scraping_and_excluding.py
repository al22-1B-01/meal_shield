from typing import Final, Optional, Union

from tqdm.asyncio import tqdm

from meal_shield.scrape.cookpad import scraping_cookpad

MAX_RECIPE_SIZE: Final[int] = 100


async def scraping_and_excluding(
    allergy_list: list[str], recipe_name: str
) -> Optional[list[dict[str, Union[str, list[str]]]]]:
    """レシピ名とアレルギーリストからアレルギーを除外したレシピのデータを返す

    検索結果が存在しないときNoneを返す

    :param list[str] allergy_list: 選択されたアレルギーのリスト
    :param str recipe_name: 入力されたレシピ名
    :return: アレルギーを除外したレシピのデータが辞書型リストで格納されたデータ
    :rtype: Optional[list[dict[str, Union[str, list[str]]]]]
    """

    recipes_list = await scraping_cookpad(recipe_name)
    if recipes_list is not None:
        excluded_recipes_list = excluding_recipe(allergy_list, recipes_list)
        if excluded_recipes_list is not None:
            return excluded_recipes_list
        else:
            return None
    else:
        return None


def contains_any(string: str, substrings: list[str]) -> bool:
    """文字列がリストの文字列を含むか判別

    substringsの要素とstringを比較して、文字列が含まれる場合
    Tureを返し、含まれない場合Falseを返す

    :param str string: 比較される文字列
    :param list[str]:substrings比較する文字列のリスト
    """

    return any(substring in string for substring in substrings)


def contains_any_in_list(strings: list[str], substrings: list[str]) -> bool:
    """文字列リストの要素がリストに含まれる文字列を含むか判別

    stringのすべての要素に対して
    contains_anyを実行してTrueがある場合Trueを返し、それ以外はFalseを返す。

    :param list[str] string: リストの文字列と比較される文字列のリスト
    :param list[str] substrings: 比較する文字列のリスト
    """

    return any(contains_any(string, substrings) for string in strings)


def excluding_recipe(allergy_list: list[str], recipes_list: list[dict]) -> list[dict]:
    """レシピのデータからアレルギーを含むレシピを除外する

    recipes_listの各要素に対してcontains_any_in_listを材料に対して実行し、
    Falseを返したレシピだけリストに追加する

    :param list[str] allergy_list: 選択されたアレルギーのリスト
    :param recipes_list: 除外処理を行っていないレシピデータ
    :type recipe_list: Optional[list[dict[str, Union[str, list[str]]]]]
    """

    # 材料にアレルギーを含むレシピとカテゴリーを含むレシピを除外
    allergy_list.append('カテゴリー')
    excluded_recipes_list = [
        recipe_data
        for recipe_data in tqdm(recipes_list, desc="Filtering recipes")
        if not contains_any_in_list(recipe_data['recipe_ingredients'], allergy_list)
    ]
    return excluded_recipes_list[:MAX_RECIPE_SIZE]

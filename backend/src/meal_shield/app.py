"""概要

    説明
    fastapiを利用してapi化を行う
    WORDSはアレルギー品目を詳細化したもの
    serch_allergyで詳細情報を取得
    get_recipeでレシピを取得
    anking_recipeはレシピに順位付けしたもの
    scraping_and_excluding:cookpadからレシピをスクレイピング

"""
from typing import Final, Optional

import nest_asyncio
from fastapi import FastAPI, Query

from meal_shield.ranking.ranking import ranking_recipe
from meal_shield.scrape.scraping_and_excluding import scraping_and_excluding

nest_asyncio.apply()

app = FastAPI()
WORDS: Final[dict[str, list[str]]] = {
    'えび': ['えび', 'エビ', '海老'],
    'かに': ['かに', 'カニ', '蟹'],
    '小麦': ['小麦'],
    'そば': ['そば', 'ソバ', '蕎麦'],
    'たまご': ['卵', '卵白', 'マヨネーズ', 'たまご', 'タマゴ', '玉子'],
    '乳': ['牛乳', 'チーズ', 'ヨーグルト', 'バター', '生クリーム', '乳'],
    '落花生': ['落花生'],
    'アーモンド': ['アーモンド'],
    'あわび': ['あわび', 'アワビ'],
    'いか': ['いか', 'イカ'],
    'いくら': ['いくら', 'イクラ'],
    'オレンジ': ['オレンジ'],
    'カシューナッツ': ['カシューナッツ'],
    'キウイフルーツ': ['キウイフルーツ', 'キウイ'],
    '牛': ['牛', 'ビーフ'],
    'くるみ': ['くるみ', 'クルミ'],
    'ごま': ['ごま', 'ゴマ', '胡麻'],
    'さけ': ['さけ', 'サケ', '鮭', 'しゃけ', 'サーモン'],
    'さば': ['さば', 'サバ', '鯖'],
    '大豆': ['大豆', '豆腐', '厚揚げ', '油揚げ', '納豆', 'きなこ', 'きな粉'],
    '鶏': ['鶏', 'チキン', '鳥', 'とり'],
    'バナナ': ['バナナ'],
    '豚': ['豚', 'ポーク', 'ぶた'],
    'まつたけ': ['まつたけ', 'マツタケ', '松茸'],
    'もも': ['もも', 'モモ', '桃'],
    'やまいも': ['やまいも', '山芋', 'ヤマイモ'],
    'りんご': ['りんご', 'リンゴ', '林檎'],
    'ゼラチン': ['ゼラチン'],
}


def serch_allergy(allergy_list: list[str]) -> list[list[str]]:
    """概要

    説明
    param:allergy_list;選択されたアレルギー品目
    type:allergy_list:list[str]
    return:WORDSからallergy_listから取得
    rtype:list[list[str]]

    """
    allergu_search = []
    for item in allergy_list:
        if item in WORDS:
            allergu_search.extend(WORDS[item])
    return allergu_search


@app.get("/")
async def get_recipe(
    recipe: str, allergy_list: Optional[list[str]] = Query(default=None)
) -> list:
    """概要

    説明
    param:recipe:入力されたレシピ
    type:recipe:str
    paras:allergy_list:選択されたアレルギー品目
    type:list
    return:順位付けされたレシピをかえす
    rtype:list[dict[str, Union[str, list[str]]]]

    """
    if allergy_list is None:
        return [{'status': 'error', 'message': 'No allergy list', 'data': []}]

    allergy_found = serch_allergy(allergy_list)

    allergy_remove = await scraping_and_excluding(
        recipe_name=recipe, allergy_list=allergy_found
    )
    if allergy_remove is None:
        return [{'status': 'error', 'message': 'No recipe', 'data': []}]

    rank_recipe = await ranking_recipe(
        allergy_found, excluded_recipes_list=allergy_remove
    )
    return rank_recipe

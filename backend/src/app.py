from typing import Optional

import nest_asyncio
from fastapi import FastAPI, Query

from meal_shield.ranking.ranking import ranking_recipe
from meal_shield.scrape.scraping_and_excluding import scraping_and_excluding

nest_asyncio.apply()

app = FastAPI()
WORDS = {
    'えび': ['えび', 'エビ', '海老'],
    'かに': ['かに', 'カニ', '蟹'],
    '小麦': ['小麦'],
    'そば': ['そば', 'ソバ', '蕎麦'],
    'たまご': ['卵', '卵白', 'マヨネーズ', 'たまご', 'タマゴ'],
    '乳': ['牛乳', 'チーズ', 'ヨーグルト', 'バター', '生クリーム', '乳'],
    '落花生': ['落花生'],
    'アーモンド': ['アーモンド'],
    'あわび': ['あわび', 'アワビ'],
    'いか': ['いか', 'イカ'],
    'いくら': ['いくら', 'イクラ'],
    'オレンジ': ['オレンジ'],
    'カシューナッツ': ['カシューナッツ'],
    'キウイフルーツ': ['キウイフルーツ', 'キウイ'],
    '牛肉': ['牛肉'],
    'くるみ': ['くるみ', 'クルミ'],
    'ごま': ['ごま', 'ゴマ', '胡麻'],
    'さけ': ['さけ', 'サケ', '鮭', 'しゃけ', 'サーモン'],
    'さば': ['さば', 'サバ', '鯖'],
    '大豆': ['大豆', '豆腐', '厚揚げ', '油揚げ', '納豆', 'きなこ', 'きな粉'],
    '鶏肉': ['鶏肉'],
    'バナナ': ['バナナ'],
    '豚肉': ['豚肉'],
    'まつたけ': ['まつたけ', 'マツタケ', '松茸'],
    'もも': ['もも', 'モモ', '桃'],
    'やまいも': ['やまいも', '山芋', 'ヤマイモ'],
    'りんご': ['りんご', 'リンゴ', '林檎'],
    'ゼラチン': ['ゼラチン'],
}


def serch_allergy(allergy_list: list[str]) -> list[list[str]]:
    allergu_search = []
    for item in allergy_list:
        if item in WORDS:
            allergu_search.extend(WORDS[item])
    return allergu_search


@app.get("/")
async def get_recipi(
    recipi: str, allergy_list: Optional[list[str]] = Query(default=None)
) -> list:
    if allergy_list is None:
        return [{'status': 'error', 'message': 'No allergy list', 'data': []}]
    allergy_found = serch_allergy(allergy_list)
    if recipi is None:
        return [{'status': 'error', 'message': 'No recipi', 'data': []}]
    allergy_remove = scraping_and_excluding(
        recipe_name=recipi, allergy_list=allergy_found
    )
    rank_recipi = await ranking_recipe(
        allergy_found, excluded_recipes_list=allergy_remove
    )
    return rank_recipi

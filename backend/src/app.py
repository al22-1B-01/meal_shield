from typing import Union

from fastapi import FastAPI

from meal_shield.ranking import ranking
from meal_shield.scrape.scraping_and_excluding import scraping_and_exclude

app = FastAPI()

WORDS = {
    'えび': ['えび', 'エビ', '海老'],
    'かに': ['かに', 'カニ', '蟹'],
    '小麦': ['小麦'],
    'そば': ['そば', 'ソバ', '蕎麦'],
    '卵': ['卵', '卵白', 'マヨネーズ'],
    '乳': ['牛乳', 'チーズ', 'ヨーグルト', 'バター', '生クリーム'],
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


async def serch_allergy(allergy_list: list[str]) -> list[list[str]]:
    allergu_search = []
    for item in allergy_list:
        if item in WORDS:
            allergu_search.append(WORDS[item])
    return allergu_search


@app.get("/get")
async def get_recipi(
    recipi: str = None, allergy_list: list[str] = None
) -> list[dict[str, Union[str, list[str]]]]:
    allergy_found = serch_allergy(allergy_list)

    if recipi is None:
        return [{'status': 'error', 'message': 'No recipi', 'data': []}]

    allergy_remove = scraping_and_exclude(recipi, allergy_found)
    rank_recipi = ranking.ranking_recipi(allergy_found, allergy_remove)

    return rank_recipi

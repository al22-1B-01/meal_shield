from typing import Optional, Dict, List, Union
from fastapi import FastAPI

app = FastAPI()

# WORDS = {
#     "えび": ["えび", "エビ", "海老"],
#     "かに": ["かに", "カニ", "蟹"],
#     "小麦": ["小麦"],
#     "そば": ["そば", "ソバ", "蕎麦"],
#     "卵": ["卵", "卵白", "マヨネーズ"],
#     "乳": ["牛乳", "チーズ", "ヨーグルト", "バター", "生クリーム"],
#     "落花生": ["落花生"],
#     "アーモンド": ["アーモンド"],
#     "あわび": ["あわび", "アワビ"],
#     "いか": ["いか", "イカ"],
#     "いくら": ["いくら", "イクラ"],
#     "オレンジ": ["オレンジ"],
#     "カシューナッツ": ["カシューナッツ"],
#     "キウイフルーツ": ["キウイフルーツ", "キウイ"],
#     "牛肉": ["牛肉"],
#     "くるみ": ["くるみ", "クルミ"],
#     "ごま": ["ごま", "ゴマ", "胡麻"],
#     "さけ": ["さけ", "サケ", "鮭", "しゃけ", "サーモン"],
#     "さば": ["さば", "サバ", "鯖"],
#     "大豆": ["大豆", "豆腐", "厚揚げ", "油揚げ", "納豆", "きなこ", "きな粉"],
#     "鶏肉": ["鶏肉"],
#     "バナナ": ["バナナ"],
#     "豚肉": ["豚肉"],
#     "まつたけ": ["まつたけ", "マツタケ", "松茸"],
#     "もも": ["もも", "モモ", "桃"],
#     "やまいも": ["やまいも", "山芋", "ヤマイモ"],
#     "りんご": ["りんご", "リンゴ", "林檎"],
#     "ゼラチン": ["ゼラチン"],
# }


# async def serch_allergy(allergy_list: List[str]) -> List[List[str]]:
#     allergu_search = []
#     for item in allergy_list:
#         if item in WORDS:
#             allergu_search.append(WORDS[item])
#     return allergu_search


@app.get("/get")
async def get_recipi(
    recipi: str = None, allergy_list: list[str] = None
) -> List[Dict[str, Union[str, list[str]]]]:
    if recipi == None:
        return [{"status": "error", "message": "No recipi", "data": []}]

    return scraping_and_exclude(recipi, allergy_list)


# 沖井さんが実装終了したらその関数に飛ばせるようにする
def scraping_and_exclude(recipi, allergy_list):
    return [recipi, allergy_list]

from typing import Optional, Dict, List
from backend.src.app import FastAPI

app = FastAPI()

WORDS = {
    "えび": ["えび", "エビ", "海老"],
    "かに": ["かに", "カニ", "蟹"],
    "小麦": ["小麦"],
    "そば": ["そば", "ソバ", "蕎麦"],
    "卵": ["卵", "卵白", "マヨネーズ"],
    "乳": ["牛乳", "チーズ", "ヨーグルト", "バター", "生クリーム"],
    "落花生": ["落花生"],
    "アーモンド": ["アーモンド"],
    "あわび": ["あわび", "アワビ"],
    "いか": ["いか", "イカ"],
    "いくら": ["いくら", "イクラ"],
    "オレンジ": ["オレンジ"],
    "カシューナッツ": ["カシューナッツ"],
    "キウイフルーツ": ["キウイフルーツ", "キウイ"],
    "牛肉": ["牛肉"],
    "くるみ": ["くるみ", "クルミ"],
    "ごま": ["ごま", "ゴマ", "胡麻"],
    "さけ": ["さけ", "サケ", "鮭", "しゃけ", "サーモン"],
    "さば": ["さば", "サバ", "鯖"],
    "大豆": ["大豆", "豆腐", "厚揚げ", "油揚げ", "納豆", "きなこ", "きな粉"],
    "鶏肉": ["鶏肉"],
    "バナナ": ["バナナ"],
    "豚肉": ["豚肉"],
    "まつたけ": ["まつたけ", "マツタケ", "松茸"],
    "もも": ["もも", "モモ", "桃"],
    "やまいも": ["やまいも", "山芋", "ヤマイモ"],
    "りんご": ["りんご", "リンゴ", "林檎"],
    "ゼラチン": ["ゼラチン"],
}


async def serch_allergy(allergy_list: List[str]) -> List[List[str]]:
    allergu_search = []
    index = 0
    for item in WORDS:
        if allergy_list[index] == item:
            index += 1
            allergu_search.append(WORDS.get(item))
    return allergu_search


@app.get("/get")
async def get_recipi(
    recipi: str = None, allergy: list[str] = None
) -> Dict[str, List[List[str]]]:  # クエリパラメータを使いたい
    allergy_list = serch_allergy(allergy)
    if recipi == None:
        return ["error", None]

    return scraping(recipi, allergy_list)


# 沖井さんが実装終了したらその関数に飛ばせるようにする
def scraping(recipi, allergy_list):
    return [recipi, allergy_list]

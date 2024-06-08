import logging
from typing import Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Make rule base count score func
ALLERGIES = {
    'えび': ['えび', 'エビ', '海老'],
    'かに': ['かに', 'カニ', '蟹'],
    '小麦': ['小麦', '醤油', 'しょうゆ'],
    'そば': ['そば', 'ソバ', '蕎麦'],
    '卵': ['卵', '卵白', 'マヨネーズ'],
    '乳': ['牛乳', 'チーズ', 'ヨーグルト', 'バター', '生クリーム', 'マーガリン'],
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
    'ごま': ['ごま', 'ゴマ', '胡麻', 'ごま油', 'ゴマ油', '胡麻油'],
    'さけ': ['さけ', 'サケ', '鮭', 'しゃけ', 'サーモン'],
    'さば': ['さば', 'サバ', '鯖'],
    '大豆': ['大豆', '豆腐', '厚揚げ', '油揚げ', '納豆', 'きなこ', 'きな粉', '醤油', 'しょうゆ', '味噌', 'みそ'],
    '鶏肉': ['鶏肉'],
    'バナナ': ['バナナ'],
    '豚肉': ['豚肉'],
    'まつたけ': ['まつたけ', 'マツタケ', '松茸'],
    'もも': ['もも', 'モモ', '桃'],
    'やまいも': ['やまいも', '山芋', 'ヤマイモ'],
    'りんご': ['りんご', 'リンゴ', '林檎'],
    'ゼラチン': ['ゼラチン'],
}


def extract_allergy_words(
    words_dict: dict[str, list[str]], allergies_list: list[str]
) -> list[str]:
    result = []
    for key in allergies_list:
        result.extend(words_dict[key])
    return result


def score_allergens(
    excluded_recipes_list: list[dict[str, Union[str, list[str]]]],
    allergies_list: list[str],
) -> dict[str, float]:
    extracted_allergies_list = extract_allergy_words(ALLERGIES, allergies_list)
    result = {}

    for recipe in excluded_recipes_list:
        allergen_counts = 0
        recipe_title = recipe["recipe_title"]
        ingredients = recipe["recipe_ingredients"]
        for allergen in extracted_allergies_list:
            allergen_counts += ingredients.count(allergen)

        result[recipe_title] = allergen_counts

    return result

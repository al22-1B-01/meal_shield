from multiprocessing import Pool, cpu_count
from typing import Final, Optional, Union

from tqdm.auto import tqdm

WORDS: Final[dict[str, list[str]]] = {
    'えび': ['えび', 'エビ', '海老'],
    'かに': ['かに', 'カニ', '蟹'],
    '小麦': ['小麦', '醤油', 'しょうゆ', '小麦粉'],
    'そば': ['そば', 'ソバ', '蕎麦', 'そば粉', '蕎麦粉'],
    'たまご': ['卵', '卵白', 'マヨネーズ', 'たまご', 'タマゴ'],
    '乳': ['牛乳', 'チーズ', 'ヨーグルト', 'バター', '生クリーム', 'マーガリン'],
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
    'ごま': ['ごま', 'ゴマ', '胡麻', 'ごま油', 'ゴマ油', '胡麻油'],
    'さけ': ['さけ', 'サケ', '鮭', 'しゃけ', 'サーモン'],
    'さば': ['さば', 'サバ', '鯖'],
    '大豆': ['大豆', '豆腐', '厚揚げ', '油揚げ', '納豆', 'きなこ', 'きな粉', '醤油', 'しょうゆ', '味噌', 'みそ'],
    '鶏': ['鶏', 'チキン', '鳥', 'とり'],
    'バナナ': ['バナナ'],
    '豚': ['豚', 'ポーク', 'ぶた'],
    'まつたけ': ['まつたけ', 'マツタケ', '松茸'],
    'もも': ['もも', 'モモ', '桃'],
    'やまいも': ['やまいも', '山芋', 'ヤマイモ'],
    'りんご': ['りんご', 'リンゴ', '林檎'],
    'ゼラチン': ['ゼラチン'],
}


def extract_allergy_words(
    words: dict[str, list[str]],
    allergies_list: list[str],
) -> list[str]:
    '''指定されたアレルギー品目に対応する文字列を抽出する関数。

    指定されたアレルギー品目をもとに、それに分類される材料の文字列を抽出する。

    :param dict[str, list[str]] words: アレルギー品目に関するデータをキーとしてもつ辞書型のデータ
    :param list[str] allergies_list: 指定されたアレルギー品目のデータをもったリスト
    :return: 指定されたアレルギー品目に対応する文字列が含まれたリスト
    :rtype: list[str]
    '''
    extracted_allergies_list = []
    for key in allergies_list:
        extracted_allergies_list.extend(words.get(key, []))

    return extracted_allergies_list


def scoring_recipe(
    recipe: dict[str, Union[str, list[str], float]],
    extracted_allergies_list: list[str],
    score_column: Optional[str] = 'recipe_score',
) -> dict[str, Union[str, list[str], float]]:
    '''各レシピに対して実際にスコアリングを行う関数。

    指定されたアレルギー品目が材料の中に含まれる回数に基づいてスコアリングする。

    :param dict[str, Union[str, list[str], float]] recipe: スコアリング対象となるレシピ単体
    :param list[str] extracted_allergies_list: 指定されたアレルギー品目に対応する文字列が含まれたリスト
    :param Optional[str] score_column: 出力の辞書キー名を設定する変数
    :return: スコアリング済みのレシピ
    :rtype: dict[str, Union[str, list[str], float]]
    '''
    allergen_count = 0
    ingredients = recipe['recipe_ingredients']

    for allergen in extracted_allergies_list:
        allergen_count += ingredients.count(allergen)

    recipe[score_column] = allergen_count
    return recipe


def scoring_recipe_wrapper(
    args: dict[str, Union[dict[str, Union[str, list[str], float]], list[str]]]
) -> dict[str, Union[str, list[str], float]]:
    '''並列処理のための補助関数。

    :param args:
    :type args: dict[str, Union[dict[str, Union[str, list[str], float]], list[str]]]
    :return: スコアリング済みのレシピ
    :rtype: dict[str, Union[str, list[str], float]]
    '''
    return scoring_recipe(**args)


def scoring_count(
    allergies_list: list[str],
    excluded_recipes_list: list[dict[str, Union[str, list[str], float]]],
    score_column: Optional[str] = 'recipe_score',
) -> list[dict[str, Union[str, list[str], float]]]:
    '''カウントベースによるスコアリングを行う関数。

    アレルギー除去処理を行ったレシピに対し、カウントベースによるスコアリングを行う。

    :param list[str] allergies_list: 指定されたアレルギー品目のデータをもったリスト
    :param excluded_recipes_list: アレルギー除去処理を行ったレシピのデータをもったリスト
    :type excluded_recipes_list: list[dict[str, Union[str, list[str], float]]]
    :param Optional[str] score_column: 出力の辞書キー名を設定する変数
    :return: スコアリング済みの、アレルギー除去処理を行ったレシピのデータをもったリスト
    :rtype: list[dict[str, Union[str, list[str], float]]]
    '''
    extracted_allergies_list = extract_allergy_words(WORDS, allergies_list)

    with Pool(cpu_count()) as pool:
        results = list(
            tqdm(
                pool.imap(
                    scoring_recipe_wrapper,
                    [
                        {
                            'recipe': recipe,
                            'extracted_allergies_list': extracted_allergies_list,
                            'score_column': score_column,
                        }
                        for recipe in excluded_recipes_list
                    ],
                ),
                total=len(excluded_recipes_list),
                desc="Processing recipes by counting",
            )
        )

    return results

import logging
import os

from openai import OpenAI

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO: Make OpenAI text chatgpt score func


os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()


def check_allergens_with_chatgpt(ingredients, allergens):
    # ChatGPTへのプロンプトを作成
    prompt = f"次の材料リストにアレルギー品目が含まれているかどうかを教えてください:\n\n材料: {', '.join(ingredients)}\nアレルギー品目: {', '.join(allergens)}\n\nアレルギー品目が含まれている材料をリストアップし、その数を返してください。"

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()

def score_allergens_by_chatgpt(
    recipes, allergens, model_name='text-embedding-3-small'
) -> dict[str, list[float]]:
    # 各レシピに対してアレルギーチェックを行い、スコアを計算する
    for recipe in recipes:
        result = check_allergens_with_chatgpt(recipe['ingredients'], allergens)
        # 含まれているアレルギー品目の数を抽出
        allergen_count = len(result.split())
        # アレルギースコアの計算
        recipe['allergen_score'] = allergen_count / len(recipe['ingredients'])

    return recipe
    

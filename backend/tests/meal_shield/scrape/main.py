import logging

from meal_shield.scrape.scraping_and_excluding import scraping_and_excluding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    recipe_name = 'ココナッツカレー'
    allergy_list = ['鶏', 'とり']
    recipe_data_list = scraping_and_excluding(allergy_list, recipe_name)
    if recipe_data_list is not None:
        for index, recipe_data in enumerate(recipe_data_list):
            logger.info(index + 1)
            logger.info(recipe_data['recipe_title'])
            logger.info(recipe_data['ingredient_list'])
            logger.info(recipe_data['recipe_url'])
            logger.info(recipe_data['recipe_img_url'])
        logger.info(f'検索結果{len(recipe_data_list)}件')
        logger.info(f'検索レシピ名:{recipe_name}')
        logger.info(f'除外品目:{allergy_list}')
    else:
        logger.info(recipe_data_list)
        logger.info('検索結果が見つかりませんでした')

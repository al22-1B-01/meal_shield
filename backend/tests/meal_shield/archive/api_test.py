import logging

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_url = "http://localhost:8000"

recipe = "チョコレートケーキ"
allergy_list = ["卵", "乳", "小麦"]

# パラメータをクエリに変換
params = {
    "recipe": recipe,
    "allergy_list": allergy_list,
}


def main():
    response = requests.get(base_url, params=params)

    logger.info(f"Status code: {response.status_code}")

    if response.status_code == 200:
        logger.info("Response JSON:")
        logger.info(response.json())
    else:
        logger.info("Failed to get a response")


if __name__ == "__main__":
    main()

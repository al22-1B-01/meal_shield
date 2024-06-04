import logging
import os

from openai import OpenAI

from meal_shield.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO: Make OpenAI text chatgpt score func


os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI()


def score_allergens_by_chatgpt(
    recipes, allergens, model_name='text-embedding-3-small'
) -> dict[str, list[float]]:
    pass

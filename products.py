import json
from typing import TypedDict
from api_handler import search_food


class Product:
    nf_calories: float
    nf_total_fat: float
    nf_saturated_fat: float
    nf_cholesterol: float
    nf_sodium: float
    nf_total_carbohydrate: float
    nf_dietary_fiber: float
    nf_sugars: float
    nf_protein: float

    def __init__(self, **nutrients):
        pass


if __name__ == '__main__':
    # query = "apple"
    # result = search_food(query)
    p = Product({"nf_calories": 3, "other": 0})
    print(Product())

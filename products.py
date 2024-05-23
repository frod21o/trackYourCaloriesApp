import json
from collections import namedtuple

Nutrients = namedtuple("Nutrients", ['nf_calories', 'nf_total_fat',
                                     'nf_saturated_fat', 'nf_cholesterol', 'nf_total_carbohydrate',
                                     'nf_sugars', 'nf_dietary_fiber', 'nf_protein', 'nf_sodium'])


class Product:
    def __init__(self, name: str, weight: float = None, **nutrients):
        """
        :param name: Name of the product
        :param weight: Amount of the product in grams
        :param nutrients: Saved will be nutrients: 'nf_calories', 'nf_total_fat', 'nf_saturated_fat', 'nf_cholesterol',
                        'nf_total_carbohydrate', 'nf_sugars', 'nf_dietary_fiber', 'nf_protein', 'nf_sodium'
        """
        self.name = name
        self.weight = weight
        self.description = None
        self.nutrients: Nutrients = Nutrients(**({field: nutrients.get(field, None) for field in Nutrients._fields}))

    def __repr__(self):
        return json.dumps({
            "name": self.name,
            "weight": self.weight,
            "nutrients": self.nutrients
        })


if __name__ == '__main__':
    """ testing functionalities """
    p = Product({"nf_calories": 3, "other": 0})
    print(p)


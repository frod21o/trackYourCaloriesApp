import json
from collections import namedtuple

Nutrients = namedtuple("Nutrients", ['nf_calories', 'nf_total_fat',
                                     'nf_saturated_fat', 'nf_cholesterol', 'nf_total_carbohydrate',
                                     'nf_sugars', 'nf_dietary_fiber', 'nf_protein', 'nf_sodium'])


class ProductType:
    """ Defines all characteristics of an eatable product """
    def __init__(self, name: str, **nutrients):
        """
        :param name: Name of the product
        :param nutrients: Saved will be nutrients: 'nf_calories', 'nf_total_fat', 'nf_saturated_fat', 'nf_cholesterol',
                        'nf_total_carbohydrate', 'nf_sugars', 'nf_dietary_fiber', 'nf_protein', 'nf_sodium'
        """
        self.name = name
        self.description = None
        self.nutrients: Nutrients = Nutrients(**({field: nutrients.get(field, None) for field in Nutrients._fields}))

    def __repr__(self):
        return json.dumps({
            "name": self.name,
            "nutrients": self.nutrients
        })

    @staticmethod
    def combine_products(name: str, ingreedients: list['Product']) -> 'Product':
        combined_nutrients = {}
        for product in ingreedients:
            for nut_name in product.product_type.nutrients._fields:
                combined_nutrients[nut_name] = (combined_nutrients.get(nut_name, 0) +
                                                product.product_type.nutrients[nut_name] * product.weight/100)
        return ProductType(name, **combined_nutrients)


class Product:
    """ Represents an actual product """
    def __init__(self, product_type: ProductType, weight: float):
        """
        :param product_type: Type of the product characterized by ProductType class
        :param weight: Amount of the product in grams
        """
        self.product_type = product_type
        self.weight = weight

    def __repr__(self):
        return f"{self.product_type} :: {self.weight}g"


if __name__ == '__main__':
    """ testing functionalities """
    p = ProductType({"nf_calories": 3, "other": 0})
    print(p)

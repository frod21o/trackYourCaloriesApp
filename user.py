from PySide6.QtCore import QDate
from typing import TypedDict
import re
import os
import pickle

from products import ProductType, Product, Nutrients

MALE_STR = "Male"
FEMALE_STR = "Female"


def current_date() -> QDate:
    return QDate.currentDate()


def _user_filename(username: str) -> str:
    return username + "_data.pkl"


class UserData(TypedDict):
    """ Holds data about specific user """
    username: str
    custom_products: list[ProductType]
    eat_history: dict[QDate, list[Product]]
    gender: str
    age: int
    height: float
    weight: float
    limits: Nutrients


class User:
    def __init__(self, username: str):
        self._data: UserData = {"username": username}
        try:
            self.load_data()
        except FileNotFoundError:
            self._data["custom_products"] = []
            self._data["eat_history"] = {}
            self._data["gender"] = ''
            self._data["age"] = 0
            self._data["height"] = 0
            self._data["weight"] = 0
            self._data["limits"] = Nutrients(*(None for _ in Nutrients._fields))

    def load_data(self):
        """ Loads user data from file """
        with open(_user_filename(self._data["username"]), 'rb') as file:
            self._data = pickle.load(file)

    def save_data(self):
        """ Saves user data to file """
        with open(_user_filename(self._data["username"]), 'wb') as file:
            pickle.dump(self._data, file)

    # Custom products are the products created and described by the user
    def get_custom_products(self) -> list[ProductType]:
        return self._data["custom_products"]

    def create_add_custom_product(self, food_name: str, **nutrients):
        self._data["custom_products"].append(ProductType(name=food_name, nutrients=nutrients))
        self.save_data()

    def add_custom_product(self, product_type: ProductType):
        self._data["custom_products"].append(product_type)
        self.save_data()

    def del_custom_product(self, index: int):
        self._data["custom_products"].pop(index)
        self.save_data()

    # Eaten products are products that user claimed that he ate
    def get_eaten_products(self, from_date: QDate = current_date()) -> list[Product]:
        return self._data["eat_history"].setdefault(from_date, [])

    def create_add_eaten_product(self, product_type: ProductType, weight: float):
        self._data["eat_history"].setdefault(current_date(), []).append(
            Product(product_type=product_type, weight=weight))
        self.save_data()

    def add_eaten_product(self, product: Product):
        self._data["eat_history"].setdefault(current_date(), []).append(product)
        self.save_data()

    def del_eaten_product(self, index: int):
        self._data["eat_history"][current_date()].pop(index)
        self.save_data()

    def count_nutrients(self, nutrient_idx: int, date: QDate = current_date()):
        """
        Returns a tuple like (amount, correct) where:
        amount - amount of selected nutrient eaten at selected date
        correct - bool value indicating if none of the nutrient values were NoneType

        TODO
        """
        nutrient_values = [product.product_type.nutrients[nutrient_idx] * product.weight / 100
                           for product in self._data["eat_history"][date]
                           if product.product_type.nutrients[nutrient_idx] is not None]
        return sum(nutrient_values), len(nutrient_values) == len(self._data["eat_history"][date])

    def set_user_parameters(self, gender: str, age: int, height: float, weight: float):
        """ Sets user parameters to given values """
        self._data["gender"] = gender
        self._data["age"] = age
        self._data["height"] = height
        self._data["weight"] = weight
        self.save_data()

    def set_limits(self, limits: Nutrients):
        self._data["limits"] = limits
        self.save_data()

    def get_ppm(self) -> float | None:
        """ Returns PPM based on the user parameters. If not all parameters are valid, returns None"""
        if self._data["age"] <= 0 or self._data["height"] <= 0 or self._data["weight"] <= 0:
            return None
        if self._data["gender"] is MALE_STR:
            return 66.473 + 13.7561 * self._data["weight"] + 5.0033 * self._data["height"] + 6.755 * self._data["age"]
        if self._data["gender"] is FEMALE_STR:
            return 655.0955 + 9.5634 * self._data["weight"] + 1.8496 * self._data["height"] + 4.6756 * self._data["age"]
        return None

    # Getters
    @property
    def name(self):
        return self._data.get("username", "")

    @property
    def gender(self):
        return self._data.get("gender", "")

    @property
    def age(self):
        return self._data.get("age", 0)

    @property
    def height(self):
        return self._data.get("height", 0)

    @property
    def weight(self):
        return self._data.get("weight", 0)

    @property
    def limits(self):
        return self._data.get("limits", Nutrients(*(None for _ in Nutrients._fields)))


def get_available_users() -> list[str]:
    """ Finds all users, whose data is available """
    matched_filenames = [re.match(r'(.*)_data\.pkl', file) for file in os.listdir()]
    return [m.group(1) for m in matched_filenames if m]


if __name__ == '__main__':
    """ testing functionalities """
    user = User("jedrzej")
    # user.create_add_eaten_product(ProductType("ogór"), 50)
    user.create_add_eaten_product(ProductType("jajo"), 20)
    user.create_add_eaten_product(ProductType("drugie jajo"), 20)
    # user.del_eaten_product(0)
    print(user.get_eaten_products())

    print(get_available_users())

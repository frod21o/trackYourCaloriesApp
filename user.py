from datetime import date
from typing import TypedDict

from products import Product
import pickle


def _current_date() -> date:
    return date.today()


def _user_filename(username: str) -> str:
    return username + "_data.pkl"


class UserData(TypedDict):
    """ Holds data about specific user """
    username: str
    custom_products: list[Product]
    eat_history: dict[date, list[Product]]


class User:
    def __init__(self, username: str):
        self._data: UserData = {"username": username}
        try:
            self.load_data()
        except FileNotFoundError:
            self._data["custom_products"] = []
            self._data["eat_history"] = {}

    def load_data(self):
        """ Loads user data from file """
        with open(_user_filename(self._data["username"]), 'rb') as file:
            self._data = pickle.load(file)

    def save_data(self):
        """ Saves user data to file """
        with open(_user_filename(self._data["username"]), 'wb') as file:
            pickle.dump(self._data, file)

    # Custom products are the products created and described by the user
    def get_custom_products(self) -> list[Product]:
        return self._data["custom_products"]

    def add_custom_product(self, food_name: str, **nutrients):
        self._data["custom_products"].append(Product(name=food_name, nutrients=nutrients))
        self.save_data()

    def del_custom_product(self, index: int):
        self._data["custom_products"].pop(index)
        self.save_data()

    # Ate products are products that user claimed that he ate
    def get_ate_products(self) -> list[Product]:
        return self._data["eat_history"].setdefault(_current_date(), [])

    def add_ate_product(self, food_name: str, weight: float, **nutrients):
        self._data["eat_history"].setdefault(_current_date(), []).append(Product(name=food_name, weight=weight,
                                                                                 nutrients=nutrients))
        self.save_data()

    def del_ate_product(self, index: int):
        self._data["eat_history"][_current_date()].pop(index)
        self.save_data()


if __name__ == '__main__':
    """ testing functionalities """
    user = User("jedrzej")
    # user.add_ate_product("ogór", 50)
    # user.add_ate_product("jajo", 20)
    # user.add_ate_product("drugie jajo", 20)
    # user.del_ate_product(0)
    print(user.get_ate_products())

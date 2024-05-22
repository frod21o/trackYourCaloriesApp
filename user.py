from datetime import date
from typing import TypedDict

from products import Product


def current_date() -> date:
    return date.today()


def user_filename(username: str) -> str:
    return username + "_data.json"


class UserData(TypedDict):
    username: str
    custom_products: list[Product]
    eat_history: dict[date, list[Product]]


def get_userdata_from_file(name: str) -> UserData:
    pass


class User:
    def __init__(self, username: str):
        self.data: UserData
        self.load_data()

    def load_data(self):
        pass

    def save_data(self):
        pass




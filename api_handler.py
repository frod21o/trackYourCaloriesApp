import requests
import json


def get_headers(filename: str):
    """ Loads headers from file, including API key and ID """
    with open(filename, 'r') as file:
        return json.load(file)


headers_filename = "headers.json"
base_url = "https://trackapi.nutritionix.com/v2/"
headers = get_headers(headers_filename)


def search_food(query: dict) -> dict:
    """
    Finds a product based on string query

    :param query: Name of the product
    :return: Dict with the results
    """
    params = {
        'query': query,
        'branded': True,
        'common': False
    }

    try:
        response = requests.get(base_url + "search/instant", headers=headers, params=params)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_nutrition_info(item_id: str) -> dict:
    """
    Downloads information about nutrition of specific item

    :param item_id: Unique product identifier (nix_item_id)
    :return: Dict with nutrition info
    """
    params = {
        'nix_item_id': item_id
    }

    try:
        response = requests.get(base_url + "search/item", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    query = "apple"
    search_result = search_food(query)

    if search_result and 'branded' in search_result and search_result['branded']:
        # Weź pierwszy wynik z listy produktów markowych
        item_id = search_result['branded'][0]['nix_item_id']

        # Pobierz informacje o składnikach odżywczych
        nutrition_info = get_nutrition_info(item_id)

        if nutrition_info:
            print(nutrition_info)
        else:
            print("Failed to retrieve nutrition information")
    else:
        print("No branded products found or failed to retrieve search results")


    # if result:
    #     print(len(result))
    #     print(result)
    #     for it in result["common"]:
    #         print(f"keys: {it.keys()}")
    #         print(f"name: {it['food_name']}")
    #         print(f"id: {it['tag_id']}")
    #     for it in result["branded"]:
    #         # print(f"keys: {it.keys()}")
    #         print(f"name: {it['food_name']}")
    #         print(it)
    #         # print(f"name: {it['tag_name']}")
    #         # print(f"id: {it['tag_id']}")
    # else:
    #     print("Failed to retrieve data")

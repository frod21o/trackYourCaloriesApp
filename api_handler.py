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
    return _get_response(base_url + "search/instant", params)['branded']


def get_nutrition_by_id(item_id: str) -> dict:
    """
    Downloads information about nutrition of specific item

    :param item_id: Unique product identifier (nix_item_id)
    :return: Dict with nutrition info
    """
    params = {'nix_item_id': item_id}
    response = _get_response(base_url + "search/item", params)
    return response['foods'][0] if response else None


def get_nutrition_by_upc(upc: str) -> dict:
    """
    Downloads information about nutrition of specific item

    :param :
    :return: Dict with nutrition info
    """
    params = {'upc': upc}
    response = _get_response(base_url + "search/item", params)
    return response['foods'][0] if response else None


def _get_response(url: str, params: dict):
    """
    Sends request to given url with given parameters

    :param url: Url address for request
    :param params: Dict with parameters of the request
    :return: Dict with response
    """
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    """ testing functionalities """
    search_result = search_food("apple")

    if search_result:
        print(len(search_result))
        for it in search_result:
            print(f"keys: {it.keys()}")
            print(f"name: {it['food_name']}")
            print(it)
    else:
        print("Failed to retrieve data")

    print('\n\n')

    if search_result:
        item_id = search_result[0]['nix_item_id']

        nutrition_info = get_nutrition_by_id(item_id)

        if nutrition_info:
            print("found nutrition info:")
            print(nutrition_info)
        else:
            print("Failed to retrieve nutrition information")
    else:
        print("No branded products found or failed to retrieve search results")

    print(get_nutrition_by_upc(49000000450))


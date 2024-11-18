# 3. Сценарий Foursquare:

import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(asctime)s %(message)s")

client_id = "__"
client_secret = "__"
city = "Tyumen"
valid_categories = ['coffee shops', 'museums', 'parks', 'zoo', 'cafe', 'park', 'shops', 'restaurants', 'restauran']

url = "https://api.foursquare.com/v3/places/search"

category = input("Enter a category from coffee shops, museums or parks: ")

while category == "" or category.lower() not in valid_categories:
    print("Input cannot be empty, enter a category: coffee shops, museums, parks, zoo, park, shops, restaurants, restauran")
    category = input("Enter a category from coffee shops, museums or parks: ").strip()

params = {
    "limit": 10,
    "client_id": client_id,
    "client_secret": client_secret,
    "near": city,
    "query": category,
    "fields": "name,location,rating"
    
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}

response = requests.get(url=url, params=params, headers=headers)

if response.status_code == 200:
    response = requests.get(url=url, params=params, headers=headers)
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        try:
            print("Название:", venue["name"])
            print("Адрес:", venue["location"]["address"] if 'address' in venue["location"] else "Адрес не найден.")
            print("Рейтинг:", venue["rating"] if 'rating' in venue else "Рейтинг не найден.")
            print("\n")
        except KeyError as e:
            logging.error(f"Отсутствует ожидаемое поле: {e}")

    logging.info(f"Статус Вашего запроса: {response.status_code}")
else:
    print("Запрос API отклонен с ошибкой:", response.status_code)

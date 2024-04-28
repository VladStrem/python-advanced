import json
import requests
from pydantic import BaseModel


class Book(BaseModel):
    number: int
    originalTitle: str
    releaseDate: str


def get_data():
    response = requests.get("https://potterapi-fedeperin.vercel.app/en/books")
    return response.json()


def save_to_json(filename):
    products = get_data()
    data = []
    for product in products:
        item = Book(**product)
        data.append(item.dict())
        print(item.dict())
    with open(filename, mode="w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    save_to_json("books.json")

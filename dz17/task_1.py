from typing import List
from pydantic import BaseModel, Field, ValidationError, field_validator
import json


class Author(BaseModel):
    name: str
    gender: str
    nationality: str

    @field_validator('gender')
    def validate_gender(cls, value):
        if value.lower() not in ['male', 'female']:
            raise ValueError('Gender must be "Male" of "Female"')
        return value.title()


class Book(BaseModel):
    id: int
    name_book: str = Field(alias="nameBook")
    year: int
    authors: List[Author]

    def __str__(self):
        authors = ", ".join(author.name for author in self.authors)
        return f"Book id: {self.id}, Title: {self.name_book}, Year: {self.year}, Authors: {authors}"


def deserialize(filename: str):
    with open(filename, mode='r') as file:
        data = json.load(file)
        try:
            return Book(**data)
        except ValidationError as e:
            print(f'Deserialization Error: {e}')


def serialize(book: Book, filename: str):
    new_data = book.dict(exclude={"id"})
    with open(filename, mode='w') as file:
        json.dump(new_data, file, indent=4)


if __name__ == "__main__":
    book = deserialize('data.json')
    if book:
        print('Original Book:')
        print("Title:", book.name_book)
        print("Year:", book.year)
        print("Authors:")
        for author in book.authors:
            print(" - Name:", author.name)
            print("   Gender:", author.gender)
            print("   Nationality:", author.nationality)
        print()
        book.year = 1998
        print('Modified Book:')
        print("Title:", book.name_book)
        print("Year:", book.year)
        print("Authors:")
        for author in book.authors:
            print(" - Name:", author.name)
            print("   Gender:", author.gender)
            print("   Nationality:", author.nationality)

        serialize(book, 'data_modified.json')
        print('Serialization seccessful')

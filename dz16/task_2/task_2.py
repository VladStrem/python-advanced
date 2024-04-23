import pickle
from typing import List, Dict, Any


class Author:
    def __init__(self, name: str, gender: str, nationality: str) -> None:
        self.name = name
        self.gender = gender
        self.nationality = nationality


class Book:
    def __init__(self, title: str, year: int, authors: List[Author]) -> None:
        self.title = title
        self.year = year
        self.authors = authors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "year": self.year,
            "authors": [aut.__dict__ for aut in self.authors]
        }

    def save_to_json(self, filename: str) -> None:
        with open(filename, mode='wb') as file:
            pickle.dump(self.to_dict(), file)

    @classmethod
    def load_from_json(cls, filename: str) -> 'Book':
        with open(filename, mode='rb') as file:
            data = pickle.load(file)
            authors = [Author(**author_data) for author_data in data['authors']]
            return cls(data['title'], data['year'], authors)


author1 = Author("J.K. Rowling", "Female", "British")
author2 = Author("Stephen King", "Male", "American")

book = Book("Harry Potter", 1997, [author1, author2])

book.save_to_json("book.pkl")

loaded_book = Book.load_from_json("book.pkl")

print("Title:", loaded_book.title)
print("Year:", loaded_book.year)
print("Authors:")
for author in loaded_book.authors:
    print(" - Name:", author.name)
    print("   Gender:", author.gender)
    print("   Nationality:", author.nationality)
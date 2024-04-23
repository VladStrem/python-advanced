import json
from typing import List, Dict, Any


class Author:
    def __init__(self, name: str, gender: str, nationality: str) -> None:
        self.name = name
        self.gender = gender
        self.nationality = nationality

    def to_dict(self) -> Dict[str, str]:
        author_dict = {
            "name": self.name,
            "gender": self.gender,
            "nationality": self.nationality
        }
        return author_dict

    @classmethod
    def from_dict(cls, author_data: Dict[str, str]) -> 'Author':
        return cls(author_data['name'], author_data['gender'], author_data['nationality'])


class Book:
    def __init__(self, title: str, year: int, authors: List[Author]) -> None:
        self.title = title
        self.year = year
        self.authors = authors

    def to_dict(self) -> Dict[str, Any]:
        book_dict = {
            "title": self.title,
            "year": self.year,
            "authors": []
        }
        for author in self.authors:
            book_dict['authors'].append(author.to_dict())
        return book_dict

    def save_to_json(self, filename: str) -> None:
        with open(filename, mode='w') as file:
            json.dump(self.to_dict(), file, indent=4)

    @classmethod
    def load_from_json(cls, filename: str) -> 'Book':
        with open(filename, mode='r') as file:
            data = json.load(file)
            authors = []
            for author_data in data['authors']:
                authors.append(Author.from_dict(author_data))
            return cls(data['title'], data['year'], authors)


author1 = Author("J.K. Rowling", "Female", "British")
author2 = Author("Stephen King", "Male", "American")

book = Book("Harry Potter", 1997, [author1, author2])

book.save_to_json("book.json")

loaded_book = Book.load_from_json("book.json")

print("Title:", loaded_book.title)
print("Year:", loaded_book.year)
print("Authors:")
for author in loaded_book.authors:
    print(" - Name:", author.name)
    print("   Gender:", author.gender)
    print("   Nationality:", author.nationality)

from book import Book
from typing import List, NoReturn, Dict

import enum
import json


class SearchRemoveBy(enum.Enum):
    AUTHORS = 1
    PUBLISHING_HOUSE_AND_AUTHOR = 2
    VOLUMES_AMOUNT = 3
    BOOK_NAME = 4
    PUBLISHED_AMOUNT = 5
    PUBLISHED_VOLUMES_AMOUNT = 6


class SortBy(enum.Enum):
    NAME_SORT = 1
    PUBLISHING_HOUSE_SORT = 2
    PUBLISHED_AMOUNT_SORT = 3


class Library:

    def __init__(self, books=None, filename: str = '', saved_flag=False):
        if books:
            for book in books:
                if not isinstance(book, Book):
                    raise TypeError(f"Unknown type for library: {type(book)}")
            self._books: List[Book] = books
        else:
            self._books = []
        if filename and not filename.endswith(".json"):
            raise ValueError(f"Expected .json file. Got {filename} instead")
        self._save_filename: str = filename
        self._saved_flag = saved_flag

    @property
    def books(self) -> List[Book]:
        return self._books

    @property
    def save_filename(self) -> str:
        return self._save_filename

    @save_filename.setter
    def save_filename(self, new_filename: str) -> NoReturn:
        if not isinstance(new_filename, str):
            raise TypeError(f"Filename must be str, not {type(new_filename)}")
        elif not new_filename.endswith(".json"):
            raise ValueError(f"Expected .json file. Got {new_filename} instead")
        else:
            self._save_filename = new_filename

    @property
    def saved_flag(self) -> bool:
        return self._saved_flag

    def exists(self, book: Book) -> bool:
        if book in self._books:
            return True

    def add_book(self, book_params: Dict) -> str:
        if self._saved_flag:
            self._saved_flag = False
        if self.exists(Book(**book_params)):
            return f"Book {Book(**book_params)} is already exists."
        else:
            self._books.append(Book(**book_params))
            return f"Book {Book(**book_params)} is added to library."

    def add_books(self, books_params: List[Dict]) -> str:
        if self._saved_flag:
            self._saved_flag = False
        msg = ""
        added_amount = 0
        for book_params in books_params:
            if self.exists(Book(**book_params)):
                msg += f"Book {Book(**book_params)} is already exists.\n"
            else:
                self._books.append(Book(**book_params))
                msg += f"Book {Book(**book_params)} is added to library.\n"
                added_amount += 1
        return f"Added amount:\t{added_amount}\n" + msg.rstrip("\n")

    def remove_books(self, remove_by: SearchRemoveBy, *args) -> int:
        if remove_by == SearchRemoveBy.AUTHORS:
            removed = self._remove_by_authors(authors=args[0])
        elif remove_by == SearchRemoveBy.PUBLISHING_HOUSE_AND_AUTHOR:
            removed = self._remove_by_publishing_house_and_authors(publishing_house=args[0], authors=args[1])
        elif remove_by == SearchRemoveBy.VOLUMES_AMOUNT:
            removed = self._remove_by_volumes_amount(min_volumes_amount=args[0], max_volumes_amount=args[1])
        elif remove_by == SearchRemoveBy.BOOK_NAME:
            removed = self._remove_by_book_name(removing_book_name=args[0])
        elif remove_by == SearchRemoveBy.PUBLISHED_AMOUNT:
            removed = self._remove_by_published_amount(min_published_amount=args[0], max_published_amount=args[1])
        elif remove_by == SearchRemoveBy.PUBLISHED_VOLUMES_AMOUNT:
            removed = self._remove_by_published_volumes(min_published_v_amount=args[0], max_published_v_amount=args[1])
        else:
            raise ValueError(f"Unknown parameter for search: {remove_by}")
        if removed and self._saved_flag:
            self._saved_flag = False
        return removed

    def _remove_by_authors(self, authors: List[str]) -> int:
        if not isinstance(authors, list):
            raise TypeError(f"Expected list, got {type(authors)} instead")
        for author in authors:
            if not isinstance(author, str):
                raise TypeError(f"Unknown type for \"author\": {type(author)}")
        remaining_books: List[Book] = []
        for book in self._books:
            for author in authors:
                if author in book.authors:
                    break
            else:
                remaining_books.append(book)
        deleted_amount = len(self._books) - len(remaining_books)
        self._books = remaining_books
        return deleted_amount

    def _remove_by_publishing_house_and_authors(self, publishing_house: str, authors: List[str]) -> int:
        if not isinstance(publishing_house, str):
            raise TypeError(f"Unknown type for \"publishing_house\": {type(publishing_house)}")
        if not isinstance(authors, list):
            raise TypeError(f"Expected list, got {type(authors)} instead")
        for author in authors:
            if not isinstance(author, str):
                raise TypeError(f"Unknown type for \"author\": {type(author)}")
        remaining_books: List[Book] = []
        for book in self._books:
            for author in authors:
                if publishing_house == book.publishing_house or author in book.authors:
                    break
            else:
                remaining_books.append(book)
        deleted_amount = len(self._books) - len(remaining_books)
        self._books = remaining_books
        return deleted_amount

    def _remove_by_volumes_amount(self, min_volumes_amount: int, max_volumes_amount: int) -> int:
        if not isinstance(min_volumes_amount, int):
            raise TypeError(f"Unknown type for \"min_volumes_amount\": {type(min_volumes_amount)}")
        if not isinstance(max_volumes_amount, int):
            raise TypeError(f"Unknown type for \"max_volumes_amount\": {type(max_volumes_amount)}")
        remaining_books: List[Book] = []
        for book in self._books:
            if not min_volumes_amount <= book.volumes <= max_volumes_amount:
                remaining_books.append(book)
        deleted_amount = len(self._books) - len(remaining_books)
        self._books = remaining_books
        return deleted_amount

    def _remove_by_book_name(self, removing_book_name: str) -> int:
        if not isinstance(removing_book_name, str):
            raise TypeError(f"Unknown type for \"book_name\": {type(removing_book_name)}")
        remaining_books: List[Book] = []
        for book in self._books:
            if book.name != removing_book_name:
                remaining_books.append(book)
        deleted_amount = len(self._books) - len(remaining_books)
        self._books = remaining_books
        return deleted_amount

    def _remove_by_published_amount(self, min_published_amount: int, max_published_amount: int) -> int:
        if not isinstance(min_published_amount, int):
            raise TypeError(f"Unknown type for \"min_published_amount\": {type(min_published_amount)}")
        if not isinstance(max_published_amount, int):
            raise TypeError(f"Unknown type for \"max_published_amount\": {type(max_published_amount)}")
        remaining_books: List[Book] = []
        for book in self._books:
            if not min_published_amount <= book.published_amount <= max_published_amount:
                remaining_books.append(book)
        deleted_amount = len(self._books) - len(remaining_books)
        self._books = remaining_books
        return deleted_amount

    def _remove_by_published_volumes(self, min_published_v_amount: int, max_published_v_amount: int) -> int:
        if not isinstance(min_published_v_amount, int):
            raise TypeError(f"Unknown type for \"min_published_v_amount\": {type(min_published_v_amount)}")
        if not isinstance(max_published_v_amount, int):
            raise TypeError(f"Unknown type for \"max_published_v_amount\": {type(max_published_v_amount)}")
        remaining_books: List[Book] = []
        for book in self._books:
            if not min_published_v_amount <= book.published_volumes_amount <= max_published_v_amount:
                remaining_books.append(book)
        deleted_amount = len(self._books) - len(remaining_books)
        self._books = remaining_books
        return deleted_amount

    def search_for_books(self, search_by: SearchRemoveBy, *args) -> List[Book]:
        if search_by == SearchRemoveBy.AUTHORS:
            return self._search_by_authors(authors=args[0])
        elif search_by == SearchRemoveBy.PUBLISHING_HOUSE_AND_AUTHOR:
            return self._search_by_publishing_house_and_authors(publishing_house=args[0], authors=args[1])
        elif search_by == SearchRemoveBy.VOLUMES_AMOUNT:
            return self._search_by_volumes_amount(min_volumes_amount=args[0], max_volumes_amount=args[1])
        elif search_by == SearchRemoveBy.BOOK_NAME:
            return self._search_by_book_name(book_name=args[0])
        elif search_by == SearchRemoveBy.PUBLISHED_AMOUNT:
            return self._search_by_published_amount(min_published_amount=args[0], max_published_amount=args[1])
        elif search_by == SearchRemoveBy.PUBLISHED_VOLUMES_AMOUNT:
            return self._search_by_published_volumes(min_published_v_amount=args[0], max_published_v_amount=args[1])
        else:
            raise ValueError(f"Unknown parameter for search: {search_by}")

    def _search_by_authors(self, authors: List[str]) -> List[Book]:
        if not isinstance(authors, list):
            raise TypeError(f"Expected list, got {type(authors)} instead")
        for author in authors:
            if not isinstance(author, str):
                raise TypeError(f"Unknown type for \"author\": {type(author)}")
        found_books: List[Book] = []
        for book in self._books:
            for author in authors:
                if author in book.authors:
                    found_books.append(book)
                    break
        return found_books

    def _search_by_publishing_house_and_authors(self, publishing_house: str, authors: List[str]) -> List[Book]:
        if not isinstance(publishing_house, str):
            raise TypeError(f"Unknown type for \"publishing_house\": {type(publishing_house)}")
        if not isinstance(authors, list):
            raise TypeError(f"Expected list, got {type(authors)} instead")
        for author in authors:
            if not isinstance(author, str):
                raise TypeError(f"Unknown type for \"author\": {type(author)}")
        found_books: List[Book] = []
        for book in self._books:
            for author in authors:
                if publishing_house == book.publishing_house or author in book.authors:
                    found_books.append(book)
                    break
        return found_books

    def _search_by_volumes_amount(self, min_volumes_amount: int, max_volumes_amount: int) -> List[Book]:
        if not isinstance(min_volumes_amount, int):
            raise TypeError(f"Unknown type for \"min_volumes_amount\": {type(min_volumes_amount)}")
        if not isinstance(max_volumes_amount, int):
            raise TypeError(f"Unknown type for \"max_volumes_amount\": {type(max_volumes_amount)}")
        found_books: List[Book] = []
        for book in self._books:
            if min_volumes_amount <= book.volumes <= max_volumes_amount:
                found_books.append(book)
        return found_books

    def _search_by_book_name(self, book_name: str) -> List[Book]:
        if not isinstance(book_name, str):
            raise TypeError(f"Unknown type for \"book_name\": {type(book_name)}")
        found_books: List[Book] = []
        for book in self._books:
            if book.name == book_name:
                found_books.append(book)
        return found_books

    def _search_by_published_amount(self, min_published_amount: int, max_published_amount: int) -> List[Book]:
        if not isinstance(min_published_amount, int):
            raise TypeError(f"Unknown type for \"min_published_amount\": {type(min_published_amount)}")
        if not isinstance(max_published_amount, int):
            raise TypeError(f"Unknown type for \"max_published_amount\": {type(max_published_amount)}")
        found_books: List[Book] = []
        for book in self._books:
            if min_published_amount <= book.published_amount <= max_published_amount:
                found_books.append(book)
        return found_books

    def _search_by_published_volumes(self, min_published_v_amount: int, max_published_v_amount: int) -> List[Book]:
        if not isinstance(min_published_v_amount, int):
            raise TypeError(f"Unknown type for \"min_published_v_amount\": {type(min_published_v_amount)}")
        if not isinstance(max_published_v_amount, int):
            raise TypeError(f"Unknown type for \"max_published_v_amount\": {type(max_published_v_amount)}")
        found_books: List[Book] = []
        for book in self._books:
            if min_published_v_amount <= book.published_volumes_amount <= max_published_v_amount:
                found_books.append(book)
        return found_books

    def save(self, filename: str) -> NoReturn:
        if not filename.endswith(".json"):
            raise ValueError(f"Save file must be .json. Got {filename} instead")
        with open(filename, "w") as save_file:
            json.dump([book.json_dict() for book in self._books], save_file, indent="\t")
            if self._save_filename != filename:
                self._save_filename = filename
        self._saved_flag = True

    @staticmethod
    def load(filename):
        if not filename.endswith(".json"):
            raise ValueError(f"Uploading file must be .json. Got {filename} instead")
        with open(filename, "r") as save_file:
            return Library(
                books=[Book(**book_json_dict) for book_json_dict in json.load(save_file)],
                filename=filename,
                saved_flag=True)

    def change_book_info(self, book: Book, new_params: Dict) -> str:
        if book not in self._books:
            raise ValueError(f"There is no such book {book} in library")
        else:
            msg: str = ""
            if "name" in new_params.keys():
                msg += f"Book name \"{book.name}\" changed to \"{new_params['name']}\"\n"
                book.name = new_params["name"]
            if "authors" in new_params.keys():
                msg += f"Book authors {''.join(book.authors)} changed to {''.join(new_params['authors'])}\n"
                book.authors = new_params["authors"]
            if "publishing_house" in new_params.keys():
                msg += f"Book publishing house {book.publishing_house} changed to {new_params['publishing_house']}\n"
                book.publishing_house = new_params["publishing_house"]
            if "volumes" in new_params.keys():
                msg += f"book volumes amount {book.volumes} changed to {new_params['volumes']}\n"
                book.volumes = new_params["volumes"]
            if "published_amount" in new_params.keys():
                msg += f"Book published amount {book.published_amount} changed to {new_params['published_amount']}\n"
                book.published_amount = new_params["published_amount"]
            if msg and self._saved_flag:
                self._saved_flag = False
            return "Nothing was changed." if not msg else msg.rstrip("\n")

    def sort_by(self, sort_by: SortBy, reverse: bool) -> NoReturn:
        if sort_by == SortBy.NAME_SORT:
            self._books.sort(key=lambda book: book.name, reverse=reverse)
        elif sort_by == SortBy.PUBLISHED_AMOUNT_SORT:
            self._books.sort(key=lambda book: book.published_amount, reverse=reverse)
        elif sort_by == SortBy.PUBLISHING_HOUSE_SORT:
            self._books.sort(key=lambda book: book.publishing_house, reverse=reverse)
        else:
            raise TypeError(f"Unknown type for sort parameter: got {type(sort_by)} instead {type(SortBy)}")


"""
l1 = [Book(authors=["Voitkus", "Ibrahimov Ilya"], name="Какиш в двух томах", publishing_house="IIT KAFEDRA",
           published_amount=243, volumes=2)]
lib = Library(books=l1)

tmp = lib.add_book({
    "authors": ["Славянка Слабая"],
    "name": "Оформил бы?",
    "published_amount": 28
}
)
tmp = lib.add_books([
    {
        "authors": ["Славянка Слабая"],
        "name": "Оформил бы?",
        "published_amount": 28
    },
    {
        "authors": ["Voitkus"],
        "name": "Всё о мёде. Секретные методики оформелния НКВД",
        "publishing_house": "Гульчитай",
        "published_amount": 777
    },
    {"authors": ["Ibrahimov Ilya", "Ахмэд"],
     "name": "How to kill Zaklepka",
     "publishing_house": "Ich zet nein tue frein",
     "published_amount": 188, "volumes":10
     }]
)
for book_bamboo in lib.search_for_books(SearchRemoveBy.AUTHORS, ["Voitkus"]):
    lib.change_book_info(book_bamboo, {"authors": ["Войткус", "Ибрагимов Илья"], "published_amount": 654})

lib = lib.save("./saves/autosave10.json")

# temp = lib.remove_books(SearchRemoveBy.PUBLISHED_VOLUMES_AMOUNT, 230, 1870)

input()
"""

'''
# For autosave - name of autosave file
import os
import re
regex = re.compile(r"^exit_save([1-9]\d*)\.json$")

def _find_max_index_of_exit_file():
    indexes = [int(regex.match(file).group(1)) for file in os.listdir("./saves") if regex.match(file)]
    return max(indexes)

temp = _find_max_index_of_exit_file()
input()
'''




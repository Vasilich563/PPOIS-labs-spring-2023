from typing import List, NoReturn, Dict


class Book:

    def __init__(self, **kwargs):
        kwargs["name"] = kwargs.get("name", "unknown")
        kwargs["authors"] = kwargs.get("authors", "unknown")
        kwargs["publishing_house"] = kwargs.get("publishing_house", "unknown")
        kwargs["volumes"] = kwargs.get("volumes", 1)
        kwargs["published_amount"] = kwargs.get("published_amount", 0)
        self._name: str = kwargs["name"]
        self._authors: List[str] = kwargs["authors"]
        self._publishing_house: str = kwargs["publishing_house"]
        self._volumes: int = kwargs["volumes"]
        self._published_amount: int = kwargs["published_amount"]

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name) -> NoReturn:
        self._name = new_name

    @property
    def authors(self) -> List[str]:
        return self._authors

    @authors.setter
    def authors(self, new_authors) -> NoReturn:
        self._authors = new_authors

    @property
    def publishing_house(self) -> str:
        return self._publishing_house

    @publishing_house.setter
    def publishing_house(self, new_publishing_house) -> NoReturn:
        self._publishing_house = new_publishing_house

    @property
    def volumes(self) -> int:
        return self._volumes

    @volumes.setter
    def volumes(self, new_amount) -> NoReturn:
        self._volumes = new_amount

    @property
    def published_amount(self) -> int:
        return self._published_amount

    @published_amount.setter
    def published_amount(self, new_amount) -> NoReturn:
        self._published_amount = new_amount

    @property
    def published_volumes_amount(self) -> int:
        return self._published_amount * self._volumes

    def json_dict(self) -> Dict:
        return {
            "name": self._name,
            "authors": self._authors,
            "publishing_house": self._publishing_house,
            "volumes": self._volumes,
            "published_amount": self._published_amount}

    def __eq__(self, other) -> bool:
        if not self._name == other.name:
            return False
        for author in self._authors:
            if author not in other.authors:
                return False
        for author in other.authors:
            if author not in self._authors:
                return False
        if not self._publishing_house == other.publishing_house:
            return False
        if not self._volumes == other.volumes:
            return False
        if not self._published_amount == other.published_amount:
            return False
        return True

    def __ne__(self, other) -> bool:
        return not self == other

    def __str__(self):
        return f"Name: {self._name}, Authors: {' ,'.join(self._authors)} in {self._volumes} volumes. Published by" \
               f" {self._publishing_house}"

    def __repr__(self):
        return f"Book<name: {self._name}, authors:{self._authors}, publishing house: {self._publishing_house}, " \
               f"volumes:{self._volumes}, published amount: {self._published_amount}>"

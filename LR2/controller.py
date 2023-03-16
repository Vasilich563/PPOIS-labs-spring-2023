from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from library import Library, SortBy, SearchRemoveBy
from book import Book
from typing import NoReturn, List
import enum
import os
import re


class ColumnsNames(enum.Enum):
    NAME = 0
    AUTHORS = 1
    PUBLISHING_HOUSE = 2
    VOLUMES = 3
    PUBLISHED = 4
    PUBLISHED_VOLUMES = 5


class SortCondition:
    def __init__(self, sort_by: SortBy = SortBy.NAME_SORT, reverse_order=False):
        self._sort_by = sort_by
        self._reverse_order = reverse_order

    @property
    def sort_by(self) -> SortBy:
        return self._sort_by

    @sort_by.setter
    def sort_by(self, new_sort_param: SortBy) -> NoReturn:
        self._sort_by = new_sort_param

    @property
    def reverse_order(self) -> bool:
        return self._reverse_order

    @reverse_order.setter
    def reverse_order(self, new_order: bool) -> NoReturn:
        self._reverse_order = new_order


class Controller:

    _books_on_page: int = 10

    def __init__(self, lib: Library):
        if not isinstance(lib, Library):
            raise TypeError(f"lib must be {type(Library)}. Got {type(lib)} instead")
        self._lib = lib
        self._current_page = 0
        self._sort_condition = SortCondition()
        lib.sort_by(self.sort_condition.sort_by, self.sort_condition.reverse_order)

    @property
    def sort_condition(self) -> SortCondition:
        return self._sort_condition

    @property
    def lib(self) -> Library:
        return self._lib

    @property
    def books_on_page(self) -> int:
        return self._books_on_page

    @property
    def page(self) -> int:
        return self._current_page

    def load_next_page(self, ui_main_window) -> NoReturn:
        self.update_table(ui_main_window)
        if self._current_page < (len(self._lib.books) / self._books_on_page) - 1:
            self._current_page += 1
            self.load_current_page(ui_main_window)

    def load_prev_page(self, ui_main_window) -> NoReturn:
        self.update_table(ui_main_window)
        if self._current_page > 0:
            self._current_page -= 1
            self.load_current_page(ui_main_window)

    def load_first_page(self, ui_main_window) -> NoReturn:
        self.update_table(ui_main_window)
        self._current_page = 0
        self.load_current_page(ui_main_window)

    def load_last_page(self, ui_main_window) -> NoReturn:
        self.update_table(ui_main_window)
        if len(self.lib.books) % self._books_on_page == 0:
            self._current_page = len(self.lib.books) // self._books_on_page - 1
        else:
            self._current_page = len(self.lib.books) // self._books_on_page
        self.load_current_page(ui_main_window)

    @staticmethod
    def _set_item_of_table(ui_main_window, row_number: int, column_name: ColumnsNames, table_item) -> NoReturn:
        ui_main_window.table_page.setItem(
            row_number,
            column_name.value,
            QtWidgets.QTableWidgetItem(table_item))

    def load_current_page(self, ui_main_window) -> NoReturn:
        labels = [str(index) for index in range(self._current_page * self._books_on_page + 1,
                                                (self._current_page + 1) * self._books_on_page + 1)
                  if index <= len(self._lib.books)]
        ui_main_window.table_page.setVerticalHeaderLabels(labels)
        row = 0
        ui_main_window.table_page.setRowCount(len(
                                              self._lib.books[self._current_page * self._books_on_page:
                                                              (self._current_page + 1) * self._books_on_page]))
        for book in self._lib.books[self._current_page * self._books_on_page:
                                    (self._current_page + 1) * self._books_on_page]:
            if row >= self._books_on_page:
                break
            self._set_item_of_table(ui_main_window, row, ColumnsNames.NAME, book.name)
            authors_str = ", ".join(book.authors)
            self._set_item_of_table(ui_main_window, row, ColumnsNames.AUTHORS, authors_str)
            self._set_item_of_table(ui_main_window, row, ColumnsNames.PUBLISHING_HOUSE, book.publishing_house)
            self._set_item_of_table(ui_main_window, row, ColumnsNames.VOLUMES, str(book.volumes))
            self._set_item_of_table(ui_main_window, row, ColumnsNames.PUBLISHED, str(book.published_amount))
            self._set_item_of_table(ui_main_window, row, ColumnsNames.PUBLISHED_VOLUMES,
                                    str(book.published_volumes_amount))
            row += 1

    @staticmethod
    def _autosave_name() -> str:
        regex = re.compile(r"^autosave([1-9]\d*)\.json$")
        filename_indexes = [int(regex.match(file).group(1)) for file in os.listdir("./saves") if regex.match(file)]
        if not filename_indexes:
            filename_indexes.append(1)
        return f"./saves/autosave{max(filename_indexes) + 1}.json"

    def save_library_as(self, filename) -> NoReturn:
        self._lib.save(filename)

    def save_library(self) -> NoReturn:
        if not self.lib.saved_flag:
            filename = self._lib.save_filename if self._lib.save_filename else Controller._autosave_name()
            self._lib.save(filename)

    def load_library(self, filename) -> NoReturn:
        self._lib = self._lib.load(filename)

    @staticmethod
    def _change_sort_conditions_arguments_correct(**kwargs) -> NoReturn:
        if not len(kwargs) == 1:
            raise ValueError(f"expected 1 key argument, got {len(kwargs)} instead")
        for key in kwargs.keys():
            if key != "reverse_order" and key != "sort_by":
                raise ValueError(f"Unknown positional argument: {key}")
            if key == "sort_by":
                if not isinstance(kwargs[key], SortBy):
                    raise TypeError(f"Unknown type for sort_by arg. Expected {type(SortBy)},"
                                    f" got {type(kwargs[key])} instead")

    @staticmethod
    def _sort_params_can_be_changed(ui_main_window, **kwargs) -> bool:
        kwargs["sort_by"] = kwargs.get("sort_by", "No_Param")
        kwargs["reverse_order"] = kwargs.get("reverse_order", "No_Param")
        if not ui_main_window.sort_by_name_act.isChecked() and \
            not ui_main_window.sort_by_published_amount_act.isChecked() and \
                not ui_main_window.sort_by_publishing_house_act.isChecked() and kwargs["sort_by"] == SortBy.NAME_SORT:
            ui_main_window.sort_by_name_act.setChecked(True)
            return False
        elif not ui_main_window.sort_by_published_amount_act.isChecked() and \
            not ui_main_window.sort_by_name_act.isChecked() and \
                not ui_main_window.sort_by_publishing_house_act.isChecked() and \
                kwargs["sort_by"] == SortBy.PUBLISHED_AMOUNT_SORT:
            ui_main_window.sort_by_published_amount_act.setChecked(True)
            return False
        elif not ui_main_window.sort_by_publishing_house_act.isChecked() and \
            not ui_main_window.sort_by_published_amount_act.isChecked() and \
                not ui_main_window.sort_by_name_act.isChecked() and kwargs["sort_by"] == SortBy.PUBLISHING_HOUSE_SORT:
            ui_main_window.sort_by_publishing_house_act.setChecked(True)
            return False
        if not ui_main_window.direct_sort_act.isChecked() and not ui_main_window.reverse_sort_act.isChecked() and \
           kwargs["reverse_order"] == False:
            ui_main_window.direct_sort_act.setChecked(True)
            return False
        elif not ui_main_window.reverse_sort_act.isChecked() and not ui_main_window.direct_sort_act.isChecked() and \
                kwargs["reverse_order"] == True:
            ui_main_window.reverse_sort_act.setChecked(True)
            return False
        return True

    def _sort_books_in_lib(self) -> NoReturn:
        self._lib.sort_by(self.sort_condition.sort_by, self.sort_condition.reverse_order)

    def _change_sort_params(self, ui_main_window, **kwargs) -> NoReturn:
        for key in kwargs.keys():
            if key == "reverse_order":
                if kwargs[key]:
                    ui_main_window.direct_sort_act.setChecked(False)
                    self._sort_condition.reverse_order = True
                else:
                    ui_main_window.reverse_sort_act.setChecked(False)
                    self._sort_condition.reverse_order = False
            else:
                if kwargs[key] == SortBy.NAME_SORT:
                    self.sort_condition.sort_by = SortBy.NAME_SORT
                    ui_main_window.sort_by_published_amount_act.setChecked(False)
                    ui_main_window.sort_by_publishing_house_act.setChecked(False)
                elif kwargs[key] == SortBy.PUBLISHING_HOUSE_SORT:
                    ui_main_window.sort_by_published_amount_act.setChecked(False)
                    ui_main_window.sort_by_name_act.setChecked(False)
                    self.sort_condition.sort_by = SortBy.PUBLISHING_HOUSE_SORT
                elif kwargs[key] == SortBy.PUBLISHED_AMOUNT_SORT:
                    ui_main_window.sort_by_name_act.setChecked(False)
                    ui_main_window.sort_by_publishing_house_act.setChecked(False)
                    self.sort_condition.sort_by = SortBy.PUBLISHED_AMOUNT_SORT

    def sort_lib(self, ui_main_window, **kwargs) -> NoReturn:
        self._change_sort_conditions_arguments_correct(**kwargs)
        if not self._sort_params_can_be_changed(ui_main_window, **kwargs):
            return
        self._change_sort_params(ui_main_window, **kwargs)
        self._sort_books_in_lib()
        self.load_current_page(ui_main_window)

    @staticmethod
    def _table_input_error(error_code: int, wracked_data: str, element_number: int) -> QMessageBox:
        detailed_text = f"При изменении данных книги под номером {element_number + 1} произошла ошибка: были введены " \
                        f"некорретные данные в столбце \"" \
                        f"{'Тираж' if error_code == ColumnsNames.PUBLISHED.value else 'Количество томов'}\". Ожидалось"\
                        f" натуральное число или 0, но было введено \"{wracked_data}\". Данные из этой строки не были" \
                        f" изменены."
        error = QMessageBox()
        error.setWindowTitle("Ошибка")
        error.setText("Вы ввели некорректные данные!")
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        error.setDefaultButton(QMessageBox.Ok)
        error.setDetailedText(detailed_text)
        error.adjustSize()
        return error

    def update_table(self, ui_main_wind) -> NoReturn:
        for i in range(len(self.lib.books[self._current_page * self._books_on_page:
                                          (self._current_page + 1) * self._books_on_page])):
            if not re.match(r"^0$|^[1-9]\d*$", ui_main_wind.table_page.item(i, ColumnsNames.VOLUMES.value).text()):
                self._table_input_error(ColumnsNames.VOLUMES.value,
                                        wracked_data=ui_main_wind.table_page.item(i, ColumnsNames.VOLUMES.value).text(),
                                        element_number=i).exec()
                continue
            if not re.match(r"^0$|^[1-9]\d*$", ui_main_wind.table_page.item(i, ColumnsNames.PUBLISHED.value).text()):
                self._table_input_error(ColumnsNames.PUBLISHED.value,
                                        wracked_data=ui_main_wind.table_page.item(i, ColumnsNames.PUBLISHED.value).text(),
                                        element_number=i).exec()
                continue
            book_in_table = Book(
                name=ui_main_wind.table_page.item(i, ColumnsNames.NAME.value).text(),
                authors=ui_main_wind.table_page.item(i, ColumnsNames.AUTHORS.value).text().split(", "),
                publishing_house=ui_main_wind.table_page.item(i, ColumnsNames.PUBLISHING_HOUSE.value).text(),
                volumes=int(ui_main_wind.table_page.item(i, ColumnsNames.VOLUMES.value).text()),
                published_amount=int(ui_main_wind.table_page.item(i, ColumnsNames.PUBLISHED.value).text()))
            if self._lib.books[self._current_page * self._books_on_page + i] != book_in_table:
                self._lib.books[self._current_page * self._books_on_page + i] = book_in_table
        self.load_current_page(ui_main_wind)

# -*- coding: utf-8 -*-
from typing import NoReturn

# Author: Vodohleb04
# Form implementation generated from reading ui file 'removeDialogWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from enum import Enum
from library import SearchRemoveBy


class RemoveTypeNames(Enum):
    REMOVE_NOT_CHOSEN = "Удаление..."
    NAME = "по названию"
    AUTHORS = "по авторам"
    AUTHORS_PUBLISHING_HOUSE = "по издательству и авторам"
    VOLUMES = "по числу томов"
    PUBLISHED = "по тиражу"
    PUBLISHED_VOLUMES = "по количеству выпущенных томов"


class Ui_removeDialog(object):
    def setupUi(self, ui_main_window, mainWindow, removeDialog, data_controller):
        removeDialog.setObjectName("removeDialog")
        removeDialog.resize(529, 73)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/png-transparent-rubbish-bins-waste-paper-baskets-recycling-bin-computer-icons-trash-miscellaneous-recycling-logo-thumbnail-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        removeDialog.setWindowIcon(icon)
        removeDialog.setStyleSheet("background-color: rgb(255, 225, 230);")
        self.removeButtonBox = QtWidgets.QDialogButtonBox(removeDialog)
        self.removeButtonBox.setGeometry(QtCore.QRect(330, 20, 171, 31))
        self.removeButtonBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.removeButtonBox.setStyleSheet("background-color: rgb(199, 214, 255);")
        self.removeButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.removeButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.removeButtonBox.setObjectName("removeButtonBox")
        self.removeButtonBox.button(self.removeButtonBox.Ok).setEnabled(False)
        self.removeComboBox = QtWidgets.QComboBox(removeDialog)
        self.removeComboBox.setGeometry(QtCore.QRect(20, 20, 281, 31))
        self.removeComboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.removeComboBox.setStyleSheet("background-color: rgb(199, 214, 255);")
        self.removeComboBox.setObjectName("removeComboBox")
        self.removeComboBox.addItem("")
        self.removeComboBox.addItem("")
        self.removeComboBox.addItem("")
        self.removeComboBox.addItem("")
        self.removeComboBox.addItem("")
        self.removeComboBox.addItem("")
        self.removeComboBox.addItem("")

        self.retranslateUi(removeDialog)
        self.removeButtonBox.accepted.connect(removeDialog.accept)
        self.removeButtonBox.rejected.connect(removeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(removeDialog)

        self.removeComboBox.textActivated.connect(lambda: self.connect_combo_box_changed(data_controller))

        self.removeButtonBox.button(self.removeButtonBox.Cancel).clicked.connect(
            lambda: data_controller.choose_remove_type(None))
        self.removeButtonBox.button(self.removeButtonBox.Ok).clicked.connect(
            lambda: data_controller.remove_books(ui_main_window, mainWindow))

    def retranslateUi(self, removeDialog):
        _translate = QtCore.QCoreApplication.translate
        removeDialog.setWindowTitle(_translate("removeDialog", "Удаление"))
        self.removeComboBox.setItemText(0, _translate("removeDialog", RemoveTypeNames.REMOVE_NOT_CHOSEN.value))
        self.removeComboBox.setItemText(1, _translate("removeDialog", RemoveTypeNames.AUTHORS.value))
        self.removeComboBox.setItemText(2, _translate("removeDialog", RemoveTypeNames.AUTHORS_PUBLISHING_HOUSE.value))
        self.removeComboBox.setItemText(3, _translate("removeDialog", RemoveTypeNames.VOLUMES.value))
        self.removeComboBox.setItemText(4, _translate("removeDialog", RemoveTypeNames.NAME.value))
        self.removeComboBox.setItemText(5, _translate("removeDialog", RemoveTypeNames.PUBLISHED.value))
        self.removeComboBox.setItemText(6, _translate("removeDialog", RemoveTypeNames.PUBLISHED_VOLUMES.value))

    def connect_combo_box_changed(self, data_controller) -> NoReturn:
        remove_type = None
        if self.removeComboBox.currentIndex() == 0:
            self.removeButtonBox.button(self.removeButtonBox.Ok).setEnabled(False)
        else:
            self.removeButtonBox.button(self.removeButtonBox.Ok).setEnabled(True)
            if self.removeComboBox.currentText() == RemoveTypeNames.AUTHORS.value:
                remove_type = SearchRemoveBy.AUTHORS
            elif self.removeComboBox.currentText() == RemoveTypeNames.AUTHORS_PUBLISHING_HOUSE.value:
                remove_type = SearchRemoveBy.PUBLISHING_HOUSE_AND_AUTHORS
            elif self.removeComboBox.currentText() == RemoveTypeNames.NAME.value:
                remove_type = SearchRemoveBy.BOOK_NAME
            elif self.removeComboBox.currentText() == RemoveTypeNames.VOLUMES.value:
                remove_type = SearchRemoveBy.VOLUMES_AMOUNT
            elif self.removeComboBox.currentText() == RemoveTypeNames.PUBLISHED.value:
                remove_type = SearchRemoveBy.PUBLISHED_AMOUNT
            elif self.removeComboBox.currentText() == RemoveTypeNames.PUBLISHED_VOLUMES.value:
                remove_type = SearchRemoveBy.PUBLISHED_VOLUMES_AMOUNT
        data_controller.choose_remove_type(remove_type)


from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QListWidget,
                               QLineEdit, QLabel, QDoubleSpinBox, QDialogButtonBox, QSpacerItem, QSizePolicy)

from user import User
from products import *
from GUI_popups import DoubleInputPopup, ProductPopup
from GUI_search_dialog import SearchProductsDialog


class ProductTypeListWidget(QListWidget):
    def __init__(self, product_list: list[ProductType], parent=None):
        super().__init__(parent=parent)
        self.product_list = product_list
        self.itemDoubleClicked.connect(self.display_selected_product_info)
        self.refresh_list()

    def refresh_list(self):
        self.clear()
        self.addItems([product.name for product in self.product_list])

    def display_selected_product_info(self):
        if self.currentRow() >= 0:
            ProductPopup(self.product_list[self.currentRow()], parent=self).exec()

    def delete_selected_product(self):
        if self.currentRow() >= 0:
            self.product_list.pop(self.currentRow())
            self.refresh_list()

    def get_selected(self) -> ProductType | None:
        if self.currentRow() >= 0:
            return self.product_list[self.currentRow()]
        else:
            return None


class ProductListWidget(QListWidget):
    def __init__(self, product_list: list[Product], parent=None):
        super().__init__(parent=parent)
        self.product_list = product_list
        self.itemDoubleClicked.connect(self.display_selected_product_info)
        self.refresh_list()

    def refresh_list(self):
        self.clear()
        self.addItems([str(product) for product in self.product_list])

    def display_selected_product_info(self):
        if self.currentRow() >= 0:
            ProductPopup(self.product_list[self.currentRow()].product_type, parent=self).exec()

    def delete_selected_product(self):
        if self.currentRow() >= 0:
            self.product_list.pop(self.currentRow())
            self.refresh_list()

    def add_product_from_api(self):
        product_type_dialog = SearchProductsDialog(self)
        if product_type_dialog.exec() == QDialog.DialogCode.Accepted:
            product_type = product_type_dialog.selected_product_type
            self.add_product_by_type(product_type)

    def add_product(self, product: Product):
        self.product_list.append(product)
        self.refresh_list()

    def add_product_by_type(self, product_type: ProductType):
        product_weight_dialog = DoubleInputPopup(parent=self, title=f"Add {product_type.name}",
                                                 label_text="Enter weight:")
        if product_weight_dialog.exec() == QDialog.DialogCode.Accepted:
            weight = product_weight_dialog.get_value()
            self.product_list.append(Product(product_type, weight))
            self.refresh_list()

    def get_selected(self) -> Product | None:
        if self.currentRow() >= 0:
            return self.product_list[self.currentRow()]
        else:
            return None

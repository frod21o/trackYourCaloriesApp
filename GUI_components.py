from PySide6.QtWidgets import QDialog, QListWidget

from products import *
from GUI_popups import DoubleInputPopup, ProductPopup
from GUI_search_dialog import SearchProductsDialog


class ProductTypeListWidget(QListWidget):
    """ List widget displaying a list of ProductType objects with a lot of useful methods """
    def __init__(self, product_list: list[ProductType], parent=None):
        """
        :param product_list: list of ProductType objects, that will bye displayed
        :param parent: Set parent of the widget
        """
        super().__init__(parent=parent)
        self.product_list = product_list
        self.itemDoubleClicked.connect(self.display_selected_product_info)
        self.refresh_list()

    def refresh_list(self):
        """ Updates the content of the widget """
        self.clear()
        self.addItems([product.name for product in self.product_list])

    def display_selected_product_info(self):
        """ Launches a popup for displaying selected product type """
        if self.currentRow() >= 0:
            ProductPopup(self.product_list[self.currentRow()], parent=self).exec()

    def delete_selected_product(self):
        """ Deletes selected product type from the list """
        if self.currentRow() >= 0:
            self.product_list.pop(self.currentRow())
            self.refresh_list()

    def get_selected(self) -> ProductType | None:
        """ Returns currently selected product type """
        if self.currentRow() >= 0:
            return self.product_list[self.currentRow()]
        else:
            return None


class ProductListWidget(QListWidget):
    """ List widget displaying a list of Product objects with a lot of useful methods """
    def __init__(self, product_list: list[Product], parent=None):
        """
        :param product_list: list of Product objects, that will bye displayed
        :param parent: Set parent of the widget
        """
        super().__init__(parent=parent)
        self.product_list = product_list
        self.itemDoubleClicked.connect(self.display_selected_product_info)
        self.refresh_list()

    def refresh_list(self):
        """ Updates the content of the widget """
        self.clear()
        self.addItems([str(product) for product in self.product_list])

    def display_selected_product_info(self):
        """ Launches a popup for displaying selected product """
        if self.currentRow() >= 0:
            ProductPopup(self.product_list[self.currentRow()].product_type, parent=self).exec()

    def delete_selected_product(self):
        """ Deletes selected product from the list """
        if self.currentRow() >= 0:
            self.product_list.pop(self.currentRow())
            self.refresh_list()

    def add_product_from_api(self):
        """ Launches a dialog for adding a product from api """
        product_type_dialog = SearchProductsDialog(self)
        if product_type_dialog.exec() == QDialog.DialogCode.Accepted:
            product_type = product_type_dialog.selected_product_type
            self.add_product_by_type(product_type)

    def add_product(self, product: Product):
        """ Adds the given product to the list"""
        self.product_list.append(product)
        self.refresh_list()

    def add_product_by_type(self, product_type: ProductType):
        """ Adds a product of given type and weight entered by the user """
        product_weight_dialog = DoubleInputPopup(parent=self, title=f"Add {product_type.name}",
                                                 label_text="Enter weight:")
        if product_weight_dialog.exec() == QDialog.DialogCode.Accepted:
            weight = product_weight_dialog.get_value()
            self.product_list.append(Product(product_type, weight))
            self.refresh_list()

    def get_selected(self) -> Product | None:
        """ Returns currently selected product """
        if self.currentRow() >= 0:
            return self.product_list[self.currentRow()]
        else:
            return None

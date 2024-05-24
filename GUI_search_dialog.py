from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QListWidget,
                               QLineEdit, QLabel, QDoubleSpinBox, QDialogButtonBox)

from products import *
from GUI_popups import AddProductPopup, ProductPopup
import api_handler


class SearchProductsDialog(QDialog):
    """ Dialog for finding a product type through the api """
    recent_products: list[ProductType] = []

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.selected_product_type: ProductType = None

        self.setWindowTitle(f"Find product")
        self.resize(400, 300)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Setting search bar
        group_box = QGroupBox("Search")
        group_layout = QHBoxLayout(group_box)
        self.text_search = QLineEdit("")            # input
        group_layout.addWidget(self.text_search)
        self.button_search = QPushButton()          # button
        self.button_search.setIcon(QIcon.fromTheme("edit-find"))
        self.button_search.clicked.connect(self.search)
        group_layout.addWidget(self.button_search)
        main_layout.addWidget(group_box)

        # Setting list widget
        self.label_widget_title = QLabel()
        main_layout.addWidget(self.label_widget_title)
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.display_selected_product_info)
        main_layout.addWidget(self.list_widget)
        self.found_products = []        # initialization of important variables
        self.displaying_recent = True   #
        self.display_recent()

        # Setting add button
        self.button_add = QPushButton("Add")
        self.button_add.clicked.connect(self.add_selected_product)
        main_layout.addWidget(self.button_add)

    def display_selected_product_info(self):
        selected_product_type = self.get_selected_product_type()
        if selected_product_type:
            ProductPopup(selected_product_type, parent=self).exec()

    def display_recent(self):
        self.displaying_recent = True
        self.label_widget_title.setText("Recent products")
        self.list_widget.clear()
        recent_names = [product.name for product in SearchProductsDialog.recent_products]
        self.list_widget.addItems(reversed(recent_names))

    def search(self):
        if self.text_search.text() == "":
            self.display_recent()
            return
        self.found_products = api_handler.search_food(self.text_search.text())
        self.displaying_recent = False
        self.label_widget_title.setText("Search results")
        self.list_widget.clear()
        self.list_widget.addItems([product["food_name"] for product in self.found_products])

    def add_selected_product(self):
        self.selected_product_type = self.get_selected_product_type()
        if self.selected_product_type:
            self.accept()

    def get_selected_product_type(self) -> ProductType:
        idx = self.list_widget.currentRow()
        if idx < 0:
            return None
        if self.displaying_recent:
            return SearchProductsDialog.recent_products[~idx]
        else:
            food_id = self.found_products[idx]["nix_item_id"]
            food_info = api_handler.get_nutrition_by_id(food_id)
            product_type = ProductType(food_info['food_name'], **food_info)
            self.recent_products.append(product_type)
            return product_type

    def create_product(self, selected_product_type: ProductType):
        dialog = AddProductPopup(selected_product_type, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.created_product = Product(selected_product_type, dialog.value())
            self.accept()

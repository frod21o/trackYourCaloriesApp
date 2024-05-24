from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QFormLayout, QSpinBox, QPushButton, QLineEdit
from PySide6.QtGui import QAction
from PySide6.QtCore import QFile, QIODeviceBase
import sys

import user
from products import *


class ProductPopup(QDialog):
    """ Popup for displaying data about product and editing them if allowed """
    def __init__(self, product: ProductType, editable=False, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle(f"Product {product.name}")
        layout = QFormLayout()
        self.setLayout(layout)

        self.text_name = QLineEdit()
        self.text_name.setReadOnly(not editable)
        self.text_name.setText(product.name)
        layout.addRow("Name", self.text_name)

        self.text_nutrients = []
        for idx, nutrient in enumerate(Nutrients._fields):
            self.text_nutrients.append(QSpinBox())
            self.text_nutrients[-1].setReadOnly(not editable)
            if product.nutrients[idx] is None:
                self.text_nutrients[-1].setValue(0)
            else:
                self.text_nutrients[-1].setValue(product.nutrients[idx])
            layout.addRow(nutrient, self.text_nutrients[-1])

        def ok_action():
            if editable:
                self.save_to_product(product)
            self.close()
        button_save = QPushButton()
        button_save.setText("ok")
        button_save.clicked.connect(ok_action)
        layout.addWidget(button_save)

    def save_to_product(self, product: ProductType):
        product.name = self.text_name.text()
        product.nutrients = Nutrients(*[spinbox.value() for spinbox in self.text_nutrients])


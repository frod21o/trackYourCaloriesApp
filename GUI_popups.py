from PySide6.QtWidgets import (QDialog, QFormLayout, QVBoxLayout, QSpinBox, QPushButton,
                               QLineEdit, QLabel, QDoubleSpinBox, QDialogButtonBox)

from products import *


class ProductPopup(QDialog):
    """ Popup for displaying data about product and editing them if allowed """
    def __init__(self, product: ProductType, editable=False, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle(f"Product {product.name}")
        self.resize(400, self.minimumHeight())
        layout = QFormLayout()
        self.setLayout(layout)

        # Setting name row
        self.text_name = QLineEdit()
        self.text_name.setReadOnly(not editable)
        self.text_name.setText(product.name)
        layout.addRow("Name", self.text_name)

        # Setting nutrients rows
        self.spinbox_nutrients = []
        for idx, nutrient in enumerate(Nutrients._fields):
            self.spinbox_nutrients.append(QSpinBox())
            self.spinbox_nutrients[-1].setRange(0, 10000)
            if not editable:
                self.spinbox_nutrients[-1].setReadOnly(True)
                self.spinbox_nutrients[-1].setStyleSheet("QSpinBox::up-button { width: 0px; } "
                                                         "QSpinBox::down-button { width: 0px; }")
            if product.nutrients[idx] is None:
                self.spinbox_nutrients[-1].setValue(0)
            else:
                self.spinbox_nutrients[-1].setValue(product.nutrients[idx])
            layout.addRow(nutrient, self.spinbox_nutrients[-1])

        # Setting ok button
        if editable:
            def ok_action():
                """ Action to do when ok button clicked """
                self.save_to_product(product)
                self.accept()
            button_save = QPushButton()
            button_save.setText("ok")
            button_save.clicked.connect(ok_action)
            layout.addWidget(button_save)

    def save_to_product(self, product: ProductType):
        """ Saves all the product information in the given ProductType object """
        product.name = self.text_name.text()
        product.nutrients = Nutrients(*[spinbox.value() for spinbox in self.spinbox_nutrients])


class DoubleInputPopup(QDialog):
    def __init__(self, parent=None, title="Enter value", label_text="Enter double value"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(350, self.minimumHeight())
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.label = QLabel(label_text)
        layout.addWidget(self.label)

        # Setting weight spinbox
        self.spinbox_weight = QDoubleSpinBox()
        self.spinbox_weight.setStyleSheet("QDoubleSpinBox::up-button { width: 0px; } "
                                          "QDoubleSpinBox::down-button { width: 0px; }")
        self.spinbox_weight.setRange(0, 10000)
        layout.addWidget(self.spinbox_weight)

        # Setting buttons ok and cancel
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_value(self):
        return self.spinbox_weight.value()


class StringInputPopup(QDialog):
    def __init__(self, parent=None, title="Enter text", label_text="Enter text"):
        super().__init__(parent)
        self.resize(350, self.minimumHeight())
        self.setWindowTitle(title)

        # Create layout
        layout = QVBoxLayout(self)

        # Create and add QLineEdit to layout
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText(label_text)
        layout.addWidget(self.text_input)

        # Create QDialogButtonBox with OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                           QDialogButtonBox.StandardButton.Cancel, self)
        layout.addWidget(self.button_box)

        # Connect buttons to their respective slots
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_value(self):
        return self.text_input.text()

from PySide6.QtWidgets import (QDialog, QFormLayout, QVBoxLayout, QSpinBox, QPushButton,
                               QLineEdit, QLabel, QDoubleSpinBox, QDialogButtonBox, QMessageBox)

from products import *


class ProductPopup(QDialog):
    """ Popup for displaying data about product and editing them if allowed """

    def __init__(self, product_type: ProductType, editable=False, parent=None):
        """
        :param product_type: product type, which will be displayed
        :param editable: Indicates if user will be able to edit information about product type
        :param parent: Set parent of the widget
        """
        super().__init__(parent=parent)
        self.setWindowTitle(f"Product {product_type.name}")
        self.resize(400, self.minimumHeight())
        layout = QFormLayout()
        self.setLayout(layout)

        # Setting name row
        self.text_name = QLineEdit()
        self.text_name.setReadOnly(not editable)
        self.text_name.setText(product_type.name)
        layout.addRow("Name", self.text_name)
        layout.addRow("In 100 grams:", None)

        # Setting nutrients rows
        self.spinbox_nutrients = []
        for idx, nutrient in enumerate(Nutrients._fields):
            self.spinbox_nutrients.append(QSpinBox())
            self.spinbox_nutrients[-1].setRange(0, 10000)
            if not editable:
                self.spinbox_nutrients[-1].setReadOnly(True)
                self.spinbox_nutrients[-1].setStyleSheet("QSpinBox::up-button { width: 0px; } "
                                                         "QSpinBox::down-button { width: 0px; }")
            if product_type.nutrients[idx] is None:
                self.spinbox_nutrients[-1].setValue(0)
            else:
                self.spinbox_nutrients[-1].setValue(product_type.nutrients[idx])
            layout.addRow(nutrient, self.spinbox_nutrients[-1])

        # Setting ok button
        if editable:
            def ok_action():
                """ Action to do when ok button clicked """
                self.save_to_product(product_type)
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
    """ Popup for getting a double type value from user """
    def __init__(self, title="Enter value", label_text="Enter double value", force_positive: bool = True, parent=None):
        """
        :param title: Title of the popup window
        :param label_text: Text of the label
        :param force_positive: Indicates if popup will require positive number
        :param parent: Set parent of the widget
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(350, self.minimumHeight())
        self.force_positive = force_positive
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.label = QLabel(label_text)
        layout.addWidget(self.label)

        # Setting SpinBox widget
        self.spinbox = QDoubleSpinBox()
        self.spinbox.setStyleSheet("QDoubleSpinBox::up-button { width: 0px; } "
                                   "QDoubleSpinBox::down-button { width: 0px; }")
        self.spinbox.setRange(0, 10000)
        layout.addWidget(self.spinbox)

        # Setting OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.try_to_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def try_to_accept(self):
        """ Checks if dialog can end with Accept code """
        if self.get_value() > 0 or not self.force_positive:
            self.accept()
        else:
            message = QMessageBox()
            message.setWindowTitle('Warning')
            message.setText('Number have to be positive')
            message.exec()

    def get_value(self) -> float:
        """ Returns entered value """
        return self.spinbox.value()


class StringInputPopup(QDialog):
    """ Popup for getting a string type value from user """
    def __init__(self, title="Enter text", label_text="Enter text", parent=None):
        """
        :param title: Title of the popup window
        :param label_text: Text of the label
        :param parent: Set parent of the widget
        """
        super().__init__(parent)
        self.resize(350, self.minimumHeight())
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)

        # Setting LineEdit widget
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText(label_text)
        layout.addWidget(self.text_input)

        # Setting OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                           QDialogButtonBox.StandardButton.Cancel, self)
        self.button_box.accepted.connect(self.try_to_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def try_to_accept(self):
        """ Checks if dialog can end with Accept code """
        if self.get_value() != "":
            self.accept()
        else:
            message = QMessageBox()
            message.setWindowTitle('Warning')
            message.setText('Box can not be empty')
            message.exec()

    def get_value(self) -> str:
        """ Returns entered text """
        return self.text_input.text()

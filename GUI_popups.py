from PySide6.QtWidgets import (QDialog, QFormLayout, QVBoxLayout, QSpinBox, QPushButton, QHBoxLayout, QComboBox,
                               QLineEdit, QLabel, QDoubleSpinBox, QDialogButtonBox, QMessageBox)

from products import *
import user


class ProductPopup(QDialog):
    """ Popup for displaying data about product and editing them if allowed """

    def __init__(self, product_type: ProductType, editable=False, parent=None):
        """
        :param product_type: product type, which will be displayed
        :param editable: Indicates if user will be able to edit information about product type
        :param parent: Set parent of the widget
        """
        super().__init__(parent=parent)
        self.product_type = product_type
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
            button_save = QPushButton()
            button_save.setText("ok")
            button_save.clicked.connect(self.accept)
            layout.addWidget(button_save)

    def get_entered_nutrients(self) -> Nutrients:
        """ Return entered values as a Nutrients namedtuple """
        return Nutrients(*[spinbox.value() for spinbox in self.spinbox_nutrients])

    def accept(self):
        """ Saves values to ProductType and accepts dialog """
        self.product_type.name = self.text_name.text()
        self.product_type.nutrients = self.get_entered_nutrients()
        super().accept()


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


class UserParamsInputPopup(QDialog):
    """ Popup for editing parameters of the user """
    def __init__(self, current_user: user.User, parent=None):
        """
        :param current_user: The user whose parameters will be modified
        :param parent: Set parent of the widget
        """
        super().__init__(parent=parent)
        self.current_user = current_user

        self.setWindowTitle(f"User: {current_user.name}")
        self.resize(350, self.minimumHeight())
        layout = QVBoxLayout()

        # Gender choice
        gender_layout = QHBoxLayout()
        gender_label = QLabel("Gender:")
        self.gender_combobox = QComboBox()
        self.gender_combobox.addItems([user.MALE_STR, user.FEMALE_STR])
        if self.current_user.gender in (user.MALE_STR, user.FEMALE_STR):
            self.gender_combobox.setCurrentText(self.current_user.gender)
        else:
            self.gender_combobox.setCurrentText("")
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_combobox)
        layout.addLayout(gender_layout)

        # Age choice
        age_layout = QHBoxLayout()
        age_label = QLabel("Age (years):")
        self.age_spinbox = QSpinBox()
        self.age_spinbox.setRange(0, 150)
        self.age_spinbox.setValue(self.current_user.age)
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_spinbox)
        layout.addLayout(age_layout)

        # Height choice
        height_layout = QHBoxLayout()
        height_label = QLabel("Height (cm):")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(20, 300)
        self.height_spinbox.setValue(self.current_user.height)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_spinbox)
        layout.addLayout(height_layout)

        # Weight choice
        weight_layout = QHBoxLayout()
        weight_label = QLabel("Weight (kg):")
        self.weight_spinbox = QSpinBox()
        self.weight_spinbox.setRange(10, 300)
        self.weight_spinbox.setValue(self.current_user.weight)
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_spinbox)
        layout.addLayout(weight_layout)

        # Ok button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_values(self):
        """ Returns entered values """
        return {
            "gender": self.gender_combobox.currentText(),
            "age": self.age_spinbox.value(),
            "height": self.height_spinbox.value(),
            "weight": self.weight_spinbox.value()
        }

    def accept(self):
        """ Saves parameters and accepts dialog """
        self.current_user.set_user_parameters(**self.get_values())
        super().accept()


class UserLimitsPopup(ProductPopup):
    """ Popup for editing user limits for nutrients """
    def __init__(self, current_user: user.User, parent=None):
        """
        :param current_user: User whose limits will be edited
        :param parent: Set parent of the widget
        """
        self.current_user = current_user
        self.symbolic_product_type = ProductType(current_user.name)
        self.symbolic_product_type.nutrients = current_user.limits
        super().__init__(self.symbolic_product_type, True, parent)
        self.setWindowTitle("User nutrients limits")

    def accept(self):
        """ Saves limits and accepts dialog"""
        self.current_user.set_limits(self.get_entered_nutrients())
        super().accept()

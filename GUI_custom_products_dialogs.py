from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QSpacerItem, QSizePolicy

from user import User
from products import *
from GUI_popups import ProductPopup, StringInputPopup
from GUI_components import ProductTypeListWidget, ProductListWidget


class CustomProductsDialog(QDialog):
    """ Dialog for managing custom products of the user and adding them to eaten list """
    def __init__(self, user: User, editable=True, parent=None):
        """
        :param user: User whose custom products will be displayed and managed
        :param editable: Indicates if buttons for adding and deleting products should be created
        :param parent: Set parent of the widget
        """
        super().__init__(parent=parent)
        self.setWindowTitle(f"My products")
        self.resize(400, 300)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Setting list widget
        self.current_user = user
        self.list_widget = ProductTypeListWidget(user.get_custom_products())
        main_layout.addWidget(self.list_widget)

        # Setting buttons
        box_buttons = QGroupBox()
        box_buttons.setFlat(True)
        group_layout = QHBoxLayout(box_buttons)

        # Button for adding selected product to eaten list
        self.button_eat = QPushButton(box_buttons)
        self.button_eat.setText("use")
        self.button_eat.clicked.connect(self.try_eating)
        group_layout.addWidget(self.button_eat)

        if editable:
            # Setting buttons for creating and deleting custom product types
            group_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

            # Button for adding brand-new product type
            self.button_add_new = QPushButton()
            self.button_add_new.setIcon(QIcon(QIcon.fromTheme(u"list-add")))
            self.button_add_new.setText("new")
            self.button_add_new.clicked.connect(self.add_new_product_type)
            group_layout.addWidget(self.button_add_new)

            # Button for adding product type made out of other products
            self.button_add_combined = QPushButton(box_buttons)
            self.button_add_combined.setIcon(QIcon(QIcon.fromTheme(u"list-add")))
            self.button_add_combined.setText("combined")
            self.button_add_combined.clicked.connect(self.add_combined_product_type)
            group_layout.addWidget(self.button_add_combined)

            # Button for removing product from list
            self.button_delete = QPushButton(box_buttons)
            self.button_delete.setIcon(QIcon(QIcon.fromTheme(u"list-remove")))
            self.button_delete.clicked.connect(self.list_widget.delete_selected_product)
            group_layout.addWidget(self.button_delete)
        main_layout.addWidget(box_buttons)

    def selected_product_type(self):
        """ Returns a selected product type """
        return self.list_widget.get_selected()

    def try_eating(self):
        """ If product type is selected closes the dialog with Accept code """
        if self.selected_product_type():
            self.accept()

    def add_new_product_type(self):
        """ Launches a product popup for user to enter all the information to create new product type """
        new_product = ProductType("new product")
        dialog = ProductPopup(new_product, True, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_user.add_custom_product(new_product)
            self.list_widget.refresh_list()

    def add_combined_product_type(self):
        """ Launches a dialog for creating a list of products and combines them into one product type """
        dialog = ProductListDialog(self.current_user, self)
        dialog.setWindowTitle("Combine products")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            get_name_dialog = StringInputPopup(title="Creating product", label_text="Enter product name", parent=self)
            if get_name_dialog.exec() == QDialog.DialogCode.Accepted:
                combined_product_type = ProductType.combine_products(get_name_dialog.get_value(), dialog.created_list)
                self.current_user.add_custom_product(combined_product_type)
                self.list_widget.refresh_list()


class ProductListDialog(QDialog):
    """ Dialog for creating a product list """
    def __init__(self, user: User, parent=None):
        """
        :param user: User whose custom products can be added to list
        :param parent: Set parent of the widget
        """
        super().__init__(parent=parent)
        self.setWindowTitle("Product list")
        self.resize(400, 300)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Setting list widget
        self.current_user = user
        self.created_list: list[Product] = []
        self.list_widget = ProductListWidget(self.created_list, self)
        main_layout.addWidget(self.list_widget)

        # Setting buttons
        box_buttons = QGroupBox()
        group_layout = QHBoxLayout(box_buttons)

        # Button for adding confirmation
        self.button_confirm = QPushButton(box_buttons)      # Confirm button
        self.button_confirm.setText("confirm")
        self.button_confirm.clicked.connect(lambda: self.accept() if self.created_list != [] else self.reject())
        group_layout.addWidget(self.button_confirm)

        group_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Button for adding a product from custom products
        self.button_add_custom = QPushButton(box_buttons)
        self.button_add_custom.setIcon(QIcon(QIcon.fromTheme(u"list-add")))
        self.button_add_custom.setText("my product")
        self.button_add_custom.clicked.connect(self.add_custom_product)
        group_layout.addWidget(self.button_add_custom)

        # Button for adding a product from api
        self.button_add_search = QPushButton(box_buttons)
        self.button_add_search.setIcon(QIcon(QIcon.fromTheme(u"list-add")))
        self.button_add_search.clicked.connect(self.list_widget.add_product_from_api)
        group_layout.addWidget(self.button_add_search)

        # Button for deleting selected product
        self.button_delete = QPushButton(box_buttons)
        self.button_delete.setIcon(QIcon(QIcon.fromTheme(u"list-remove")))
        self.button_delete.clicked.connect(self.list_widget.delete_selected_product)
        group_layout.addWidget(self.button_delete)

        main_layout.addWidget(box_buttons)

    def add_custom_product(self):
        """ Launches a dialog for adding a product from users custom products list """
        dialog = CustomProductsDialog(self.current_user, parent=self, editable=False)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.list_widget.add_product_by_type(dialog.selected_product_type())
            self.list_widget.refresh_list()

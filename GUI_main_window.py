from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction
from PySide6.QtCore import QFile, QIODeviceBase
import sys

from GUI_popups import *
from GUI_search_dialog import SearchProductsDialog
from GUI_custom_products_dialogs import CustomProductsDialog
from GUI_components import ProductListWidget
# from GUI_graph_window import GraphWindow


class MyMainWindow(QMainWindow):
    """ Main window of the app, mostly loaded from the main_window.ui file """
    def __init__(self):
        super().__init__()

        # Loading ui from the .ui file
        loader = QUiLoader()
        file = QFile("main_window.ui")
        file.open(QIODeviceBase.ReadOnly)
        self.ui = loader.load(file)
        file.close()
        self.setWindowTitle(self.ui.windowTitle())
        self.resize(366, 508)
        self.setCentralWidget(self.ui)

        # Setting up user menu
        self.users = user.get_available_users()
        if len(self.users) <= 0:
            self.users.append("newUser")
        self.user_actions = []
        self.setup_users_menu()

        # Setting up statistics menu
        # self.ui.action_graph.triggered.connect(lambda: GraphWindow(self).show())
        self.ui.action_set_parameters.triggered.connect(lambda: UserParamsInputPopup(self.current_user, self).exec())
        self.ui.action_set_limits.triggered.connect(lambda: UserLimitsPopup(self.current_user, self).exec())

        # Setting up list widget displaying products from the eaten list Set parent of the widget
        self.eaten_list_widget = ProductListWidget([], self)
        self.ui.list_widget_container.layout().addWidget(self.eaten_list_widget)

        # Selecting a user
        self.current_user: user.User = None
        self.select_user(0)

        # Setting up date widget
        self.ui.date_select.dateChanged.connect(self.new_date_selected)
        self.ui.date_select.setMaximumDate(user.current_date())

        # Setting up buttons
        self.ui.button_delete.clicked.connect(self.delete_selected_product)
        self.ui.button_add.clicked.connect(self.add_eaten_product)
        self.ui.button_my_products.clicked.connect(self.add_eaten_custom_product)

    def setup_users_menu(self):
        """ Redoes the user menu - clears it and adds all users from the list """
        self.user_actions.clear()
        self.ui.menu_users.clear()
        for idx, username in enumerate(self.users):
            action = QAction(self)
            action.setObjectName(f"user_action{idx}")
            action.setCheckable(True)
            action.setText(username)
            action.triggered.connect(lambda checked, idx_inner=idx: self.select_user(idx_inner, checked))
            self.user_actions.append(action)
            self.ui.menu_users.addAction(action)
        self.ui.menu_users.addSeparator()
        action = QAction(self)
        action.setObjectName(f"add_user_action")
        action.setText("Add new user")
        action.triggered.connect(self.add_user)
        self.ui.menu_users.addAction(action)

    def select_user(self, user_idx: int, other_selected: bool = True):
        """
        Makes all necessary changes when selecting a user

        :param user_idx: Index of the user to be selected
        :param other_selected: True if the user to be selected is different from the current selected user
        """
        if not other_selected:
            self.user_actions[user_idx].setChecked(True)
            return
        for action in self.user_actions:
            action.setChecked(False)
        self.user_actions[user_idx].setChecked(True)
        self.current_user = user.User(self.users[user_idx])
        self.ui.date_select.setDate(user.current_date())
        self.refresh_eaten_info()

    def add_user(self):
        """ Adds a new user to the list, takes care of everything that should be updated """
        dialog = StringInputPopup(title="Add user", label_text="Ener user name", parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.users.append(dialog.get_value())
            self.setup_users_menu()
            self.select_user(-1)
            self.current_user.save_data()

    def is_today_selected(self) -> bool:
        """ Returns True if current date is selected """
        return self.ui.date_select.date() == user.current_date()

    def new_date_selected(self):
        """ Takes care of everything, that should be updated after changing a date """
        should_enable_edit = self.is_today_selected()
        self.ui.button_add.setEnabled(should_enable_edit)
        self.ui.button_delete.setEnabled(should_enable_edit)
        self.refresh_eaten_info()

    def refresh_eaten_info(self):
        """ Updates every information about eaten products """
        self.eaten_list_widget.product_list = self.current_user.get_eaten_products(self.ui.date_select.date())
        self.eaten_list_widget.refresh_list()
        self.display_calories_sum()

    def display_calories_sum(self):
        calories, correct = self.current_user.count_nutrients(
            Nutrients._fields.index("nf_calories"), self.ui.date_select.date())
        if correct:
            self.ui.text_calories.setText(f"{calories:.2f} kcal")
        else:
            self.ui.text_calories.setText(f"At least {calories:.2f} kcal (not every value given)")

    def add_eaten_product(self):
        """ Launches a dialog, that allows the user to add a product from api to eaten list"""
        product_type_dialog = SearchProductsDialog(self)
        if product_type_dialog.exec() == QDialog.DialogCode.Accepted:
            product_type = product_type_dialog.selected_product_type
            self.eaten_list_widget.add_product_by_type(product_type)
            self.display_calories_sum()
            self.current_user.save_data()

    def add_eaten_custom_product(self):
        """ Launches a dialog, that allows the user to manage his own products and to add one of them to eaten list"""
        product_type_dialog = CustomProductsDialog(self.current_user, self)
        if product_type_dialog.exec() == QDialog.DialogCode.Accepted:
            product_type = product_type_dialog.selected_product_type()
            self.eaten_list_widget.add_product_by_type(product_type)
            self.display_calories_sum()
            self.current_user.save_data()

    def delete_selected_product(self):
        self.eaten_list_widget.delete_selected_product()
        self.display_calories_sum()


def run():
    """ Launches the application """
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())

import time

from PySide6.QtWidgets import QApplication, QMainWindow, QDateEdit, QMenu, QListWidget, QListWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction
from PySide6.QtCore import QFile, QIODeviceBase, QDate
import sys

import user
from GUI_popups import *


class MyMainWindow(QMainWindow):
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

        # Selecting a user
        self.current_user: user.User = None
        self.select_user(0)

        # Setting up displaying products from the ate list
        def display_clicked_product(item: QListWidgetItem):
            selected_date = self.ui.date_select.date()
            product_idx = self.ui.list_ate_products.row(item)
            ProductPopup(self.current_user.get_ate_products(selected_date)[product_idx].product_type).exec()
        self.ui.list_ate_products.itemDoubleClicked.connect(display_clicked_product)

        # Setting up date widget
        def new_date_selected():
            should_enable_edit = self.is_today_selected()
            # QPushButton().
            self.ui.button_add.setEnabled(should_enable_edit)
            self.ui.button_delete.setEnabled(should_enable_edit)
            self.refresh_ate_list()
        self.ui.date_select.dateChanged.connect(new_date_selected)
        self.ui.date_select.setMaximumDate(user.current_date())

        # Setting up buttons
        self.ui.button_delete.clicked.connect(self.delete_ate_product)

        self.example_product = ProductType("ziarno", nf_calories=3, other=0)
        self.ui.button_add.clicked.connect(lambda: ProductPopup(self.example_product, parent=self).exec())

    def setup_users_menu(self):
        for idx, username in enumerate(self.users):
            action = QAction(self)
            action.setObjectName(f"user_action{idx}")
            action.setCheckable(True)
            action.setText(username)
            action.triggered.connect(lambda checked, idx_inner=idx: self.select_user(idx_inner, checked))
            self.user_actions.append(action)
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
        self.refresh_ate_list()
        # TODO

    def is_today_selected(self) -> bool:
        return self.ui.date_select.date() == user.current_date()

    def refresh_ate_list(self):
        products_names = [str(product) for product in self.current_user.get_ate_products(self.ui.date_select.date())]
        self.ui.list_ate_products.clear()
        self.ui.list_ate_products.addItems(products_names)

    def delete_ate_product(self):
        QListWidget().currentRow()
        current_product_idx = self.ui.list_ate_products.currentRow()
        if current_product_idx >= 0 and self.is_today_selected():
            self.current_user.del_ate_product(current_product_idx)
            self.refresh_ate_list()



def run():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())


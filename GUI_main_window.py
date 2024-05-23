import time

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction
from PySide6.QtCore import QFile, QIODeviceBase
import sys

import user


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = QMainWindow()
        # Loading ui from the .ui file
        loader = QUiLoader()
        file = QFile("main_window.ui")
        file.open(QIODeviceBase.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()

        self.ui.show()
        time.sleep(5)
        self.ui.closeEvent = self.closeEvent
        self.ui.close()
        # self.ui.hideEvent = lambda: print("gide")

        # Podłączamy sygnał closeEvent do metody closeEvent
        # self.ui.closeEvent = self.closeEvent

        # self.setCentralWidget(self.ui)
        # self.ui.closeEvent = self.closeEvent
        # self.ui.centralwidget.destroyed.connect(lambda: print("halo3")) #self.destroy)
        # self.ui.destroyed.connect(lambda: print("halo")) #self.destroy)
        # self.destroyed.connect(lambda: print("halo2"))

        # Setting up user menu
        self.users = user.get_available_users()
        if len(self.users) <= 0:
            self.users.append("newUser")
        self.user_actions = []
        for idx, username in enumerate(self.users):
            action = QAction(self)
            action.setObjectName(f"user_action{idx}")
            action.setCheckable(True)
            action.setText(username)
            action.triggered.connect(lambda checked, idx_inner=idx: self.choose_user(checked, idx_inner))
            self.user_actions.append(action)
            # self.ui.menu_users.addAction(action)
        print(self.user_actions)
        self.choose_user(True, 0)

    def choose_user(self, chose_other: bool, user_idx: int):
        if not chose_other:
            self.user_actions[user_idx].setChecked(True)
            return
        for action in self.user_actions:
            action.setChecked(False)
        self.user_actions[user_idx].setChecked(True)
        # TODO

    def closeEvent(self, event):
        super().closeEvent(event)
        print("wywołane")


def run():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    # main_window.ui.show()
    # main_window.cl
    app.exec_()
    # sys.exit(app.exec())


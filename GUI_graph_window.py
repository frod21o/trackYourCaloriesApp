from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QGroupBox, QHBoxLayout, QLabel, QFrame, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns

from user import User, current_date
from products import Nutrients


class MplCanvas(FigureCanvas):
    """ Matpoltlib canvas, that can be displayed in the Pyside6 window """
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class GraphWindow(QMainWindow):
    """ Window for displaying a graph with selected nutrient consumption for given user """
    def __init__(self, user: User, parent=None):
        """
        :param user: User, whose consumption will be displayed
        :param parent:  Set parent of the widget
        """
        super().__init__(parent)
        self.setWindowTitle(f"Consumption of user {user.name}")
        self.user = user

        # Create the Matplotlib canvas
        self.canvas = MplCanvas(width=10, height=8, dpi=100)

        # Set the central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # ----- Settings -----

        group_box = QGroupBox("Graph settings")
        group_layout = QHBoxLayout()
        group_box.setLayout(group_layout)

        # Label: "nutrient: "
        nutrient_label = QLabel("Nutrient: ")
        group_layout.addWidget(nutrient_label)

        # ComboBox for selecting nutrient
        self.nutrient_combobox = QComboBox()
        self.nutrient_combobox.addItems(Nutrients._fields)
        self.nutrient_combobox.currentTextChanged.connect(self.print_graph)
        group_layout.addWidget(self.nutrient_combobox)

        # Graphic separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        group_layout.addWidget(separator)

        # Label: "From last"
        last_label = QLabel("From last")
        group_layout.addWidget(last_label)

        # ComboBox for number of days
        self.days_combobox = QComboBox()
        self.days_combobox.addItems([str(i) for i in range(3, 31)])
        self.days_combobox.currentTextChanged.connect(self.print_graph)
        group_layout.addWidget(self.days_combobox)

        # Label: "days"
        days_label = QLabel("days")
        group_layout.addWidget(days_label)

        layout.addWidget(group_box)

        # Generate a Seaborn plot and draw it on the canvas
        self.print_graph()

    def print_graph(self):
        """ Printing a graph onto the canvas """
        # Generating data
        nutrient_label = f"{self.nutrient_combobox.currentText()} (g)"
        nutrient_history = {
            "day ago": [],
            nutrient_label: []
        }
        nutrient_idx = Nutrients._fields.index(self.nutrient_combobox.currentText())
        for days in reversed(range(int(self.days_combobox.currentText()))):
            iteration_date = current_date().addDays(-days)
            nutrient_history["day ago"].append(days) #iteration_date.toString())
            nutrient_history[nutrient_label].append(self.user.count_nutrients(nutrient_idx, iteration_date)[0])

        self.canvas.axes.cla()

        # Adding graph
        sns.barplot(x="day ago", y=nutrient_label, data=nutrient_history, ax=self.canvas.axes)
        self.canvas.axes.set_ylim(bottom=0)

        # Adding lines for limit and ppm
        limit_value = self.user.limits[nutrient_idx]
        if limit_value > 0:
            self.canvas.axes.axhline(limit_value, color='red', linestyle='--', linewidth=2,
                                     label=f'Limit: {limit_value:.2f}')
        if self.nutrient_combobox.currentText() == "nf_calories" and self.user.get_ppm:
            self.canvas.axes.axhline(self.user.get_ppm, color='green', linestyle='--', linewidth=2,
                                     label=f'PPM: {self.user.get_ppm:.2f}')

        # Printing
        self.canvas.draw()

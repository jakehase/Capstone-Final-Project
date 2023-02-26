import sys

import pandas as pd
import processing
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class QGISImporter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.csv_file = None
        self.layer_name = 'imported_csv'
        self.df = None

        self.setWindowTitle("QGIS Data Importer")
        self.setGeometry(50, 50, 800, 600)

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("File")

        load_file_action = QtWidgets.QAction("Open CSV", self)
        load_file_action.setShortcut("Ctrl+O")
        load_file_action.triggered.connect(self.load_file)
        self.file_menu.addAction(load_file_action)

        export_action = QtWidgets.QAction("Export", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_data)
        self.file_menu.addAction(export_action)
        self.file_menu.addSeparator()

        exit_action = QtWidgets.QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

    def create_main_frame(self):
        self.main_frame = QtWidgets.QWidget()

        self.load_file_button = QtWidgets.QPushButton("Load CSV", self)
        self.load_file_button.clicked.connect(self.load_file)

        self.plot_button = QtWidgets.QPushButton("Plot Data", self)
        self.plot_button.clicked.connect(self.plot_data)
        self.plot_button.setEnabled(False)

        self.export_button = QtWidgets.QPushButton("Export Data", self)
        self.export_button.clicked.connect(self.export_data)
        self.export_button.setEnabled(False)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.figure.tight_layout()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.load_file_button)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.canvas)

        self.main_frame.setLayout(layout)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QtWidgets.QLabel("Please load a CSV file")
        self.statusBar().addWidget(self.status_text, 1)

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv);;All Files (*)",
                                                   options=options)
        if file_name:
            self.csv_file = file_name
            self.df = pd.read_csv(self.csv_file)
            self.layer_name = QFileInfo(file_name).baseName()
            layer = processing.run("qgis:importvectorintolayer",
                                   {'INPUT': self.csv_file, 'LAYER NAME': self.layer_name, 'PROVIDER': 'delimited text'})
            self.status_text.setText(f"Loaded {self.layer_name}")
            self.plot_button.setEnabled(True)
            self.export_button.setEnabled(True)

            def plot_data(self):
                # Add code to plot data using matplotlib
                pass

            def export_data(self):
                options = QFileDialog.Options()
                options |= QFileDialog.ReadOnly
                file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                           "All Files (*);;KML Files (*.kml);; GPX Files (*.gpx);; "
                                                           "CSV Files (*.csv)",
                                                           options=options)
                if file_name:
                    if file_name.endswith('.kml'):
                        processing.run("qgis:convert format",
                                       {'INPUT': self.layer_name, 'OUTPUT': file_name, 'TARGET_CRS': 'EPSG:4326',
                                        'OUTPUT_FORMAT': 'KML'})
                    elif file_name.endswith('.gpx'):
                        processing.run("qgis:convert format",
                                       {'INPUT': self.layer_name, 'OUTPUT': file_name, 'TARGET_CRS': 'EPSG:4326',
                                        'OUTPUT_FORMAT': 'GPX'})
                    elif file_name.endswith('.csv'):
                        self.df.to_csv(file_name, index=False)
                    else:
                        print('Invalid file format')
                        if name == "main":
                            app = QtWidgets.QApplication(sys.argv)
                        main_window = QGISImporter()
                        main_window.show()
                        sys.exit(app.exec_())
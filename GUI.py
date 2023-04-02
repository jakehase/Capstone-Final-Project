import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMenu, QMenuBar, QAction, QToolBar, QDockWidget, QListWidget,
                             QTableWidget, QVBoxLayout, QWidget, QStatusBar)
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("QGIS Data Import and Visualization Tool")
        self.setGeometry(100, 100, 800, 600)

        self.init_menu_bar()
        self.init_tool_bar()
        self.init_dock_widgets()
        self.init_status_bar()
        self.show()

    def init_menu_bar(self):
        menu_bar = QMenuBar(self)

        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        view_menu = QMenu("View", self)
        help_menu = QMenu("Help", self)

        import_csv_action = QAction("Import CSV", self)
        import_shapefile_action = QAction("Import Shapefile", self)
        export_project_action = QAction("Export Project", self)
        exit_action = QAction("Exit", self)

        file_menu.addActions([import_csv_action, import_shapefile_action, export_project_action, exit_action])

        data_cleaning_action = QAction("Data Cleaning Options", self)
        data_manipulation_action = QAction("Data Manipulation Options", self)

        edit_menu.addActions([data_cleaning_action, data_manipulation_action])

        map_preview_action = QAction("Map Preview", self)
        layer_styles_action = QAction("Layer Styles", self)

        view_menu.addActions([map_preview_action, layer_styles_action])

        user_guide_action = QAction("User Guide", self)
        about_action = QAction("About", self)

        help_menu.addActions([user_guide_action, about_action])

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(view_menu)
        menu_bar.addMenu(help_menu)

        self.setMenuBar(menu_bar)

    def init_tool_bar(self):
        tool_bar = QToolBar(self)

        import_csv_action = QAction(QIcon("path/to/csv_icon.png"), "Import CSV", self)
        import_shapefile_action = QAction(QIcon("path/to/shapefile_icon.png"), "Import Shapefile", self)
        zoom_in_action = QAction(QIcon("path/to/zoom_in_icon.png"), "Zoom In", self)
        zoom_out_action = QAction(QIcon("path/to/zoom_out_icon.png"), "Zoom Out", self)
        pan_action = QAction(QIcon("path/to/pan_icon.png"), "Pan", self)
        full_extent_action = QAction(QIcon("path/to/full_extent_icon.png"), "Full Extent", self)

        tool_bar.addActions([import_csv_action, import_shapefile_action, zoom_in_action, zoom_out_action, pan_action, full_extent_action])

        self.addToolBar(tool_bar)

    def init_dock_widgets(self):
        layers_dock = QDockWidget("Layers", self)
        layers_list_widget = QListWidget()
        layers_dock.setWidget(layers_list_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, layers_dock)

        attributes_dock = QDockWidget("Attributes", self)
        attributes_table_widget = QTableWidget()
        attributes_dock.setWidget(attributes_table_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, attributes_dock)

    def init_status_bar(self):
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMenu, QMenuBar, QAction, QToolBar, QDockWidget, QListWidget,
                             QTableWidget, QVBoxLayout, QWidget, QStatusBar, QFileDialog)
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from column_organizer import organize_columns
import data_processing


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Initialize the table widget
        self.table = QTableWidget()

        # Create a QWidget as the central widget
        central_widget = QWidget(self)

        # Create a QVBoxLayout and add the table to it
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        # Set the QVBoxLayout as the layout for the central widget
        central_widget.setLayout(layout)

        # Set the central widget for the QMainWindow
        self.setCentralWidget(central_widget)

        self.setWindowTitle("QGIS Data Import and Visualization Tool")
        self.setGeometry(100, 100, 800, 600)

        self.init_menu_bar()
        self.init_tool_bar()
        self.init_dock_widgets()
        self.init_status_bar()
        self.show()

    def organize_columns_rows(self):
        # Assume self.table is a QTableWidget
        num_rows = self.table.rowCount()
        num_cols = self.table.columnCount()

        # Get the current order of the columns
        current_column_order = [self.table.horizontalHeaderItem(i).text() for i in range(num_cols)]

        # Get the current order of the rows
        current_row_order = [self.table.verticalHeaderItem(i).text() for i in range(num_rows)]

        # Show a dialog where the user can select the new order of the columns and rows
        dialog = ColumnRowOrganizerDialog(current_column_order, current_row_order, self)
        dialog.exec_()

        if dialog.result() == QDialog.Accepted:
            new_column_order = dialog.get_column_order()
            new_row_order = dialog.get_row_order()

            # Reorder the columns
            new_column_indices = [current_column_order.index(col) for col in new_column_order]
            self.table.setColumnOrder(new_column_indices)

            # Reorder the rows
            new_row_indices = [current_row_order.index(row) for row in new_row_order]
            self.table.setVerticalHeaderLabels(new_row_order)
            self.table.setRowCount(len(new_row_indices))
            for new_i, old_i in enumerate(new_row_indices):
                for j in range(num_cols):
                    item = self.table.takeItem(old_i, j)
                    self.table.setItem(new_i, j, item)

    def drop_missing_values(self):
        try:
            self.df_cleaned.dropna(inplace=True)
            self.update_table()
        except Exception as e:
            print(f"Exception occurred: {e}")

    def fill_missing_values(self):
        try:
            self.df_cleaned.fillna(0, inplace=True)  # Fill missing values with 0
            self.update_table()
        except Exception as e:
            print(f"Exception occurred: {e}")

    def update_table(self):
        self.table.setRowCount(self.df_cleaned.shape[0])
        self.table.setColumnCount(self.df_cleaned.shape[1])
        self.table.setHorizontalHeaderLabels(self.df_cleaned.columns)
        for i in range(self.df_cleaned.shape[0]):
            for j in range(self.df_cleaned.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(self.df_cleaned.iloc[i, j])))

    def import_csv(self):
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV Files (*.csv);;All Files (*)",
                                                       options=options)

            if file_name:
                df = data_processing.read_csv(file_name)
                self.df_cleaned = data_processing.clean_missing_values(df, method='drop')
                self.table.setRowCount(self.df_cleaned.shape[0])
                self.table.setColumnCount(self.df_cleaned.shape[1])
                self.table.setHorizontalHeaderLabels(self.df_cleaned.columns)
                print(f"Number of rows: {self.df_cleaned.shape[0]}")
                for i in range(self.df_cleaned.shape[0]):
                    for j in range(self.df_cleaned.shape[1]):
                        self.table.setItem(i, j, QTableWidgetItem(str(self.df_cleaned.iloc[i, j])))
                        # Sort columns by the specified order
                        column_order = ["Departure Date", "Supplier", "Lot", "Contract", "Net Weight",
                                        "Number of Sacks"]
                        self.sort_columns(column_order)
        except Exception as e:
            print(f"Exception occurred: {e}")

            # Perform additional cleaning and manipulation operations on the DataFrame here

    def sort_columns(self, column_order):
        try:
            # Reorder columns based on the specified column_order
            self.df_cleaned = self.df_cleaned[column_order]
            self.update_table()
        except Exception as e:
            print(f"Exception occurred: {e}")

    def import_shapefile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Shapefile", "", "Shapefile (*.shp);;All Files (*)", options=options)

        if file_name:
            gdf = data_processing.read_shapefile(file_name)
            # Perform cleaning and manipulation operations on the GeoDataFrame here

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

        import_csv_action.triggered.connect(self.import_csv)
        import_shapefile_action.triggered.connect(self.import_shapefile)

        file_menu.addActions([import_csv_action, import_shapefile_action, export_project_action, exit_action])

        # Create QMenu objects for each set of options
        data_cleaning_menu = QMenu("Data Cleaning Options", self)
        data_manipulation_menu = QMenu("Data Manipulation Options", self)

        # Create QAction objects for each option
        drop_missing_values_action = QAction("Drop Missing Values", self)
        fill_missing_values_action = QAction("Fill Missing Values", self)

        # Connect the actions to their respective methods
        drop_missing_values_action.triggered.connect(self.drop_missing_values)
        fill_missing_values_action.triggered.connect(self.fill_missing_values)

        # Add the actions to their respective menus
        data_cleaning_menu.addActions([drop_missing_values_action, fill_missing_values_action])

        # Create a QAction object for the column and row organizer
        organize_columns_rows_action = QAction("Organize Columns and Rows", self)
        organize_columns_rows_action.triggered.connect(self.organize_columns_rows)

        # Add the column and row organizer action to the Data Cleaning Options submenu
        data_cleaning_menu.addAction(organize_columns_rows_action)

        # Add the menus to the parent 'Edit' menu
        edit_menu.addMenu(data_cleaning_menu)
        edit_menu.addMenu(data_manipulation_menu)

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

        # Create QAction objects for each data cleaning option
        drop_missing_values_action = QAction("Drop Missing Values", self)
        fill_missing_values_action = QAction("Fill Missing Values", self)

        # Connect the actions to their respective methods
        drop_missing_values_action.triggered.connect(self.drop_missing_values)
        fill_missing_values_action.triggered.connect(self.fill_missing_values)

        # Add the data cleaning actions to a submenu
        data_cleaning_menu = QMenu("Data Cleaning Options", self)
        data_cleaning_menu.addActions([drop_missing_values_action, fill_missing_values_action])

        # Create a QAction object for the column and row organizer
        organize_columns_rows_action = QAction("Organize Columns and Rows", self)
        organize_columns_rows_action.triggered.connect(self.organize_columns_rows)

        # Add the column and row organizer action to the Data Cleaning Options submenu
        data_cleaning_menu.addAction(organize_columns_rows_action)

        # Add the Data Cleaning Options submenu to the Edit menu
        edit_menu = QMenu("Edit", self)
        edit_menu.addMenu(data_cleaning_menu)

    def open_user_guide(self):
        user_guide_url = QUrl.fromLocalFile("user_guide.pdf")
        QDesktopServices.openUrl(user_guide_url)

        def show_user_guide(self):
            # Open the user guide file and display it in a new window
            with open("user_guide.pdf", "r") as f:
                user_guide_text = f.read()
            user_guide_window = QWidget()
            user_guide_layout = QVBoxLayout()
            user_guide_label = QLabel(user_guide_text)
            user_guide_layout.addWidget(user_guide_label)
            user_guide_window.setLayout(user_guide_layout)
            user_guide_window.setWindowTitle("User Guide")
            user_guide_window.show()

        # In the init_menu_bar function:
        user_guide_action = QAction("User Guide", self)
        user_guide_action.triggered.connect(self.show_user_guide)
        help_menu.addActions([user_guide_action])
    def init_tool_bar(self):
        tool_bar = QToolBar(self)

        import_csv_action = QAction(QIcon("csv_icon.png"), "Import CSV", self)
        import_shapefile_action = QAction(QIcon("shapefile_icon.png"), "Import Shapefile", self)
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
        attributes_dock.setWidget(self.table)  # Use self.table as the widget for the dock
        self.addDockWidget(Qt.RightDockWidgetArea, attributes_dock)

    def init_status_bar(self):
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())



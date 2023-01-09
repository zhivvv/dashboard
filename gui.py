# base modules
import pandas as pd
import os
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

# My modules
import func
from base_ui import Ui_MainWindow
from mapping import mapping_process
from calculations import calculation_process
from extraction import extraction_for_gui


class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.events()
        self.table = None

    # Define events
    def events(self):
        self.ui.btn_1.clicked.connect(lambda: self.extraction())
        self.ui.btn_4.clicked.connect(lambda: mapping_process())
        self.ui.btn_3.clicked.connect(lambda: calculation_process())
        self.ui.btn_tool_1.clicked.connect(lambda: self.get_mapping_file())
        self.ui.btn_export.clicked.connect(lambda: self.save_table('/Users/ivanov.ev/Desktop/',
                                                                   'test'))

    def get_directory(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:',
                                                         os.path.expanduser("~")
                                                         )
        return dir

    def get_file_location(self):
        location = QtWidgets.QFileDialog.getOpenFileName(None, 'Select file:',
                                                         os.path.expanduser('~')
                                                         )
        return location

    def extraction(self):
        dir = self.get_directory()
        self.table = extraction_for_gui(dir)
        model = PandasModel(self.table)
        self.ui.table_1.setModel(model)

    def get_mapping_file(self):
        dir = self.get_file_location()
        mapping_file = pd.ExcelFile(dir).parse()

    def save_table(self, loc, file_name):
        func.safe_dataframes_to_excel([self.table], ['test'], loc, file_name)
        # self.ui.table_1    get table


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(
            self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None

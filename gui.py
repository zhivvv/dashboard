# base modules
from datetime import date

import pandas as pd
import os
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

# My modules
from base_ui import Ui_MainWindow
from extraction import extraction_for_gui
from mapping import get_mapping_table, apply_mapping_to_fem


# from calculations import calculation_process


class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.events()
        self.table = None
        self.msg = None
        self.path = None

    # Define events
    def events(self):

        # Extraction process

        # add data folder
        self.ui.btn_tool_choose_fem_folder.clicked.connect(
            lambda: self.get_item_path(object_to_write=self.ui.lineEdit_datafolder,
                                       item='folder'))
        # extract FEM
        self.ui.btn_extract_fem.clicked.connect(lambda: self.extraction(self.ui.lineEdit_datafolder.text()))

        # save extraction to excel
        self.ui.btn_save_extraction.clicked.connect(lambda: self.save_table(self.table,
                                                                            file_name='extraction'))

        # Mapping process

        # add mapping file
        self.ui.btn_tool_choose_mapping_file.clicked.connect(
            lambda: self.get_item_path(object_to_write=self.ui.lineEdit_mapping_file,
                                       item='file'))

        # add extraction file
        self.ui.btn_tool_choose_data_file.clicked.connect(
            lambda: self.get_item_path(object_to_write=self.ui.lineEdit_data_file,
                                       item='file'))

        # get mapping file
        self.ui.btn_get_mapping_file.clicked.connect(self.get_mapping_file)

        # save mapping file to excel
        self.ui.btn_save_mapping.clicked.connect(lambda: self.save_table(self.table,
                                                                         file_name='mapping'))

        # add data file

        # add data file
        # self.ui.btn_export.clicked.connect(lambda: self.save_table('/Users/ivanov.ev/Desktop/', 'test'))
        # self.ui.btn_3.clicked.connect(calculation_process)
        # add event

    def get_item_path(self, item='file', object_to_write=None):

        try:
            if item == 'file':
                path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')[0]
            elif item == 'folder':
                path = QtWidgets.QFileDialog.getExistingDirectory(None, f'Select a {item}:', os.path.expanduser("~"))
            else:
                raise NotADirectoryError

            if object_to_write is None:
                return path
            else:
                object_to_write.setText(path)
                return path
        except Exception as e:
            self.msg = CriticalMessage()
            self.msg.setInformativeText(str(e))

    def extraction(self, folder_path):
        df = extraction_for_gui(folder_path)
        self.set_table(df, self.ui.table_fem_data)
        self.table = df

    def set_table(self, table: pd.DataFrame, obj_name):

        try:
            model = PandasModel(table)
            obj_name.setModel(model)

        except Exception as e:
            self.msg = CriticalMessage()
            self.msg.setInformativeText(str(e))

    def get_mapping_file(self):
        mapping_file, df = map(pd.read_excel, [self.ui.lineEdit_mapping_file.text(),
                                               self.ui.lineEdit_data_file.text()])

        result = get_mapping_table(df, mapping_file)
        self.set_table(result, self.ui.table_fem_data)
        self.table = result


    def save_table(self, table_name: pd.DataFrame, file_name='untitled'):

        today_date = date.today().strftime("%d%m%Y")
        default_sheet_name = 'sheet_1'
        file_name = file_name + today_date

        #     Folder to save selection
        folder_to_save = self.get_item_path(item='folder')
        path_to_save = os.path.join(folder_to_save, f'{file_name}.xlsx')
        table_name.to_excel(excel_writer=path_to_save, sheet_name=default_sheet_name)
        Info(label=f'File been saved to {path_to_save} successfully')

        #     TODO Write function that checks existence of file in selected folder


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


class CriticalMessage(QtWidgets.QMessageBox):
    def __init__(self):
        super(CriticalMessage, self).__init__()
        self.setIcon(QtWidgets.QMessageBox.Critical)
        self.setText("Error")
        self.setInformativeText('More information')
        self.setWindowTitle("Error")


class Info(QtWidgets.QMessageBox):

    def __init__(self, label):
        super(Info, self).__init__()
        self.setWindowTitle("Information")
        self.setText(label)
        # self.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.setStandardButtons(self.Ok)
        # self.setIcon(self.Question)
        self.exec()

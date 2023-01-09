# import pyinputplus as pyip
from gui import GUI
import settings
import os
import sys
from PyQt5 import QtWidgets
from extraction import extraction_process, extraction_for_gui
from mapping import mapping_process
from reports import report_process
from calculations import calculation_process


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())


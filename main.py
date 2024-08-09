from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import os

includePath = os.path.abspath(os.getcwd() + '\\Include')
sys.path.append(includePath)

from database import Database

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Database()
    window.show()
    app.exec_()
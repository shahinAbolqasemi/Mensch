import sys
from PyQt5.QtWidgets import QApplication
from gui.game_board_gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

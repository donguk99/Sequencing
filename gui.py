import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QMainWindow, QAction
from PyQt5.QtCore import QCoreApplication

class Exam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar()
        self.statusBar().showMessage('hi')

        menu = self.menuBar()               #메뉴바 생성
        menu_file = menu.addMenu("File")    #그룹 생성
        menu_edit = menu.addMenu("Edit")    #그룹 생성

        file_exit = QAction("Exit", self)   #메뉴 객체 생성
        file_exit.setShortcut('Ctrl+Q')
        file_exit.setStatusTip("누르면 빠이")

        menu_file.addAction(file_exit)
        self.resize(450, 400)
        self.show()

    # 종료하는 이벤트
    def closeEvent(self, QCloseEvnet):
        ans = QMessageBox.question(self, "종료 확인", "종료하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            QCloseEvnet.accept()
        else:
            QCloseEvnet.ignore()


app = QApplication(sys.argv)
w = Exam()
sys.exit(app.exec_()) # 프로그램을 깨끗하게 종료한다, app.exec: 이벤트 처리를 위한 루프 실행(메인 루프)
# 메인루프가 끝나면 exit 실행된다.
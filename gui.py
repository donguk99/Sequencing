import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("test_pyqt.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #버튼에 기능을 연결하는 코드
        self.start_btn.clicked.connect(self.start_btnFunction)

        #GroupBox안에 있는 RadioButton들을 연결
        self.groupBox_m_1.clicked.connect(self.groupBox_sqFunction)
        self.groupBox_m_2.clicked.connect(self.groupBox_sqFunction)
        self.groupBox_m_3.clicked.connect(self.groupBox_sqFunction)
        self.groupBox_m_4.clicked.connect(self.groupBox_sqFunction)
        self.groupBox_m_5.clicked.connect(self.groupBox_sqFunction)

    def start_btnFunction(self):
        print("start")

    # GroupBox안에 선택하면 어떻게 되는지
    def groupBox_sqFunction(self):
        if self.groupBox_m_1.isChecked() : print("1")
        elif self.groupBox_m_2.isChecked() : print("2")
        elif self.groupBox_m_3.isChecked() : print("3")
        elif self.groupBox_m_4.isChecked() : print("4")
        elif self.groupBox_m_5.isChecked() : print("5")




if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
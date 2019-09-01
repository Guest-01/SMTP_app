import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText

form_class = uic.loadUiType("SMTP_pyqt.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.send_button)
    
    def send_button(self):
        self.pushButton_2.setEnabled(False)
        data = self.organize_data()
        try:
            self.send_mail(data)
            self.statusbar.showMessage(f"Success, {self.lineEdit_7.text()}")
        except Exception as e:
            print(e)
            self.statusbar.showMessage(str(e))
        finally:
            self.pushButton_2.setEnabled(True)

        return
    
    def organize_data(self):
        data = {
            'host': self.lineEdit.text(),
            'port': int(self.lineEdit_2.text()),
            'ssl': self.checkBox.isChecked(),
            'id': self.lineEdit_3.text(),
            'pw': self.lineEdit_4.text(),
            'return_path': self.lineEdit_5.text() if self.checkBox_2.isChecked() else self.lineEdit_6.text(),
            'from': self.lineEdit_6.text(),
            'to': self.lineEdit_7.text(),
            'subject': self.lineEdit_8.text(),
            'content': self.textEdit.toPlainText()
        }

        return data
    
    def send_mail(self, mydict):
        if mydict['ssl']:
            print('ssl on')
            server = SMTP_SSL(mydict['host'], mydict['port'])  # Port -> int
        else:
            print('ssl off')
            server = SMTP(mydict['host'], mydict['port'])
    
        server.login(mydict['id'], mydict['pw'])  # Strings

        msg = MIMEText(mydict['content'], _charset='euc-kr')
        msg['Subject'] = mydict['subject']
        msg['From'] = mydict['from']
        msg['To'] = mydict['to']

        server.sendmail(mydict['from'], mydict['to'], msg.as_string())
        server.quit()
    
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
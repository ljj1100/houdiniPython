import sys, os
import schedule
from datetime import datetime, time
from time import sleep
from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QCompleter, QPushButton, QApplication, QGridLayout, QBoxLayout, QSpacerItem,QLabel
from PyQt5.QtCore import QStringListModel


class Alarm(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        parents_path = os.getcwd()
        self.create_txt = parents_path + "/myInfo.txt"
        self.initWidget()

    def initWidget(self):
        self.setWindowTitle("Locman Login Test")
        self.main_box = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        self.loginParents()

    def loginParents(self):
        gb1 = QGroupBox("Login")
        self.main_box.addWidget(gb1)
        # base layout
        base_box = QBoxLayout(QBoxLayout.TopToBottom, self)
        button_box = QBoxLayout(QBoxLayout.LeftToRight, self)

        line_edit_id       = self.loginID()
        line_edit_password = self.loginPassword()
        line_edit_id.textChanged.connect(self.senderTextID)
        line_edit_password.textChanged.connect(self.senderTextPassword)
        #self.password_text = line_edit_password.setEchoMode(QLineEdit.Password)

        save_button        = self.saveButton()
        cancel_button      = self.cancelButton()
        save_button.pressed.connect(self.saveFile)

        layout = QGridLayout()
        layout.addItem(QSpacerItem(30, 0))
        layout.addWidget(QLabel("ID             : "), 1, 0)
        layout.addWidget(line_edit_id, 1, 1)
        layout.addWidget(QLabel("Password  : "),2 ,0)
        layout.addWidget(line_edit_password, 2, 1)
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        base_box.addLayout(layout)
        base_box.addLayout(button_box)

        gb1.setLayout(base_box)

    def loginID(self):
        create_txt = self.create_txt
        read_file = open(create_txt, "r")
        list_info = read_file.read().split()

        self.id_export = [name for i, name in enumerate(list_info) if i%2==0]
        #password_export = [name for i, name in enumerate(list_info) if i % 2 != 0]
        try:
            le_1 = QLineEdit(self.id_export[0])
        except:
            le_1 = QLineEdit("")
        model = QStringListModel()
        model.setStringList(self.id_export)

        completer = QCompleter()
        completer.setModel(model)

        le_1.setCompleter(completer)

        return le_1

    def loginPassword(self):
        create_txt = self.create_txt
        read_file = open(create_txt, "r")
        list_info = read_file.read().split()

        #id_export = [name for i, name in enumerate(list_info) if i%2==0]
        self.password_export = [name for i, name in enumerate(list_info) if i % 2 != 0]

        try:
            le_1 = QLineEdit(self.password_export[0])
        except:
            le_1 = QLineEdit("")
        model = QStringListModel()
        model.setStringList(self.password_export)

        completer = QCompleter()
        completer.setModel(model)

        le_1.setCompleter(completer)

        return le_1

    def saveButton(self):
        pb_1 = QPushButton("Ok")
        return pb_1

    def cancelButton(self):
        pb_1 = QPushButton("Cancel")
        pb_1.pressed.connect(self.close)
        return pb_1

    def senderTextID(self):
        sender_ = self.sender().text()
        self.final_ID = sender_

    def senderTextPassword(self):
        sender_ = self.sender().text()
        self.final_Password = sender_

    def saveFile(self):
        create_txt = self.create_txt
        read_file = open(create_txt, "r")
        list_info = read_file.read().split()

        #print("save append", self.list_infomation)
        try:
            id_ = self.final_ID
            password_ = self.final_Password
            list_info = []
            list_info.append(id_)
            list_info.append(password_)

            with open(create_txt, "w") as file:
                 file.write("\n".join(list_info))
        except:
            pass
        try:
            from selenium import webdriver
            from time import sleep

            self.final_ID

            driver = webdriver.Chrome("./chromedriver")
            driver.set_window_size(1920, 1080)
            driver.implicitly_wait(2)
            driver.get('http://locman.locus.com')

            sleep(0.5)
            driver.find_element_by_name("userid").send_keys(self.final_ID)
            sleep(0.5)
            driver.find_element_by_name("password").send_keys(self.final_Password)
            sleep(0.5)
            driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/input").click()
            sleep(3)
            driver.find_element_by_id("small-pencil").click()
            sleep(4)
            driver.find_element_by_id("recent_toggle_btn").click()
            driver.find_element_by_id("start_time_value").send_keys("10")
            driver.find_element_by_id("end_time_value").send_keys("1230")

        except:
            from selenium import webdriver
            from time import sleep

            driver = webdriver.Chrome("./chromedriver")
            driver.set_window_size(1920, 1080)
            driver.implicitly_wait(2)
            driver.get('http://locman.locus.com')

            sleep(0.5)
            driver.find_element_by_name("userid").send_keys(self.id_export[0])
            sleep(0.5)
            driver.find_element_by_name("password").send_keys(self.password_export[0])
            sleep(0.5)
            driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/input").click()
            sleep(3)
            driver.find_element_by_id("small-pencil").click()
            sleep(4)
            driver.find_element_by_id("recent_toggle_btn").click()
            driver.find_element_by_id("start_time_value").send_keys("10")
            driver.find_element_by_id("end_time_value").send_keys("1230")


app = QApplication(sys.argv)
main = Alarm()
main.show()
sys.exit(app.exec_())


#
# def job():
#     now_time = datetime.now().strftime('%H:%M:%S')
#     print (now_time)
#     if now_time == '18:35:00':
#         app = QApplication(sys.argv)
#         main = Alarm()
#         main.show()
#         sys.exit(app.exec_())
#     else:
#         print("yet")
#
# schedule.every(1).second.do(job)
#
# while 1:
#     schedule.run_pending()
#     sleep(1)
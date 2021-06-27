import sys
import os
import hashlib
import time
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from set_hand_hist import get_hand_hist
from recognize_gesture import run_recognize_gesture
from recognize_number import  run_recognize_number
from create_gestures import  init_create_folder_database, store_in_db, store_in_db_2, store_images
from flip_images import flip_images
from load_images import run_load_images
from cnn_keras import train
from keras import backend as K
from display_all_gestures import run_display_mod
from PyQt5 import uic
Ui_MainWindow, baseClass = uic.loadUiType('Main_Interface.ui')

class MainWindow(baseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #code starts here

        #initiate main_interface
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #default page
        self.ui.stackedWidget.setCurrentIndex(0)

        #EventFilter
        self.ui.description_frame.setVisible(False)
        self.ui.first_time_button.installEventFilter(self)
        self.ui.description_frame_2.setVisible(False)
        self.ui.translate_button.installEventFilter(self)
        self.ui.description_frame_3.setVisible(False)
        self.ui.admin_button.installEventFilter(self)

        #set button sytlesheet (image)
        self.ui.exit_button.setStyleSheet("QPushButton {border-image : url(Img/Exit.png);}")
        self.ui.return_button_page1.setStyleSheet("QPushButton {border-image : url(Img/return_button.png);}")
        self.ui.return_button_page2.setStyleSheet("QPushButton {border-image : url(Img/return_button.png);}")
        self.ui.return_button_page3.setStyleSheet("QPushButton {border-image : url(Img/return_button.png);}")
        self.ui.return_button_page5.setStyleSheet("QPushButton {border-image : url(Img/return_button.png);}")
        self.ui.return_button_page6.setStyleSheet("QPushButton {border-image : url(Img/return_button.png);}")
        self.ui.return_button_page7.setStyleSheet("QPushButton {border-image : url(Img/return_button.png);}")
        self.ui.return_button_page8.setStyleSheet("QPushButton {border-image : url(Img/return_button.png);}")
        self.ui.return_button_page4.setStyleSheet("QPushButton {border-image : url(Img/home_icon.png);}")

        #file_menu
        self.ui.action_Main_Menu.triggered.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.action_Exit.triggered.connect(lambda: self.ui.stackedWidget.setCurrentIndex(9))
        self.ui.action_Info.triggered.connect(self.infoApp)
        self.ui.action_User_Manual.triggered.connect(self.manualApp)

        #signal and slots
        #back_button
        self.ui.return_button_page1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.return_button_page2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.return_button_page3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.return_button_page4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.return_button_page5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.return_button_page6.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.return_button_page7.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.return_button_page8.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))

        #main_menu
        self.ui.first_time_button.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.admin_button.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.translate_button.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.exit_button.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(9))

        #Admin_control
        self.ui.start_page3_button.clicked.connect(self.isAdmin)
        self.ui.icon_button_1.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(5))
        self.ui.icon_button_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(6))
        self.ui.icon_button_3.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(7))
        self.ui.icon_button_4.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(8))

        #exit
        self.ui.yes_button.clicked.connect(self.exit)
        self.ui.no_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

        #python file linking
        self.ui.start_page1_button.clicked.connect(self.set_hand)
        self.ui.start_page2_button.clicked.connect(self.run_page2)
        self.ui.start_page2_button_2.clicked.connect(self.run_page2_2)
        self.ui.start_page6_button.clicked.connect(self.run_page6)
        self.ui.Done_Page7.setVisible(False)
        self.ui.start_page7_button.clicked.connect(self.run_page7)
        self.ui.start_page7_button_2.clicked.connect(self.run_page7_2)
        self.ui.Done_Page8.setVisible(False)
        self.ui.start_page8_button.clicked.connect(self.run_page8)
        self.ui.icon_button_5.clicked.connect(self.run_display)

        #ComboBox
        self.ui.language_box.activated[str].connect(self.handleItemPressed)
        #code ends here
        self.show()

    #slots
    def exit(self):
        sys.exit()

    #Define eventFilter():
    def eventFilter(self, o, e):
        if self.ui.first_time_button is o:
            if e.type() == qtc.QEvent.Type.Enter:
                self.ui.description_frame.setVisible(True)
            if e.type() == qtc.QEvent.Type.Leave:
                self.ui.description_frame.setVisible(False)
        elif self.ui.translate_button is o:
            if e.type() == qtc.QEvent.Type.Enter:
                self.ui.description_frame_2.setVisible(True)
            if e.type() == qtc.QEvent.Type.Leave:
                self.ui.description_frame_2.setVisible(False)
        elif self.ui.admin_button is o:
            if e.type() == qtc.QEvent.Type.Enter:
                self.ui.description_frame_3.setVisible(True)
            if e.type() == qtc.QEvent.Type.Leave:
                self.ui.description_frame_3.setVisible(False)

        return super(MainWindow, self).eventFilter(o, e)

    def handleItemPressed(self):
        item = self.ui.language_box.currentIndex()

        if item == 0: #English
            self.ui.Title.setText("BIM Sign Language \nTranslator")
            self.ui.first_time_button.setText(' First Time /\n New Environment')
            self.ui.translate_button.setText(' Translation Module')
            self.ui.admin_button.setText(' Admin Control')
            self.ui.description_label.setText('First Time Using? Set up your setting!')
            self.ui.description_label_3.setText('Start Sign Language Translating!')
            self.ui.description_label_4.setText('Admin access to the internal settings.')
            self.ui.welcome_text.setText('Hello')
            #exit interface
            self.ui.Title_Page9.setText('Are you sure you\nwant to exit?')
            self.ui.yes_button.setText('YES')
            self.ui.no_button.setText('NO')

        elif item == 1: #Bahasa Melayu
            self.ui.Title.setText("Penerjemah Bahasa\nIsyarat Malaysia")
            self.ui.first_time_button.setText(' Penggunaan Kali\n Pertama / Tempat Baru')
            self.ui.translate_button.setText(' Module Terjemahan')
            self.ui.admin_button.setText(' Pentadbir Admin')
            self.ui.description_label.setText('Kali Pertama Menggunakan? Sediakan tetapan anda')
            self.ui.description_label_3.setText('Mulakan Penterjemahan Bahasa Isyarat')
            self.ui.description_label_4.setText('Akses pentadbir ke tetapan system.')
            self.ui.welcome_text.setText('Hello')
            #exit interface
            self.ui.Title_Page9.setText('Adakah anda pasti\n mahu keluar?')
            self.ui.yes_button.setText('IYA')
            self.ui.no_button.setText('TIDAK')

        elif item == 2: # Chinese
            self.ui.Title.setText("BIM\n手语翻译器")
            self.ui.first_time_button.setText(' 首次使用/\n 新环境')
            self.ui.translate_button.setText(' 翻译系统')
            self.ui.admin_button.setText(' 管理控制')
            self.ui.description_label.setText('第一次使用？快速设置您的设置！')
            self.ui.description_label_3.setText('开始手语翻译！')
            self.ui.description_label_4.setText('内部设置系统的管理')
            self.ui.welcome_text.setText('你好')
            #exit interface
            self.ui.Title_Page9.setText('您确定要退出吗？')
            self.ui.yes_button.setText('是')
            self.ui.no_button.setText('不')

        elif item == 3: # Tamil
            self.ui.Title.setText("கையொப்பம்\nமொழிபெயர்ப்பாளர்")
            self.ui.first_time_button.setText(' முதல் முறை\n / புதிய சூழல்')
            self.ui.translate_button.setText(' மொழிபெயர்ப்பு\n அமைப்பு')
            self.ui.admin_button.setText(' நிர்வாக\n கட்டுப்பாடு')
            self.ui.description_label.setText('முதல் முறையாக பயன்படுத்துகிறீர்களா? உங்கள் அமைப்பை அமைக்கவும்!')
            self.ui.description_label_3.setText('சைகை மொழி மொழிபெயர்ப்பைத் தொடங்குங்கள்')
            self.ui.description_label_4.setText('உள் அமைப்புகளுக்கான நிர்வாக அணுகல்.')
            self.ui.welcome_text.setText('வணக்கம்')
            #exit interface
            self.ui.Title_Page9.setText('நிச்சயமாக நீங்கள்\nவெளியேற வேண்டுமா?')
            self.ui.yes_button.setText('ஆம்')
            self.ui.no_button.setText('இல்லை')



    def isAdmin(self):
        string = self.ui.password_page3.text()
        encoded = string.encode()
        result = hashlib.sha256(encoded)

        if result.hexdigest() == 'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae':
            qtw.QMessageBox.information(self, 'Login Success', 'You are now login.')
            self.ui.password_page3.clear()
            self.ui.stackedWidget.setCurrentIndex(4)
        else:
            qtw.QMessageBox.warning(self, 'Login Fail', 'Wrong Password. Please Try Again.')

    def infoApp(self):
        infoMsg = qtw.QMessageBox()
        infoMsg.setWindowTitle("Information about this application")
        iconImg = qtg.QPixmap("./Img/UTHM.gif")
        iconImg = iconImg.scaledToWidth(64)
        infoMsg.setIconPixmap(iconImg)
        infoMsg.setText("This application is made by Herrick")
        infoMsg.setInformativeText("For more information, contact FSKTM @ UTHM")
        infoMsg.setDetailedText("Malaysian Sign Language (also known as Bahasa Isyarat Malaysia in Malay language, or BIM) is a Malaysian government official recognition of sign language which are used to properly communicate with the deaf community throughout the whole country, usually in a form of official announcements and broadcasts.\n\nThe background of this project is to further provide a product-based services to assist the deaf community and provide a gateway or a bridge to translate sign language (BIM) and deliver messages to the non-proficient BIM users.\n\nAlthough there is some technology advancement that covers translating sign language, but most of them are based on ASL (American Sign Language) and English language.\n\nThis creates conflicts when using of previous established technology as BIM are a lot different than ASL in terms of sign language and the use of it.\n\nIn order to resolve the problem of lack of existing BIM translation machine, a system that can translate BIM sign language for translating BIM sign language with image processing approach has been designed. The solution proposed is to provide a deep learning algorithm using TensorFlow neural structure network that provide multiple language (English, Malay and possibly other) that are translated from BIM sign languages.")
        infoMsg.exec_()

    def manualApp(self):
        psfPath = 'user_manual.pdf'
        os.system(psfPath)

    #python function
    def set_hand(self):
        self.ui.start_page1_button.setEnabled(False)
        get_hand_hist()
        #os.system('set_hand_hist.py')
        self.ui.start_page1_button.setEnabled(True)

    def run_page2(self):
        self.ui.start_page2_button.setEnabled(False)
        self.ui.start_page2_button_2.setEnabled(False)
        run_recognize_gesture()
        self.ui.start_page2_button.setEnabled(True)
        self.ui.start_page2_button_2.setEnabled(True)

    def run_page2_2(self):
        self.ui.start_page2_button.setEnabled(False)
        self.ui.start_page2_button_2.setEnabled(False)
        run_recognize_number()
        self.ui.start_page2_button.setEnabled(True)
        self.ui.start_page2_button_2.setEnabled(True)

    def run_page6(self):
        self.ui.start_page6_button.setEnabled(False)
        init_create_folder_database()
        page6_id = self.ui.id_page7.text()
        page6_name = self.ui.name_page7.text()
        error_page6_x = store_in_db(page6_id, page6_name)
        if error_page6_x:
            error_msg = qtw.QMessageBox()
            error_msg.setWindowTitle("Warning")
            error_msg.setIcon(qtw.QMessageBox.Critical)
            error_msg.setText("Duplicate found. Are you sure you want to overwrite it?")
            error_msg.setStandardButtons(qtw.QMessageBox.Cancel | qtw.QMessageBox.Ok)
            error_msg.buttonClicked.connect(self.page6_popup)
            error_msg.exec_()
        self.ui.start_page6_button.setEnabled(True)

    def page6_popup(self, i):

        if i.text() == 'OK':
            page6_id = self.ui.id_page7.text()
            page6_name = self.ui.name_page7.text()
            store_in_db_2(page6_id, page6_name)
            store_images(page6_id)

    def run_page7(self):
        self.ui.start_page7_button.setEnabled(False)
        self.ui.start_page7_button_2.setEnabled(False)
        self.ui.Done_Page7.setVisible(False)
        self.update_page7(0)
        self.page7_thread = qtc.QThread()
        self.page7_worker = page7_worker()
        self.page7_worker.moveToThread(self.page7_thread)

        self.page7_thread.started.connect(self.page7_worker.run)
        self.page7_worker.finished.connect(self.page7_thread.quit)
        self.page7_worker.finished.connect(self.page7_worker.deleteLater)
        self.page7_thread.finished.connect(self.page7_thread.deleteLater)
        self.page7_worker.progress.connect(self.update_page7)

        self.page7_thread.start()

    def update_page7(self, progress):
        self.ui.progressBar_Page7.setValue(progress)
        self.ui.start_page7_button.setEnabled(progress == 100)
        self.ui.start_page7_button_2.setEnabled(progress == 100)
        self.ui.Done_Page7.setVisible(progress == 100)
        if progress == 100:
            msg = qtw.QMessageBox()
            msg.setWindowTitle("Success")
            msg.setIcon(qtw.QMessageBox.Information)
            msg.setText("Image Flip Successfully!")
            msg.exec_()

    def run_page7_2(self):
        self.ui.start_page7_button.setEnabled(False)
        self.ui.start_page7_button_2.setEnabled(False)
        self.ui.Done_Page7.setVisible(False)
        self.update_page7(0)
        self.page7_thread = qtc.QThread()
        self.page7_worker = page7_worker_2()
        self.page7_worker.moveToThread(self.page7_thread)

        self.page7_thread.started.connect(self.page7_worker.run)
        self.page7_worker.finished.connect(self.page7_thread.quit)
        self.page7_worker.finished.connect(self.page7_worker.deleteLater)
        self.page7_thread.finished.connect(self.page7_thread.deleteLater)
        self.page7_worker.progress.connect(self.update_page7_2)

        self.page7_thread.start()

    def update_page7_2(self, progress):
        self.ui.progressBar_Page7.setValue(progress)
        self.ui.start_page7_button.setEnabled(progress == 100)
        self.ui.start_page7_button_2.setEnabled(progress == 100)
        self.ui.Done_Page7.setVisible(progress == 100)
        if progress == 100:
            msg = qtw.QMessageBox()
            msg.setWindowTitle("Success")
            msg.setIcon(qtw.QMessageBox.Information)
            msg.setText("Model is created successfully!")
            msg.exec_()

    def run_page8(self):
        self.ui.start_page8_button.setEnabled(False)
        self.ui.Done_Page8.setVisible(False)
        self.update_page8(0)
        self.page8_thread = qtc.QThread()
        self.page8_worker = page8_worker(self.ui.spinBox_Page8.value())
        self.page8_worker.moveToThread(self.page8_thread)

        self.page8_thread.started.connect(self.page8_worker.run)
        self.page8_worker.finished.connect(self.page8_thread.quit)
        self.page8_worker.finished.connect(self.page8_worker.deleteLater)
        self.page8_thread.finished.connect(self.page8_thread.deleteLater)
        self.page8_worker.progress.connect(self.update_page8)

        self.page8_thread.start()

    def update_page8(self, progress):
        self.ui.progressBar_Page8.setValue(progress)
        self.ui.start_page8_button.setEnabled(progress == 100)
        self.ui.Done_Page8.setVisible(progress == 100)
        if progress == 100:
            msg = qtw.QMessageBox()
            msg.setWindowTitle("Success")
            msg.setIcon(qtw.QMessageBox.Information)
            msg.setText("Training Machine Learning Module is success!")
            msg.exec_()

    def run_display(self):
        run_display_mod()


    # delete soon
    def test(self):
        qtw.QMessageBox.information(self, 'Success', 'You are great!')
    def test2(self):
        error_msg = qtw.QMessageBox()
        error_msg.setWindowTitle("Warning")
        error_msg.setIcon(qtw.QMessageBox.Critical)
        error_msg.setText("Duplicate found. Are you sure you want to overwrite it?")
        error_msg.setStandardButtons(qtw.QMessageBox.Cancel | qtw.QMessageBox.Ok)
        error_msg.buttonClicked.connect(self.page6_popup)
        error_msg.exec_()

class page7_worker(qtc.QObject):
    finished = qtc.pyqtSignal()
    progress = qtc.pyqtSignal(int)

    def run(self):
        flip_images(self.update_progress)
        self.finished.emit()

    def update_progress(self, percent):
            self.progress.emit(percent)

class page7_worker_2(qtc.QObject):
    finished = qtc.pyqtSignal()
    progress = qtc.pyqtSignal(int)

    def run(self):
        run_load_images(self.update_progress)
        self.finished.emit()

    def update_progress(self, percent):
            self.progress.emit(percent)

class page8_worker(qtc.QObject):
    finished = qtc.pyqtSignal()
    progress = qtc.pyqtSignal(int)

    def __init__(self, epochs):
        super(page8_worker, self).__init__()
        self.epochs = epochs

    def run(self):
        train(self.update_progress, self.epochs)
        K.clear_session()
        self.finished.emit()

    def update_progress(self, e, epochs):
        percent = (e + 1) / epochs * 100
        self.progress.emit(percent)



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    w = MainWindow(windowTitle="hello world")
    w.show()

    sys.exit(app.exec_())
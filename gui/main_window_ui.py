# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(779, 232)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.lbl_finished_objects = QLabel(self.centralwidget)
        self.lbl_finished_objects.setObjectName(u"lbl_finished_objects")

        self.gridLayout.addWidget(self.lbl_finished_objects, 1, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.lbl_finished_cases = QLabel(self.centralwidget)
        self.lbl_finished_cases.setObjectName(u"lbl_finished_cases")

        self.gridLayout.addWidget(self.lbl_finished_cases, 2, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.lbl_time = QLabel(self.centralwidget)
        self.lbl_time.setObjectName(u"lbl_time")

        self.gridLayout.addWidget(self.lbl_time, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_start = QPushButton(self.centralwidget)
        self.btn_start.setObjectName(u"btn_start")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start.sizePolicy().hasHeightForWidth())
        self.btn_start.setSizePolicy(sizePolicy)
        self.btn_start.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_2.addWidget(self.btn_start)

        self.btn_stop = QPushButton(self.centralwidget)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setEnabled(False)
        sizePolicy.setHeightForWidth(self.btn_stop.sizePolicy().hasHeightForWidth())
        self.btn_stop.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.btn_stop)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 779, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pipeline Simulator", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">Objetos finalizados:</span></p></body></html>", None))
        self.lbl_finished_objects.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt; color:#ff0000;\">0</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt;\">Pericias finalizadas:</span></p></body></html>", None))
        self.lbl_finished_cases.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt; color:#ff0000;\">0</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">Tempo:</span></p></body></html>", None))
        self.lbl_time.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt; color:#ff0000;\">0</span></p></body></html>", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"Iniciar", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"Parar", None))
    # retranslateUi


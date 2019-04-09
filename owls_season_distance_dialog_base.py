# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'owls_season_distance_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_seasonDistanceDialogBase(object):
    def setupUi(self, seasonDistanceDialogBase):
        seasonDistanceDialogBase.setObjectName("seasonDistanceDialogBase")
        seasonDistanceDialogBase.resize(281, 166)
        self.button_box = QtWidgets.QDialogButtonBox(seasonDistanceDialogBase)
        self.button_box.setGeometry(QtCore.QRect(-120, 120, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.label = QtWidgets.QLabel(seasonDistanceDialogBase)
        self.label.setGeometry(QtCore.QRect(90, 20, 111, 31))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(seasonDistanceDialogBase)
        self.comboBox.setGeometry(QtCore.QRect(110, 70, 69, 22))
        self.comboBox.setObjectName("comboBox")

        self.retranslateUi(seasonDistanceDialogBase)
        self.button_box.accepted.connect(seasonDistanceDialogBase.accept)
        self.button_box.rejected.connect(seasonDistanceDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(seasonDistanceDialogBase)

    def retranslateUi(self, seasonDistanceDialogBase):
        _translate = QtCore.QCoreApplication.translate
        seasonDistanceDialogBase.setWindowTitle(_translate("seasonDistanceDialogBase", "Owls Season Distance"))
        self.label.setText(_translate("seasonDistanceDialogBase", "Browse the file input"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PredictBinaryForSingleimage.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_predict_binary_single(object):
    def setupUi(self, Dialog_predict_binary_single):
        Dialog_predict_binary_single.setObjectName("Dialog_predict_binary_single")
        Dialog_predict_binary_single.resize(418, 228)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_predict_binary_single)
        self.buttonBox.setGeometry(QtCore.QRect(200, 190, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(Dialog_predict_binary_single)
        self.widget.setGeometry(QtCore.QRect(10, 10, 401, 171))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setMinimumSize(QtCore.QSize(55, 23))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.lineEdit_image = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_image.setMinimumSize(QtCore.QSize(201, 23))
        self.lineEdit_image.setObjectName("lineEdit_image")
        self.horizontalLayout_8.addWidget(self.lineEdit_image)
        self.pushButton_image = QtWidgets.QPushButton(self.widget)
        self.pushButton_image.setMinimumSize(QtCore.QSize(0, 23))
        self.pushButton_image.setObjectName("pushButton_image")
        self.horizontalLayout_8.addWidget(self.pushButton_image)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.spinBox_bands = QtWidgets.QSpinBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_bands.sizePolicy().hasHeightForWidth())
        self.spinBox_bands.setSizePolicy(sizePolicy)
        self.spinBox_bands.setMinimumSize(QtCore.QSize(47, 22))
        self.spinBox_bands.setMinimum(1)
        self.spinBox_bands.setMaximum(1000)
        self.spinBox_bands.setProperty("value", 3)
        self.spinBox_bands.setObjectName("spinBox_bands")
        self.horizontalLayout_4.addWidget(self.spinBox_bands)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        self.comboBox_dtype = QtWidgets.QComboBox(self.widget)
        self.comboBox_dtype.setObjectName("comboBox_dtype")
        self.comboBox_dtype.addItem("")
        self.comboBox_dtype.addItem("")
        self.comboBox_dtype.addItem("")
        self.comboBox_dtype.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_dtype)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setMinimumSize(QtCore.QSize(33, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.spinBox_windsize = QtWidgets.QSpinBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(23)
        sizePolicy.setHeightForWidth(self.spinBox_windsize.sizePolicy().hasHeightForWidth())
        self.spinBox_windsize.setSizePolicy(sizePolicy)
        self.spinBox_windsize.setMinimumSize(QtCore.QSize(50, 0))
        self.spinBox_windsize.setMaximumSize(QtCore.QSize(50, 23))
        self.spinBox_windsize.setMaximum(1000)
        self.spinBox_windsize.setSingleStep(2)
        self.spinBox_windsize.setProperty("value", 256)
        self.spinBox_windsize.setObjectName("spinBox_windsize")
        self.horizontalLayout_4.addWidget(self.spinBox_windsize)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setMinimumSize(QtCore.QSize(55, 23))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.lineEdit_model = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_model.setMinimumSize(QtCore.QSize(201, 23))
        self.lineEdit_model.setObjectName("lineEdit_model")
        self.horizontalLayout_7.addWidget(self.lineEdit_model)
        self.pushButton_model = QtWidgets.QPushButton(self.widget)
        self.pushButton_model.setMinimumSize(QtCore.QSize(0, 23))
        self.pushButton_model.setObjectName("pushButton_model")
        self.horizontalLayout_7.addWidget(self.pushButton_model)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout.addWidget(self.label_10)
        self.comboBox_gupid = QtWidgets.QComboBox(self.widget)
        self.comboBox_gupid.setMinimumSize(QtCore.QSize(0, 22))
        self.comboBox_gupid.setObjectName("comboBox_gupid")
        self.comboBox_gupid.addItem("")
        self.comboBox_gupid.addItem("")
        self.comboBox_gupid.addItem("")
        self.comboBox_gupid.addItem("")
        self.comboBox_gupid.addItem("")
        self.comboBox_gupid.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_gupid)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout.addWidget(self.label_11)
        self.comboBox_strategy = QtWidgets.QComboBox(self.widget)
        self.comboBox_strategy.setMinimumSize(QtCore.QSize(0, 22))
        self.comboBox_strategy.setObjectName("comboBox_strategy")
        self.comboBox_strategy.addItem("")
        self.comboBox_strategy.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_strategy)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setMinimumSize(QtCore.QSize(55, 23))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_9.addWidget(self.label_7)
        self.lineEdit_mask = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_mask.setMinimumSize(QtCore.QSize(201, 23))
        self.lineEdit_mask.setObjectName("lineEdit_mask")
        self.horizontalLayout_9.addWidget(self.lineEdit_mask)
        self.pushButton_mask = QtWidgets.QPushButton(self.widget)
        self.pushButton_mask.setMinimumSize(QtCore.QSize(0, 23))
        self.pushButton_mask.setObjectName("pushButton_mask")
        self.horizontalLayout_9.addWidget(self.pushButton_mask)
        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.retranslateUi(Dialog_predict_binary_single)
        self.buttonBox.rejected.connect(Dialog_predict_binary_single.reject)
        self.pushButton_image.clicked.connect(Dialog_predict_binary_single.slot_select_img_file)
        self.pushButton_model.clicked.connect(Dialog_predict_binary_single.slot_select_model_file)
        self.pushButton_mask.clicked.connect(Dialog_predict_binary_single.slot_save_mask_path)
        self.buttonBox.accepted.connect(Dialog_predict_binary_single.slot_ok)
        QtCore.QMetaObject.connectSlotsByName(Dialog_predict_binary_single)

    def retranslateUi(self, Dialog_predict_binary_single):
        _translate = QtCore.QCoreApplication.translate
        Dialog_predict_binary_single.setWindowTitle(_translate("Dialog_predict_binary_single", "Single classify binary"))
        self.label_6.setText(_translate("Dialog_predict_binary_single", "Image:"))
        self.pushButton_image.setText(_translate("Dialog_predict_binary_single", "Open"))
        self.label_8.setText(_translate("Dialog_predict_binary_single", "bands:"))
        self.label_9.setText(_translate("Dialog_predict_binary_single", "dtype:"))
        self.comboBox_dtype.setItemText(0, _translate("Dialog_predict_binary_single", "uint8"))
        self.comboBox_dtype.setItemText(1, _translate("Dialog_predict_binary_single", "uint10"))
        self.comboBox_dtype.setItemText(2, _translate("Dialog_predict_binary_single", "uint16"))
        self.comboBox_dtype.setItemText(3, _translate("Dialog_predict_binary_single", "float"))
        self.label_3.setText(_translate("Dialog_predict_binary_single", "windsize :"))
        self.label_5.setText(_translate("Dialog_predict_binary_single", "Model:"))
        self.pushButton_model.setText(_translate("Dialog_predict_binary_single", "Open"))
        self.label_10.setText(_translate("Dialog_predict_binary_single", "GPU ID:"))
        self.comboBox_gupid.setItemText(0, _translate("Dialog_predict_binary_single", "0"))
        self.comboBox_gupid.setItemText(1, _translate("Dialog_predict_binary_single", "1"))
        self.comboBox_gupid.setItemText(2, _translate("Dialog_predict_binary_single", "2"))
        self.comboBox_gupid.setItemText(3, _translate("Dialog_predict_binary_single", "3"))
        self.comboBox_gupid.setItemText(4, _translate("Dialog_predict_binary_single", "4"))
        self.comboBox_gupid.setItemText(5, _translate("Dialog_predict_binary_single", "5"))
        self.checkBox.setText(_translate("Dialog_predict_binary_single", "Onehot"))
        self.label_11.setText(_translate("Dialog_predict_binary_single", "Predict strategy:"))
        self.comboBox_strategy.setItemText(0, _translate("Dialog_predict_binary_single", "original"))
        self.comboBox_strategy.setItemText(1, _translate("Dialog_predict_binary_single", "smooth"))
        self.label_7.setText(_translate("Dialog_predict_binary_single", "Output mask:"))
        self.pushButton_mask.setText(_translate("Dialog_predict_binary_single", "Open"))


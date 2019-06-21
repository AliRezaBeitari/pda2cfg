# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

import sys
from pda import PDA
from graphviz import Digraph
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg


class MainWindow(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.center_image = QtSvg.QSvgWidget(self.central_widget)
        self.center_image.setObjectName("center_image")
        self.horizontalLayout.addWidget(self.center_image)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_export_as = QtWidgets.QMenu(self.menu_file)
        self.menu_export_as.setObjectName("menu_export_as")
        self.menu_help = QtWidgets.QMenu(self.menu_bar)
        self.menu_help.setObjectName("menu_help")
        self.menu_pda = QtWidgets.QMenu(self.menu_bar)
        self.menu_pda.setObjectName("menu_pda")
        main_window.setMenuBar(self.menu_bar)
        self.action_open_pda = QtWidgets.QAction(main_window)
        self.action_open_pda.setIconVisibleInMenu(False)
        self.action_open_pda.setObjectName("action_open_pda")
        self.action_open_pda.triggered.connect(self.open_pda)
        self.action_exit = QtWidgets.QAction(main_window)
        self.action_exit.setObjectName("action_exit")
        self.action_exit.triggered.connect(self.app_exit)
        self.action_about = QtWidgets.QAction(main_window)
        self.action_about.setObjectName("action_about")
        self.action_about.triggered.connect(self.show_about_dialog)
        self.action_gv = QtWidgets.QAction(main_window)
        self.action_gv.setObjectName("action_gv")
        self.action_gv.triggered.connect(lambda: self.export_as('gv'))
        self.action_pdf = QtWidgets.QAction(main_window)
        self.action_pdf.setObjectName("action_pdf")
        self.action_pdf.triggered.connect(lambda: self.export_as('pdf'))
        self.action_png = QtWidgets.QAction(main_window)
        self.action_png.setObjectName("action_png")
        self.action_png.triggered.connect(lambda: self.export_as('png'))
        self.action_svg = QtWidgets.QAction(main_window)
        self.action_svg.setObjectName("action_svg")
        self.action_svg.triggered.connect(lambda: self.export_as('svg'))
        self.action_convert = QtWidgets.QAction(main_window)
        self.action_convert.setObjectName("action_convert")
        self.action_convert.triggered.connect(self.convert_to_cfg)
        self.menu_export_as.addAction(self.action_gv)
        self.menu_export_as.addAction(self.action_pdf)
        self.menu_export_as.addAction(self.action_png)
        self.menu_export_as.addAction(self.action_svg)
        self.menu_file.addAction(self.action_open_pda)
        self.menu_file.addAction(self.menu_export_as.menuAction())
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_help.addAction(self.action_about)
        self.menu_pda.addAction(self.action_convert)
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_pda.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    
    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "PDA to CFG"))
        self.menu_file.setTitle(_translate("main_window", "File"))
        self.menu_export_as.setTitle(_translate("main_window", "Export as..."))
        self.menu_help.setTitle(_translate("main_window", "Help"))
        self.menu_pda.setTitle(_translate("main_window", "PDA"))
        self.action_open_pda.setText(_translate("main_window", "Open PDA"))
        self.action_open_pda.setShortcut(_translate("main_window", "Ctrl+O"))
        self.action_exit.setText(_translate("main_window", "Exit"))
        self.action_exit.setShortcut(_translate("main_window", "Ctrl+Q"))
        self.action_about.setText(_translate("main_window", "About"))
        self.action_about.setShortcut(_translate("main_window", "Ctrl+H"))
        self.action_gv.setText(_translate("main_window", ".gv"))
        self.action_pdf.setText(_translate("main_window", ".pdf"))
        self.action_png.setText(_translate("main_window", ".png"))
        self.action_svg.setText(_translate("main_window", ".svg"))
        self.action_convert.setText(_translate("main_window", "Convert to CFG"))

        self.set_menu_state(False)


    def set_menu_state(self, state):
        self.action_gv.setEnabled(state)
        self.action_pdf.setEnabled(state)
        self.action_png.setEnabled(state)
        self.action_svg.setEnabled(state)
        self.action_convert.setEnabled(state)


    def app_exit(self):
        sys.exit(0)


    def open_pda(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self.central_widget, 'Open PDA file...', '.', 'XML Files (*.xml)')

        if file_name:
            self.set_menu_state(True)

            self.pda = PDA(file_name)

            f = Digraph('pda_machine', filename='pda_tmp.gv', format='svg')
            f.attr(rankdir='LR', size='8,5')

            # Setup initial state
            f.attr('node', shape='plaintext')
            f.node(' ')
            f.attr('node', shape='circle')
            f.node(self.pda.initial_state)
            f.edge(' ', self.pda.initial_state, ' ')

            # Setup final states
            f.attr('node', shape='doublecircle')
            for fs in self.pda.final_states:
                f.node(fs)


            # Setup other states and transitions
            f.attr('node', shape='circle')
            for tr in self.pda.transitions:
                f.edge(tr['source'], tr['destination'], '{},{},{}'.format(PDA.lamb(tr['input']), PDA.lamb(tr['stack_read']), PDA.lamb(tr['stack_write'])))

            self.graph = f

            f.render()
            self.center_image.load('pda_tmp.gv.svg')

    
    def export_as(self, file_type):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self.central_widget, 'Export as' + file_type, '', file_type.upper() + ' Files (*.' + file_type + ')')

        if file_name:
            self.graph.format = file_type
            self.graph.render(file_name)


    def convert_to_cfg(self):
        self.cfg = self.pda.convert_to_cfg()

        messageBox = QtWidgets.QMessageBox()
        messageBox.setText('<font size=16>' + '<br>'.join(self.cfg) + '</font>')
        messageBox.setWindowTitle('Result CFG')
        messageBox.exec_()


    def show_about_dialog(self):
        QtWidgets.QMessageBox.information(self.central_widget, 'About me', 'Programmer: AliReza Beitari')
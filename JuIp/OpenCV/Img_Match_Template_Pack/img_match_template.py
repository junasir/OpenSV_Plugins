#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/6 20:11
# @Author  : Jun_军
# @File    : img_match_template.py


from copy import deepcopy
from sys import argv
from PySide2.QtCore import QRectF, Signal
from PySide2.QtGui import QImage, Qt
from PySide2.QtWidgets import QGridLayout, QLineEdit, QLabel, QMessageBox, QPushButton, QCompleter, \
    QApplication, QFrame

from JuControl.ju_dialog import JuDialog
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_node import Node


class ImgShowUi(JuDialog):

    def __init__(self, parent=None, default_parm=None, combox_list=None, log=None, *args, **kwargs):
        super(ImgShowUi, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("图像找外接矩形操作")
        self.ui_log = log
        self.combox_list = combox_list
        self._default_parm = default_parm
        self._parameter_change = False
        self.save_ok = False
        self.resize(400, 300)
        self._init_ui()
        self.bind_event()
        self.auto_complete()
        self._parameters_show()

    def _init_ui(self):
        label_input_variable = QLabel(self, text="输入原始图像:")
        self.label_input_variable = QLineEdit(self)
        label_input_variable1 = QLabel(self, text="输入模板图像:")
        self.label_input_variable1 = QLineEdit(self)
        label_1 = QLabel(self, text="method:")
        self.label_1 = QLineEdit(self)
        label_2 = QLabel(self, text="置信度:")
        self.label_2 = QLineEdit(self)
        label_output_variable = QLabel(self, text="输出图像变量:")
        self.label_output_variable = QLineEdit(self)
        self.update_btn = QPushButton(self, text="update")

        self._grid = QGridLayout(self)

        self._grid.addWidget(label_input_variable, 0, 0)
        self._grid.addWidget(self.label_input_variable, 0, 1)
        self._grid.addWidget(label_input_variable1, 1, 0)
        self._grid.addWidget(self.label_input_variable1, 1, 1)
        self._grid.addWidget(label_1, 2, 0)
        self._grid.addWidget(self.label_1, 2, 1)
        self._grid.addWidget(label_2, 3, 0)
        self._grid.addWidget(self.label_2, 3, 1)
        self._grid.addWidget(label_output_variable, 6, 0)
        self._grid.addWidget(self.label_output_variable, 6, 1)
        self._grid.addWidget(self.update_btn, 7, 0, 1, 2)

    def auto_complete(self):
        self.completer = QCompleter(self.combox_list)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.label_input_variable.setCompleter(self.completer)
        self.label_input_variable1.setCompleter(self.completer)

    def bind_event(self):
        self.update_btn.clicked.connect(self.generate_parameters)
        self.label_input_variable.textChanged.connect(self._parameter_changed)

    def generate_parameters(self):
        value_list = []
        output_list = []
        if self.label_input_variable.text() != "":
            value_list.append(self.label_input_variable.text())
        if self.label_input_variable1.text() != "":
            value_list.append(self.label_input_variable1.text())
        if self.label_1.text() != "":
            value_list.append(self.label_1.text())
        if self.label_2.text() != "":
            value_list.append(self.label_2.text())
        if self.label_output_variable.text() != "":
            output_list.append(self.label_output_variable.text())
        if len(value_list) == 4 and len(output_list) == 1:
            self._default_parm["variable_input"] = [self.label_input_variable.text(), self.label_input_variable1.text()]
            self._default_parm["value"] = value_list
            self._default_parm["variable_output"] = output_list
            self._parameter_change = False
            self.save_ok = True
            self.close()
        else:
            QMessageBox.warning(self, "错误", '请输入相应的参数.', QMessageBox.Ok)

    def _parameters_show(self):
        if len(self._default_parm["value"]) == 4:
            self.label_input_variable.setText(self._default_parm["value"][0])
            self.label_input_variable1.setText(self._default_parm["value"][1])
            self.label_1.setText(self._default_parm["value"][2])
            self.label_2.setText(self._default_parm["value"][3])
        if len(self._default_parm["variable_output"]) == 1:
            self.label_output_variable.setText(self._default_parm["variable_output"][0])

    def get_parameters(self):
        return self._default_parm

    def _parameter_changed(self):
        self._parameter_change = True

    def closeEvent(self, event):
        if self._parameter_change is True:
            res = QMessageBox.question(self, "Save", "Do you want to save the changes?",
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if res == QMessageBox.Yes:
                event.accept()
                self.generate_parameters()
            elif res == QMessageBox.Cancel:
                event.ignore()


class CalcGraphicsNode(QDMGraphicsNode):
    double_click = Signal()

    def __init__(self, node: 'Node'):

        super().__init__(node)
        # self.init_ui = init_ui
        self.user_logger = self.node.scene.user_logger
        self.init_node_ui = node.content
        self.init_node_ui.setFixedWidth(self.width)
        self.init_node_ui.setFixedHeight(self.height - 26)
        self.default_parm = self.init_node_ui.default_parm
        if self.default_parm is None:
            self.default_parm = {"object": {"type": "OpenCV", "index": 0},
                                 "operation_file": "JuOpencvHough", "operation_func": "opencv_template_match_func",
                                 "node_input_num": 2, "node_output_num": 1,
                                 "value": [],
                                 "result_flag": False,
                                 "result": {},
                                 "variable_input": [],
                                 "variable_output": []}

    def double_click_ui_show(self):
        combox_list = []
        for i in range(self.default_parm["node_input_num"]):
            default_parm = deepcopy(self.node.getInput(i).grNode.default_parm)
            for j in range(len(default_parm["variable_output"])):
                combox_list.append(default_parm["variable_output"][j])
        parameters_win = ImgShowUi(default_parm=self.default_parm, combox_list=combox_list, log=self.user_logger)
        parameters_win.exec_()
        if parameters_win.save_ok:
            self.default_parm = deepcopy(parameters_win.get_parameters())
            self.init_node_ui.setToolTip(str(self.default_parm["variable_input"]))
            default_parm = deepcopy(self.default_parm)
            default_parm["result_flag"] = False
            default_parm["result"] = {}
            self.init_node_ui.default_parm = self.default_parm

    def mouseDoubleClickEvent(self, event):
        """Overriden event for doubleclick. Resend to `Node::onDoubleClicked`"""
        self.node.onDoubleClicked(event)

    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("JuResource/img/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 0
        # if self.node.isShow():
        if self.node.isDirty(): offset = 24.0

        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        pass

    def serialize(self):
        res = super().serialize()
        if self.default_parm is not None:
            self.default_parm["result_flag"] = False
            self.default_parm["result"] = {}
            res['default_parm'] = self.default_parm
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        if "default_parm" in data:
            self.node.grNode.default_parm = data["default_parm"]
        return res


class JuIpImgMatchTemplate(Node):
    icon = ""
    op_code = "CalcNode_ImgMatchTemplate"
    op_title = "模板匹配"
    content_label_objname = "calc_node_img_match_Template"
    version = "v0.1"

    def __init__(self, scene, inputs=[(2, "input_ori_img"), (2, "input_template_img")], outputs=[(1, "output_img")]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.user_logger = self.scene.user_logger

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    #
    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        # print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res


if __name__ == "__main__":
    default_parm = {"object": {"type": "Opencv", "index": 0},
                    "operation_file": "JuOpencvTest", "operation_func": "opencv_test_func",
                    "node_input_num": 0, "node_output_num": 1,
                    "value": ["./JuResource/bac_1.png"],
                    "result_flag": False,
                    "result": {"img": None},
                    "variable_input": [],
                    "variable_output": ["img"]}
    app = QApplication(argv)
    window = ImgShowUi(default_parm=default_parm, combox_list=["img"])
    window.show()
    exit(app.exec_())

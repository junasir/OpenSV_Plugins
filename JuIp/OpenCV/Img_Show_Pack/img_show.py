#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/25 13:58
# @Author  : Jun_军
# @File    : img_show.py


from copy import deepcopy
from sys import argv

import cv2
from PySide2.QtCore import QRectF, Signal
from PySide2.QtGui import QImage, QPixmap, Qt
from PySide2.QtWidgets import QGridLayout, QLineEdit, QLabel, QMessageBox, QPushButton, QCompleter, \
    QApplication

from JuControl.ju_dialog import JuDialog
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_node import Node


class ImgShowUi(JuDialog):

    def __init__(self, parent=None, default_parm=None, combox_list=None, log=None, *args, **kwargs):
        super(ImgShowUi, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("显示图像")
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
        label_input_variable = QLabel(self, text="输入图像变量:")
        self.label_input_variable = QLineEdit(self)
        self.update_btn = QPushButton(self, text="update")
        self._grid = QGridLayout(self)
        # self._grid.addWidget(self.btn_img_path, 0, 0)
        # self._grid.addWidget(self.img_path, 0, 1)
        self._grid.addWidget(label_input_variable, 1, 0)
        self._grid.addWidget(self.label_input_variable, 1, 1)
        self._grid.addWidget(self.update_btn, 2, 0, 1, 2)

    def auto_complete(self):
        """
        配置自动补全函数
        """
        # 设置匹配模式  有三种： Qt.MatchStartsWith 开头匹配（默认）
        #                      Qt.MatchContains 内容匹配
        #                      Qt.MatchEndsWith 结尾匹配
        self.completer = QCompleter(self.combox_list)
        self.completer.setFilterMode(Qt.MatchContains)
        # 设置补全模式  有三种： QCompleter.PopupCompletion 弹出选项补全（默认）
        #                      QCompleter.InlineCompletion 行内显示补全
        #                      QCompleter.UnfilteredPopupCompletion 全显选项补全
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.label_input_variable.setCompleter(self.completer)

    def bind_event(self):
        self.update_btn.clicked.connect(self.generate_parameters)
        self.label_input_variable.textChanged.connect(self._parameter_changed)

    def generate_parameters(self):
        value_list = []
        if self.label_input_variable.text() != "":
            value_list.append(self.label_input_variable.text())
        if len(value_list) == 1:
            self._default_parm["variable_input"] = [self.label_input_variable.text()]
            self._default_parm["value"] = value_list
            self._parameter_change = False
            self.save_ok = True
            self.close()
        else:
            QMessageBox.warning(self, "错误", '请输入相应的参数.', QMessageBox.Ok)

    def _parameters_show(self):
        if len(self._default_parm["variable_input"]) != 0:
            self.label_input_variable.setText(self._default_parm["variable_input"][0])

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
                                 "operation_file": "JuOpencvTest", "operation_func": "opencv_test_show",
                                 "node_input_num": 1, "node_output_num": 0,
                                 "value": [],
                                 "result_flag": False,
                                 "result": {},
                                 "variable_input": [],
                                 "variable_output": []}

    def double_click_ui_show(self):
        combox_list = []
        for i in range(len(self.node.getInputs())):
            default_parm = deepcopy(self.node.getInputs()[i].grNode.default_parm)
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
        self.width = 300
        self.height = 326
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
        self._grid = QGridLayout()
        self._grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._grid)
        self.label = QLabel()
        self._grid.addWidget(self.label)
        # self.label.setPixmap(QPixmap("./JuResource/bac_1.png"))  # 我的图片格式为png.与代码在同一目录下
        self.label.setScaledContents(True)

        # self.edit = QLineEdit("1", self)
        # self.edit.setAlignment(Qt.AlignRight)
        # self.edit.setObjectName(self.node.content_label_objname)

    def img_show(self, img):
        show = deepcopy(img)
        try:
            size = (int(self.label.width()), int(self.label.height()))
            shrink = cv2.resize(show, size, interpolation=cv2.INTER_AREA)
            show = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            if self.label:
                self.label.setPixmap(QPixmap.fromImage(showImage))
        except BaseException as e:
            print(e)

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


class JuIpImgShow(Node):
    icon = "icons/in.png"
    op_code = "CalcNode_Imgshow"
    op_title = "显示图像"
    content_label_objname = "calc_node_img_show"
    version = "v0.1"

    def __init__(self, scene, inputs=[(1, "input_img")], outputs=[]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.user_logger = self.scene.user_logger

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        # print(self.grNode.node.id, "---=======")
        # print(self.grNode.default_parm, "===")

    def modify_ui_show(self):
        self.grNode.setToolTip("2222222222222")
        pass

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res
    #
    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
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
    pass

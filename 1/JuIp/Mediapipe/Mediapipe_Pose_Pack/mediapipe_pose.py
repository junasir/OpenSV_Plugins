#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/25 13:58
# @Author  : Jun_军
# @File    : mediapipe_pose.py


from copy import deepcopy
from sys import argv
from PySide2.QtCore import QRectF, Signal
from PySide2.QtGui import QImage, Qt
from PySide2.QtWidgets import QGridLayout,QLineEdit, QLabel, QMessageBox, QPushButton, QCompleter, \
    QApplication, QFrame

from JuControl.ju_dialog import JuDialog
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_node import Node


class MediapipePoseUi(JuDialog):

    def __init__(self, parent=None, default_parm=None, combox_list=None, log=None, *args, **kwargs):
        super(MediapipePoseUi, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("mediapipe姿态检测")
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
        label_thresh = QLabel(self, text="最小置信度:")
        self.label_thresh = QLineEdit(self)
        label_maxval = QLabel(self, text="最小跟踪度:")
        self.label_maxval = QLineEdit(self)
        label_output_variable = QLabel(self, text="输出图像变量:")
        self.label_output_variable = QLineEdit(self)
        self.update_btn = QPushButton(self, text="update")
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMaximumHeight(3)

        self._grid = QGridLayout(self)

        self._grid.addWidget(label_input_variable, 0, 0)
        self._grid.addWidget(self.label_input_variable, 0, 1)
        self._grid.addWidget(label_thresh, 1, 0)
        self._grid.addWidget(self.label_thresh, 1, 1)
        self._grid.addWidget(label_maxval, 2, 0)
        self._grid.addWidget(self.label_maxval, 2, 1)
        self._grid.addWidget(line, 4, 0, 1, 2)
        self._grid.addWidget(label_output_variable, 6, 0)
        self._grid.addWidget(self.label_output_variable, 6, 1)
        self._grid.addWidget(self.update_btn, 7, 0, 1, 2)

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
        output_list = []
        if self.label_input_variable.text() != "":
            value_list.append(self.label_input_variable.text())
        if self.label_thresh.text() != "":
            try:
                value_list.append(float(self.label_thresh.text()))
            except BaseException as e:
                print(e)
        if self.label_maxval.text() != "":
            try:
                value_list.append(float(self.label_maxval.text()))
            except BaseException as e:
                print(e)
        if self.label_output_variable.text() != "":
            output_list.append(self.label_output_variable.text())
        if len(value_list) == 3 and len(output_list) == 1:
            self._default_parm["variable_input"] = [self.label_input_variable.text()]
            self._default_parm["value"] = value_list
            self._default_parm["variable_output"] = output_list
            self._parameter_change = False
            self.save_ok = True
            self.close()
        else:
            QMessageBox.warning(self, "错误", '请输入相应的参数.', QMessageBox.Ok)

    def _parameters_show(self):
        if len(self._default_parm["value"]) == 3:
            self.label_input_variable.setText(self._default_parm["value"][0])
            self.label_thresh.setText(str(self._default_parm["value"][1]))
            self.label_maxval.setText(str(self._default_parm["value"][2]))
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
            self.default_parm = {"object": {"type": "Mediapipe", "index": 0},
                                 "operation_file": "JuMediapipePose", "operation_func": "mediapipe_pose_det",
                                 "node_input_num": 1, "node_output_num": 1,
                                 "value": [],
                                 "result_flag": False,
                                 "result": {},
                                 "variable_input": [],
                                 "variable_output": []}

    def double_click_ui_show(self):
        self.combox_list = []
        self.get_node_info(self.node.inputs)
        parameters_win = MediapipePoseUi(default_parm=self.default_parm, combox_list=self.combox_list, log=self.user_logger)
        parameters_win.exec_()
        if parameters_win.save_ok:
            self.default_parm = deepcopy(parameters_win.get_parameters())
            self.init_node_ui.setToolTip(str(self.default_parm["variable_input"]))
            default_parm = deepcopy(self.default_parm)
            default_parm["result_flag"] = False
            default_parm["result"] = {}
            self.init_node_ui.default_parm = self.default_parm

    def get_node_info(self, input):
        for l in input:
            node = l.edges
            for i in node:
                if "start_socket" in i.__dir__():
                    default_parm_node = i.start_socket.node
                    default_parm = default_parm_node.grNode.default_parm
                    for k in range(len(default_parm["variable_output"])):
                        self.combox_list.append(default_parm["variable_output"][k])
                    self.get_node_info(default_parm_node.inputs)

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


class MediapiePoseContent(QDMNodeContentWidget):
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


class JuIpMediapipePose(Node):
    icon = "icons/in.png"
    op_code = "CalcNode_Pose"
    op_title = "Mediapipe人体姿态检测"
    content_label_objname = "node_mediapipe_pose"
    version = "v0.1"

    def __init__(self, scene, inputs=[(1, "input")], outputs=[(1, "output")]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.user_logger = self.scene.user_logger

    def initInnerClasses(self):
        self.content = MediapiePoseContent(self)
        self.grNode = CalcGraphicsNode(self)

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
    window = MediapipePoseUi(default_parm=default_parm, combox_list=["img"])
    window.show()
    exit(app.exec_())
    pass

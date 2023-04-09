#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/7 21:51
# @Author  : Jun_军
# @File    : print_func.py


from copy import deepcopy
from json import loads, dumps
from sys import argv
from time import sleep
import zmq
from PySide2.QtCore import QRectF, Signal
from PySide2.QtGui import QImage, Qt
from PySide2.QtWidgets import QGridLayout, QLineEdit, QLabel, QMessageBox, QPushButton, QCompleter, \
    QApplication, QComboBox
from threading import Thread
from JuControl.ju_dialog import JuDialog
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_node import Node
from socket import socket, AF_INET, SOCK_STREAM


class ImgShowUi(JuDialog):

    def __init__(self, parent=None, default_parm=None, combox_list=None, log=None, *args, **kwargs):
        super(ImgShowUi, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle("print")
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
        self.close_flag = False
        self.queue_receive()
        # r = Thread(target=self.queue_receive, args=())
        # r.start()

    def _init_ui(self):
        # label_combobox = QLabel(self, text="通信文件:")
        # self.label_combobox = QComboBox(self)
        # self.label_combobox.addItems(["img", "video"])
        label_input_variable = QLabel(self, text="输入:")
        self.label_input_variable = QLineEdit(self)
        self.update_btn = QPushButton(self, text="update")
        self._grid = QGridLayout(self)
        # self._grid.addWidget(label_combobox, 0, 0)
        # self._grid.addWidget(self.label_combobox, 0, 1)
        self._grid.addWidget(label_input_variable, 1, 0)
        self._grid.addWidget(self.label_input_variable, 1, 1)
        self._grid.addWidget(self.update_btn, 3, 0, 1, 2)

    def set_combobox_items(self, info):
        if isinstance(info, dict):
            if "item" in info:
                completer = QCompleter(info["item"])
                completer.setFilterMode(Qt.MatchContains)
                completer.setCompletionMode(QCompleter.PopupCompletion)
                self.label_input_variable.setCompleter(completer)

    def queue_receive(self):
        try:
            context = zmq.Context()
            self.socket = context.socket(zmq.REQ)
            self.socket.connect("tcp://localhost:5557")
            info = {"func": "init_func", "args": ("Get Return Variable", )}
            self.socket.send_string(dumps(info, ensure_ascii=False, separators=(',', ':')))
            response = self.socket.recv()
            try:
                get_info = loads(response.decode())
                self.combox_list = get_info["args"]
                self.auto_complete()
                # self.set_combobox_items(get_info["args"])
                # if isinstance(get_info, dict):
                #     if "func" in get_info:
                #         if isinstance(get_info, dict) is True and hasattr(self, get_info.get("func")) is True:
                #             getattr(self, get_info.get("func"))(*get_info.get("args", ()), **get_info.get("kwargs", {}))
                #     elif "result" in get_info:
                #         pass
            except BaseException as e:
                self.ui_log.error(e)
        except BaseException as e:
            self.ui_log.error(e)

    def auto_complete(self):
        self.completer = QCompleter(self.combox_list)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.label_input_variable.setCompleter(self.completer)

    def bind_event(self):
        self.update_btn.clicked.connect(self.generate_parameters)
        self.label_input_variable.textChanged.connect(self._parameter_changed)

    def generate_parameters(self):
        if self.label_input_variable.text() != "":
            if self.combox_list[0] == self.label_input_variable.text():
                self._default_parm["variable_input"] = [self.label_input_variable.text()]
                self._default_parm["variable_output"] = [self.label_input_variable.text()]
            self._default_parm["value"] = [self.label_input_variable.text()]
            self._default_parm["socket_class"] = deepcopy(self.socket)
            self._parameter_change = False
            self.save_ok = True
            self.close_flag = True
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
            self.default_parm = {"object": {"type": "BaseLogic", "index": 0},
                                 "operation_file": "JuBaseFunc", "operation_func": "socket_info",
                                 "node_input_num": 1, "node_output_num": 1,
                                 "value": [],
                                 "result_flag": False,
                                 "result": {},
                                 "variable_input": [],
                                 "variable_output": [],
                                 "socket_class": None}

    def double_click_ui_show(self):
        self.combox_list = []
        self.get_node_info(self.node.inputs)
        parameters_win = ImgShowUi(default_parm=self.default_parm, combox_list=self.combox_list, log=self.user_logger)
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


class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        pass

    def serialize(self):
        res = super().serialize()
        if self.default_parm is not None:
            self.default_parm["result_flag"] = False
            self.default_parm["result"] = {}
            self.default_parm["socket_class"] = None
            res['default_parm'] = self.default_parm
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        if "default_parm" in data:
            self.node.grNode.default_parm = data["default_parm"]
        return res


class JuIpSocketCom(Node):
    icon = "icons/in.png"
    op_code = "CalcNode_Socket_Com"
    op_title = "socket_com"
    content_label_objname = "calc_node_img_socket_com"
    version = "v0.1"

    def __init__(self, scene, inputs=[(1, "input")], outputs=[(1, "output")]):
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

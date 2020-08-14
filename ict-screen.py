import qtpy
from pydm import Display
from qtpy.QtWidgets import (QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QScrollArea, QFrame,
    QApplication, QWidget)
from pydm.widgets import PyDMDrawingRectangle, PyDMPushButton, PyDMLabel
from pydm.utilities import connection

"""
PyDM Button that changes color/label based on the value of it's attached channel
"""
class ColorableButton(PyDMPushButton):
	def __init__(self, color_table=dict(), label_table=dict(), parent=None, label=None, icon=None, pressValue=None, relative=False, init_channel=None):
		super().__init__(parent=parent, label=label, icon=icon, pressValue=pressValue, relative=relative, init_channel=init_channel)
		self.color_table = color_table
		self.label_table = label_table

	def value_changed(self, newval):
		super().value_changed(newval)
		color = self.color_table[newval]
		label = self.label_table[newval]
		self.setText(label)
		self.setStyleSheet("\
			PyDMPushButton {\
				background-color: {0};\
				color: {1};\
			}".format(color[0], color[1]))
		
"""
PyDM Label that changes color/label based on the value of it's attached channel
"""
class ColorableLabel(PyDMLabel):
	def __init__(self, color_table=dict(), label_table=dict(), parent=None, label=None, icon=None, pressValue=None, relative=False, init_channel=None):
		super().__init__(parent=parent, label=label, icon=icon, pressValue=pressValue, relative=relative, init_channel=init_channel)
		self.color_table = color_table
		self.label_table = label_table

	def value_changed(self, newval):
		super().value_changed(newval)
		color = self.color_table[newval]
		label = self.label_table[newval]
		self.setText(label)
		self.setStyleSheet("\
			PyDMLabel {\
				background-color: {0};\
				color: {1};\
			}".format(color[0], color[1]))


class ICTChannelEntry(QFrame):

	def __init__(self, side, num):
		self.side = side
		self.num = num 
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.objectName = 'ICT_Channel_' + str(side) + str(num)

		# Add the toggle button
		colorButtonTable = {
			"CLOSED": [
				"rgb(0, 255, 0)", # Background
				"rgb(0, 0, 0)"  # Foreground 
			],
			"OPEN": [
				"rgb(255, 0, 0)",
				"rgb(255, 255, 255)"
			]
		}
		colorButtonLabelTable = {
			"ENABLED": "ONLINE",
			"DISABLED": "OFFLINE"
		}

		# Add the OFF button
		self.offBtn = PyDMPushButton(parent=self, label='TURN OFF', pressValue='1', init_channel='ca://$\{BASE\}:Output{0}{1}:SetState'.format(num, side))
		self.offBtn.setStyleSheet("\
			PyDMPushButton { \
				background-color: rgb(255, 0, 0); \
				color: rgb(255, 255, 255); \
			}")
		self.layout.addWidget(self.offBtn)

		# Add the ON button
		self.onBtn = PyDMPushButton(parent=self, label='TURN ON', pressValue='0', init_channel='ca://$\{BASE\}:Output{0}{1}:SetState'.format(num, side))
		self.onBtn.setStyleSheet("\
			PyDMPushButton { \
				background-color: rgb(0, 255, 0); \
				color: rgb(0, 0, 0); \
			}")
		self.layout.addWidget(self.onBtn)

		self.setLayout(self.layout)

		# Add the status widget 
		#self.statusLabel = ColorableLabel(color_table=colorButtonTable, label_table=colorButtonLabelTable, parent=self)


"""
Main window for the display 
"""
class ICTScreenDisplay(Display):
	def __init__(self, parent=None, args=[], macros=None):
		super(ICTScreenDisplay, self).__init__(parent=parent, args=args, macros=None)
		self.data = []
		self.app = QApplication.instance()

	def ui_filepath(self):
		return None 

	def setup_ui(self):
		self.main_layout = QVBoxLayout()
		self.setLayout(self.main_layout)
		
		self.main_layout.addWidget(ICTChannelEntry('A', 1))
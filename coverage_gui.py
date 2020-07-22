#! /usr/bin/env python3

# Author : Nuha Nishat
# Date: 6/29/20

from coverage_test import *
from Sprayer import *
from transforms import *
from Geometry import *

from PyQt5 import QtGui 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen, QPolygon, QLinearGradient, QFont, QColor
from PyQt5.QtCore import Qt, QPoint, QSize

import sys
import numpy as np


class DrawGeometry(QWidget):
	def __init__(self, gui):
		super(QWidget, self).__init__()
		self.title = "Coverage Test Visualizer"

		self.gui = gui

		# Window size param
		self.top = 150
		self.left = 150
		self.width = 900
		self.height = 900

		reset = QPushButton("Reset", self)
		reset.move(10,20)
		run_test = QPushButton("Run Test", self)
		run_test.move(10,50)

		reset.clicked.connect(self.show_reset)
		run_test.clicked.connect(self.show_test)

		# To get sprayer properties
		self.my_sprayer = Sprayer()

		# Call geometry class
		self.my_geometry = Geometry()

		self.sprayer_width = self.my_sprayer.sprayer_width
		self.sprayer_range = self.my_sprayer.sprayer_range
		self.spread_angle = self.my_sprayer.spread_angle

		# Get the made up surface for testing
		self.surface = self.my_geometry.test_surface

		# Get the cube resolution/sprayer movement res

		'''We will get the pose from the Sprayer class.
		This is the default starting pose for now. We
		will update this variable to change sprayer pose'''
		
		self.pose = [0.5, 0.5, 0] # Should be 6D. 3D for now

		self.InitWindow()


	def InitWindow(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.top, self.left, self.width, self.height)
		self.show()

	# For making sure the window shows up the right size
	def minimumSizeHint(self):
		return QSize(self.width, self.height)

	# For making sure the window shows up the right size
	def sizeHint(self):
		return QSize(self.width, self.height)

	
	def paintEvent(self, event):
		'''Call all the draw methods here to the painted'''
		qp = QPainter(self)
		qp.begin(self)

		self.draw_spray(qp)
		self.draw_surface(qp)

		qp.end()

	def x_map(self, x):
		return(int(x*self.width))

	def y_map(self, y):
		return(self.height - int(y*self.height) - 1)


	def make_surface(self):
		'''Get mold geometry from Geometry class and make lines
		to be displayed'''

		pass

	def make_spray(self):
		'''Get sprayer properties from Sprayer class and make
		geometry.
		params x,y: Position of sprayer origin'''

		# Sprayer position
		x = 0
		y = 0
		h_1 = self.sprayer_width
		h_2 = h_1 + 2*self.sprayer_range*np.tan(self.spread_angle)

		l = self.sprayer_range

		# The two points on the left
		x_1 = x 
		x_2 = x
		y_1 = y + h_1/2
		y_2 = y - h_1/2

		# The two points on the right
		x_3 = x + l
		x_4 = x + l
		y_3 = y - h_2/2
		y_4 = y + h_2/2


		# Orientation Axes

		# Origin
		x_5 = x
		y_5 = (y_1 + y_2)/2

		#Next Point
		x_6 = x + l + 0.1
		y_6 = (y_3 + y_4)/2

		# return the four vertices of polygon representing spray volume and the normal vector
		return [[x_1, y_1, 1], [x_2, y_2, 1], [x_3, y_3, 1], [x_4, y_4, 1], [x_5, y_5, 1], [x_6, y_6, 1]]


	def draw_surface(self,qp):
		'''Draw the surface I made up for now'''
		pen = QPen(Qt.black, 3, Qt.SolidLine)
		qp.setPen(pen)
		

		inc = 0.01

		for i in range(len(self.surface)-1):
			i_next = (i+1)%len(self.surface)
			curr_point = self.surface[i]
			next_point = self.surface[i_next]

			x_curr= curr_point[0]
			y_curr= curr_point[1]

			x_next = next_point[0]
			y_next = next_point[1]

			# diff_x = x_next - x_curr
			# diff_y = y_next - y_curr

			qp.drawLine(self.x_map(x_curr), self.y_map(y_curr), self.x_map(x_next), self.y_map(y_next))

			# gradient = diff_y/diff_x

			# if diff_x != 0:
			# 	x_i_next = x_curr
			# 	while x_i_next <= x_next:
			# 		qp.drawLine(self.x_map(x_curr), self.y_map(y_curr), self.x_map(x_i_next), self.y_map(y_next))
			# 		x_i_next += inc

			# if diff_y != 0:

	
	def draw_spray(self, qp):
		'''Draw a polygon for sprayer volume at the 
		given pose
		params pose: pose of srayer'''
		pen = QPen(Qt.blue, 5, Qt.SolidLine)
		qp.setPen(pen)
	
		rect = self.make_spray()
		

		rect_new = transform_poly(rect[0:4], self.pose)

		for i in range(len(rect_new)):
			i_next = (i+1)%len(rect_new)
			x_i = self.x_map(rect_new[i][0])
			y_i = self.y_map(rect_new[i][1])
			x_i_next = self.x_map(rect_new[i_next][0])
			y_i_next = self.y_map(rect_new[i_next][1])
			qp.drawLine(x_i, y_i, x_i_next, y_i_next)

		# Draw axes
		pen1 = QPen(Qt.green, 5, Qt.SolidLine)
		qp.setPen(pen1)

		rect_axis = transform_poly(rect[4:6], self.pose)

		qp.drawLine(self.x_map(rect_axis[0][0]), self.y_map(rect_axis[0][1]), self.x_map(rect_axis[1][0]), self.y_map(rect_axis[1][1]))


	def show_reset(self):
		# Reseting sprayer pose
		self.pose = [0.1, 0.8, np.pi/4]
		self.gui.repaint()

	
	def show_test(self):
		y = 0.8
		inc = 0.1

		while y > 0:
			self.pose = [0, y, 0]
			y -= inc
			self.gui.repaint()


class GUIWindow(QMainWindow):
	'''Creates the GUI Interface for test visualization'''
	def __init__(self):
		QMainWindow.__init__(self)
		self.setWindowTitle('Coverage Test')

		# Control buttons for the interface
		quit_button = QPushButton('Quit')
		quit_button.clicked.connect(App.exit)

		# parameters = QGroupBox('Test Cases')
		# parameter_layout = QVBoxLayout()


		# Draw stuff
		self.draw = DrawGeometry(self)

		# The layout of the interface
		widget = QWidget()
		self.setCentralWidget(widget)

		top_level_layout = QHBoxLayout()
		widget.setLayout(top_level_layout)
		# left_side_layout = QVBoxLayout()
		right_side_layout = QVBoxLayout()

		# left_side_layout.addWidget(parameters)
		right_side_layout.addWidget(self.draw)
		right_side_layout.addWidget(quit_button)

		# top_level_layout.addLayout(left_side_layout)
		top_level_layout.addLayout(right_side_layout)

	
	def trigger_repaint():
		self.draw.repaint()

	def draw(self,data):
		self.draw.draw()



if __name__ == '__main__':
	App = QApplication(sys.argv)
	gui = GUIWindow()

	gui.show()
	sys.exit(App.exec_())
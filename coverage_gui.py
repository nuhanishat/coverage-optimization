#! /usr/bin/env python3

# Author : Nuha Nishat
# Date: 6/29/20

from coverage_test import *
from Sprayer import *
from transforms import *
from Geometry import *

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSlider
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import numpy as np


class DrawGeometry(QWidget):
	def __init__(self, gui):
		super(QWidget, self).__init__()
		self.title = "Coverage Test Visualizer"

		
		# For slider
		self.gui = gui

		# Window size param
		self.top = 150
		self.left = 150
		self.width = 1000
		self.height = 1000

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
		# self.surface = self.my_geometry.test_surface
		self.robot_base = self.my_geometry.robot_base

		# Get the grid size
		self.grid_size = self.my_geometry.grid_size

		'''We will get the pose from the Sprayer class.
		This is the default starting pose for now. We
		will update this variable to change sprayer pose'''
		
		self.pose = [0.5, 0.5, 0] # Should be 6D. 3D for now

		# Change this to change table height 
		self.table_height = 0.15

		# self.new_voxel = self.my_geometry.my_compute_mesh_to_voxel()



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
		# self.draw_test_surface(qp)
		self.draw_robot_base(qp)
		self.draw_mold_surface(30,qp)
		self.draw_texts(qp)
		self.draw_table_top(qp)
		self.draw_sprayer(30,qp)

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


	def draw_robot_base(self,qp):
		'''Draw the surface I made up for now'''
		pen = QPen(Qt.black, 3, Qt.SolidLine)
		qp.setPen(pen)
		

		

		for i in range(len(self.robot_base)):
			i_next = (i+1)%len(self.robot_base)
			curr_point = self.robot_base[i]
			next_point = self.robot_base[i_next]

			x_curr= curr_point[0]
			y_curr= curr_point[1] + self.table_height

			x_next = next_point[0]
			y_next = next_point[1] + self.table_height

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

	def draw_mold_surface(self,slice_index,qp):
		'''Draw the volxalized mold surface'''
		pen = QPen(Qt.red, 3, Qt.SolidLine)
		qp.setPen(pen)

		voxel_grid = self.my_geometry.get_2D_mold_slice(self.my_geometry.compute_mesh_to_volume('voxel_mold_new.npy'),slice_index)

		# voxel_grid = self.my_geometry.voxel_grid

		surface_cells = []

		# Narrow down cells close to surface 
		for j in range(self.grid_size):
			for i in range(self.grid_size):
				if -0.08< voxel_grid[i,j] < 0.08 :
					surface_cells.append([i,j])
		
		
		# Save points on surface from linear interpolation
		surface_points = []

		for i in range(len(surface_cells)):
			temp = self.my_geometry.marching_cubes_2D_per_cell(voxel_grid, surface_cells[i])
		
			if len(temp) > 0:
				surface_points.append(temp[0])
				surface_points.append(temp[1])


		# Draw the surface
		for i in range(len(surface_points)):
			i_next = (i+1)%len(surface_points)
			curr_point = surface_points[i]
			next_point = surface_points[i_next]

			x_curr= curr_point[0]
			y_curr= curr_point[1]

			x_next = next_point[0]
			y_next = next_point[1]


			# Change these value to change mold position
			offset_x = 0.5*(self.my_geometry.cube_size/0.01)
			offset_y = self.table_height - 0.285*(self.my_geometry.cube_size/0.01)
			
			

			if abs(x_curr-x_next) <= self.my_geometry.cube_size*3 and abs(y_curr-y_next) <= self.my_geometry.cube_size*3:
				qp.drawLine(self.x_map(x_curr+offset_x), self.y_map(y_curr+offset_y), self.x_map(x_next+offset_x), self.y_map(y_next+offset_y))

	def draw_sprayer(self, slice_index, qp):
		'''Draw sprayer from volxalised sprayer stl model'''
		pen = QPen(Qt.red, 3, Qt.SolidLine)
		qp.setPen(pen)

		voxel_grid = self.my_geometry.get_2D_mold_slice(self.my_geometry.compute_mesh_to_volume('voxel_sprayer.npy'),slice_index)

		# voxel_grid = self.my_geometry.voxel_grid

		surface_cells = []

		# Narrow down cells close to surface 
		for j in range(self.grid_size):
			for i in range(self.grid_size):
				if -0.06< voxel_grid[i,j] < 0.06 :
					surface_cells.append([i,j])
		
		
		# Save points on surface from linear interpolation
		surface_points = []

		for i in range(len(surface_cells)):
			temp = self.my_geometry.marching_cubes_2D_per_cell(voxel_grid, surface_cells[i])
		
			if len(temp) > 0:
				surface_points.append(temp[0])
				surface_points.append(temp[1])


		# Draw the surface
		for i in range(len(surface_points)):
			i_next = (i+1)%len(surface_points)
			curr_point = surface_points[i]
			next_point = surface_points[i_next]

			x_curr= curr_point[0]
			y_curr= curr_point[1]

			x_next = next_point[0]
			y_next = next_point[1]


			# Change these value to change mold position
			offset_x = 0.2*(self.my_geometry.cube_size/0.01)
			offset_y = self.table_height - 0.1*(self.my_geometry.cube_size/0.01)
			
			

			if abs(x_curr-x_next) <= self.my_geometry.cube_size*2 and abs(y_curr-y_next) <= self.my_geometry.cube_size*2:
				qp.drawLine(self.x_map(x_curr+offset_x), self.y_map(y_curr+offset_y), self.x_map(x_next+offset_x), self.y_map(y_next+offset_y))


	
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


	

	def draw_table_top(self, qp):
		'''Draw a line that represents the table top'''
		pen = QPen()
		pen.setColor(QtGui.QColor('black'))
		pen.setWidth(2)
		qp.setPen(pen)	

		qp.drawLine(self.x_map(0),self.y_map(self.table_height),self.x_map(1.0),self.y_map(self.table_height))


	def draw_texts(self, qp):
		pen = QPen()
		pen.setColor(QtGui.QColor('green'))
		pen.setWidth(1)
	
		qp.setPen(pen)

		font = QtGui.QFont()
		font.setFamily("Times")
		# font.setBold(True)
		font.setPointSize(15)
		qp.setFont(font)

		# Robot Base

		qp.drawText(self.x_map(0.03), self.y_map(0.02 + self.table_height), 'Robot Base')
		

		# Mold
		qp.drawText(self.x_map(0.86), self.y_map(self.table_height + 0.025), 'Mold')

		# 


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


class MoldSlicer(QWidget):
	gui = None

	def __init__(self, name, low = 0, high = 65, initial_value = 20, ticks = 66):
		'''Class for the making 2D slicing of the mold'''
		
		# name: Displayed name of slider
		# low: Minimum value on slider
		# high : Maximum value on slider
		# initial_value: Should be a value of between low and high
		# ticks: Resolution of slider

		# Input values
		self.name = name 
		self.low = low 
		self.range = high - low
		self.ticks = ticks

		# Text value Widget
		QWidget.__init__(self)
		layout = QHBoxLayout()
		self.setLayout(layout)

		self.slider = QSlider(Qt.Horizontal)
		self.slider.setMinimum(0)
		self.slider.setMaximum(ticks)

		# call back - call change_value when slider changed
		self.slider.valueChanged.connect(self.change_value)

		self.display = QLabel()
		self.set_value(initial_value)
		self.change_value()

		layout.addWidget(self.display)
		layout.addWidget(self.slider)

	# Use this to get the value between low/high
	def value(self):
		# Return the current value of the slider 
		return (self.slider.value()/self.ticks) * self.range + self.low

	# Called when the value changes - low/high
	def change_value(self):
		if (MoldSlicer.gui != None):
			MoldSlicer.gui.repaint()
		self.display.setText('{0}: {1:.0f}'.format(self.name,self.value()))

	# Use this to change the value
	def set_value(self, value_f):
		value_tick = self.ticks * (value_f - self.low)/self.range
		value_tick = min(max(0, value_tick), self.ticks)
		self.slider.setValue(int(value_tick))
		self.display.setText('{0}: {1:.0f}'.format(self.name, self.value()))



class GUIWindow(QMainWindow):
	'''Creates the GUI Interface for test visualization'''
	def __init__(self):
		QMainWindow.__init__(self)
		self.setWindowTitle('Coverage Test')

		# Control buttons for the interface
		quit_button = QPushButton('Quit')
		quit_button.clicked.connect(App.exit)

		parameters = QGroupBox('Test Cases')
		parameter_layout = QVBoxLayout()

		self.slice = MoldSlicer('Slice')
		self.slice_sld = [self.slice]

		parameter_layout.addWidget(self.slice)
		parameters.setLayout(parameter_layout)

		# Draw stuff
		self.draw = DrawGeometry(self)

		self.slice.slider.valueChanged.connect(self.trigger_repaint)

		# The layout of the interface
		widget = QWidget()
		self.setCentralWidget(widget)

		top_level_layout = QHBoxLayout()
		widget.setLayout(top_level_layout)
		left_side_layout = QVBoxLayout()
		right_side_layout = QVBoxLayout()

		left_side_layout.addWidget(parameters)
		right_side_layout.addWidget(self.draw)
		right_side_layout.addWidget(quit_button)

		top_level_layout.addLayout(left_side_layout)
		top_level_layout.addLayout(right_side_layout)

		# Create Labels for objects
		# robot_text = QLabel()
		# robot_text.setText("Robot Base")

		# robot_text.setAlignment(Qt.AlignLeft)

		# self.robot_base_label = QLabel()
		# canvas = QtGui.QPixmap(400, 300)
		# self.robot_base_label.setPixmap(canvas)
		# self.setCentralWidget(self.robot_base_label)
		# self.draw_robot_text()

		MoldSlicer.gui = self

	
	def trigger_repaint(self):
		self.draw.repaint()

	def draw(self,data):
		self.draw.draw()



if __name__ == '__main__':
	App = QApplication(sys.argv)
	gui = GUIWindow()

	gui.show()
	sys.exit(App.exec_())
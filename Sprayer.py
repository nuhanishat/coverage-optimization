#! /usr/bin/env python3

# Author : Nuha Nishat
# Date: 6/26/20

# from Geometry import *

# from MoveSprayer import *

import numpy as np
import math

class Sprayer():
	def __init__(self):
		''' Holds sprayer properties and methods'''

		# Define sprayer geometry here / Load from a file 
		self.sprayer_width = 0.1 #meters
		self.sprayer_range = 0.20 #meters
		self.spread_angle = (20*np.pi)/180 #radians

		# Keep offsets in a dictionary
		self.offsets = {}

		# Save pose as a class variable
		self.pose = [0,0,0,0,0,0]

	
	def compute_sprayer_volume(self, pose):
		'''Creates the volume occupied by sprayer '''
		
		# Find cells representing sprayer volume
		volume_cells = []
		
		
		
		start_pos[0] = int(pose[0])
		start_pos[1] = int(pose[1])
		x_new = start_pos[0]
		y_new = start_pos[1]
		end_pos = [0,0]


		try:
			slope = np.tan(angle)
		except:
			slope = np.inf
		a = length*np.cos(angle)
		end_pos[0] = int(start_pos[0] + a) 
		b = length*np.sin(angle)
		end_pos[1] = int(start_pos[1] + b)

		dx = end_pos[0] - start_pos[0]
		dy = end_pos[1] - start_pos[1]

		steps = 0
		if (abs(dx) > abs(dy)):
			steps = abs(dx)
		else:
			steps = abs(dy)

		Xinc = float(dx)/float(steps)
		Yinc = float(dy)/float(steps)

		for i in range(0, steps):
			x_new = x_new + Xinc
			y_new = y_new + Yinc 
			volume_cells.append([x_new, y_new])

		return volume_cells	



	def check_if_inside_spray_volume(self, cell, volume_cells):
		''' Checks if cells in surface geometry are 
		inside the sprayer geometry given a pose.'''
		distance = math.sqrt((cell[0] - pose[0])**2 + (cell[1] - pose[1])**2 + (cell[2] - pose[2])**2)

		threshold_min = 0.05
		threshold_max = 0.2
		try:
			slope = -1/(threshold_max - threshold_min)

		except:
			slope = np.inf

		if distance < threshold_min:
			distance_coverage = 1

		elif distance > threshold_max:
			distance_coverage = 0

		else:
			distance_coverage = slope*(distance - threshold_max)

		# return distance_coverage

		# return True/False
		flag = False
		if collision:
			flag = True

		return flag

	def find_pose_from_offset(self, offset_cell):
		''' Generate sprayer pose from offset'''
		
		# Call the method that returns cube offsets
		# offsets = my_geometry.get_sprayer_pose_offset_cells(mold_geometry)
		pose = [0,0,0,0,0,0]
		return pose	

	def in_collision(self, pose, surface_point):
		'''Given sprayer position, does it collide with surface'''
		sprayer_position = [pose[0], pose[1]]
		
		flag = False
		if collision:
			flag = True

		return flag

		'''Check out rotation python library for converting poses
		to quaternion'''

		'''There was something about keeping poses as class
		variable.....'''


		

if __name__ == '__main__':
	Sprayer()
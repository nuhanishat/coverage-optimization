#! /usr/bin/env python3

# Author : Nuha Nishat
# Date: 6/26/20

# from Geometry import *

# from MoveSprayer import *

import numpy as np

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
		return volume_cells



	def check_if_inside_spray_volume(self, cell, volume_cells):
		''' Checks if cells in surface geometry are 
		inside the sprayer geometry given a pose.'''
		
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
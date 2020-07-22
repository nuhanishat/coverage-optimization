#! /usr/bin/env python3

# Author : Nuha Nishat
# Date: 6/26/20

import numpy as np

class MoveSprayer():
	def __init__(self,lp_file, spin_file):
		''' Create a combination of paths for the sprayer
		to follow'''

		# If we want to read in waypoints	
		self._lp_file = 'lawnmower_path.txt'


	def read_path_file(self):
		''' Read in waypoints from some file.'''
		waypoints = []
		return waypoints 

	
	def _lawnmower_path(self, pose, path_range):
		'''Given a range, chop up range by cells resolution and 
		return a sequence of poses for a linear path'''

		# Call Geometry class property cube size
		res = my_geometry.cube_size

		increment = path_range/cube_size

		path = []

		while pose <= pose + path_range:
			path.append(pose + increment)
		
		return path

	
	def _spin_path(self, pose, angle_range):
		'''Given initial pose and angle change, create spin path'''
		increment = 0.01

		path = []

	
		while pose <=  pose + angle_range:
			# Check if in collision here
			new_pose = pose + increment
			if not my_sprayer.in_collision(new_pose):
				path.append(new_pose)

		return path
			
	
	def _adjust_height(self, pose, delta):
		'''Change delta z given a pose and a delta height'''
		pose[2] += delta
		return pose


if __name__ == '__main__':
	MoveSprayer()







	



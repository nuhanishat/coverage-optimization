#! /usr/bin/env python3

# Author : Nuha Nishat
# Date: 6/26/20

# from Geometry import *

# from MoveSprayer import *

import numpy as np
import math
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

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
		self.pose = [0,0,0] #2D --->3D[0,0,0,0,0,0]


	def scan_convert(self,  start_pos, end_pos):
		full_line = []
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
			full_line.append([x_new, y_new])

		return full_line
										
	def points_on_spray_width(self, pose):
		start_pos = []
		end_pos = []
		
		mid_pos[0] = int(pose[0])
		mid_pos[1] = int(pose[1])
		
		angle = pose[2]

		try:
			slope = np.tan(angle)
		except:
			slope = np.inf

		if (angle<np.pi/2):
			start_pos_x = mid_pos[0] + np.cos(angle)*self.sprayer_width/2
			start_pos_y = mid_pos[1] + np.sin(angle)*self.sprayer_width/2 

			end_pos_x = mid_pos[0] - np.cos(angle)*self.sprayer_width/2
			end_pos_y = mid_pos[1] - np.sin(angle)*self.sprayer_width/2

		else:
			start_pos_x = mid_pos[0] - np.cos(angle)*self.sprayer_width/2
			start_pos_y = mid_pos[1] + np.sin(angle)*self.sprayer_width/2 

			end_pos_x = mid_pos[0] + np.cos(angle)*self.sprayer_width/2
			end_pos_y = mid_pos[1] - np.sin(angle)*self.sprayer_width/2	

		start_pos.append(start_pos_x)
		start_pos.append(start_pos_y)
		end_pos.append(end_pos_x)
		end_pos.append(end_pos_y)
		return np.asarray(scan_convert(start_pos, end_pos))		

	def angles_for_start_points(self, pose, start_points):
		angles = []
		angle_to_be_covered = 90 - (180 - self.spread_angle)
		dtheta = angle_to_be_covered/len(start_points)

		#Find angles w.r.t x-axis (see notes in PCC book)
		angleOAB = 90 - angle_to_be_covered
		angleAPO = 180 - pose[3]
		angleAOP = 180 - (angleOAB + angleAPO)
		anglePOB = angle_to_be_covered - angleAOP 

		angle_in_x = anglePOB

		for i in range(0, dtheta):
			angle = angle_to_be_covered - dtheta
			angles.append(angle)
			
		angles  = np.asarray(angles)
		##Calculating lower half of angles
		bot_angles  =  -angles[::-1]
		angles = np.append(angles, bot_angles)
		angles_in_x  = angles - angle_in_x
		return angles, angles_in_x 

	def points_on_spray_range(self, pose, start_points, start_angles, angles_not_in_x):
		##Look  at  notes to understand wtf is this
		length_PY = self.sprayer_range/np.cos(angles_not_in_x)
		end_point_x = start_points[:,0] + np.cos(start_angles)*length_PY
		end_point_y = start_points[:,1] + np.sin(start_angles)*length_PY
		end_points = np.transpose(np.array(([end_point_x],[end_point_y])))
		end_points = end_points.reshape(len(end_point_x), 2)
		return end_points

	## TODO: Add spray width calc for all directions
	def compute_spray_area(self, pose):
		'''Creates the area occupied by sprayer '''
		
		# Find cells representing sprayer volume
		area_cells = []
		start_points = points_on_spray_width(pose)
		angles_not_in_x, start_angles = angles_for_start_points(pose, start_points)
		end_points = points_on_spray_range(pose, start_points, start_angles, angles_not_in_x) 

		for i in range(len(start_points)):
			area_cells.append(scan_convert(start_points[i],  end_points[i]))

		self.cov_area = Polygon([(start_points[0,0], start_points[1,0]), (start_points[0,len(start_points)-1],start_points[1,len(start_points)-1]), (end_points[0,0], end_points[1,0]), (end_points[0,len(end_points)-1],end_points[1,len(end_points)-1])])

		return  area_cells

	def distance_cov(self, cell):
		distance = math.sqrt((cell[0] - pose[0])**2 + (cell[1] - pose[1])**2)

		threshold_min = 0.05
		threshold_max = 0.2

		try:
			slope = -1/(threshold_max - threshold_min)

		except:
			slope = np.inf

		c = slope*(-threshold_max) #Y-intercept

		if distance < threshold_min:
			distance_coverage = 1

		elif distance > threshold_max:
			distance_coverage = 0

		else:
			distance_coverage = slope*(distance) + c

		return distance_coverage

	def angle_cov(self, cell, surface_norms, norm_sprayer):
		cos_theta = np.dot(norm_sprayer, surface_norms[cell[0], cell[1]])/(math.sqrt(norm_sprayer[0]*norm_sprayer[0] + norm_sprayer[1]*norm_sprayer[1])*math.sqrt(surface_norms[cell[0]]*surface_norms[cell[0]] + surface_norms[cell[1]]*surface_norms[cell[1]]))
		theta = np.degrees(np.arccos(cos_theta))

		threshold_min = 45
		threshold_max = 80

		try:
			slope = -1/(threshold_max - threshold_min)

		except:
			slope = np.inf

		c = slope*(-threshold_max)

		if (abs(theta)<threshold_min):
			angle_coverage = 1

		elif (abs(theta)>threshold_max):
			angle_coverage = 0

		else:
			angle_coverage = slope*(abs(theta)) + c

		return angle_coverage

	def check_if_inside_spray_volume(self, cell, volume_cells):
		''' Checks if cells in surface geometry are 
		inside the sprayer geometry given a pose.'''

		point = Point(cell[0], cell[1])

		if (self.cov_area.contains(point)):
			flag = True
		else:
			flag = False

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
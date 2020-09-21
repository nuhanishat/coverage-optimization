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

##TODO: Need to accept float as well
	def scan_convert(self,  start_pos, end_pos):
		full_line = []
		dx = end_pos[0] - start_pos[0]
		dy = end_pos[1] - start_pos[1]

		x_new = start_pos[0]
		y_new = start_pos[1]

		steps = 0
		if (abs(dx) > abs(dy)):
			steps = abs(dx)
			# print("STEPS", steps, abs(dx))
	
		else:
			steps = int(abs(dy))



		Xinc = float(dx)/0.1#float(steps)
		Yinc = float(dy)/0.1#float(steps)

		for i in range(0, int(steps)+1):
			x_new = x_new + Xinc
			y_new = y_new + Yinc 
			full_line.append([x_new, y_new])

		return full_line
										
	def points_on_spray_width(self, pose):
		start_pos = []
		end_pos = []
		mid_pos = [int(pose[0]),int(pose[1])]
		
		#mid_pos[0] = int(pose[0])
		#mid_pos[1] = int(pose[1])
		
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
		# print("start_pos", start_pos, end_pos)
		return np.asarray(self.scan_convert(start_pos, end_pos))		

	def angles_for_start_points(self, pose, start_points):
		angles = []
		angle_to_be_covered = self.spread_angle#90 - (180 - self.spread_angle)
		dtheta = angle_to_be_covered/len(start_points)

		#Find angles w.r.t x-axis (see notes in PCC book)
		angleOAB = 90 - angle_to_be_covered
		angleAPO = 180 - pose[2]
		angleAOP = 180 - (angleOAB + angleAPO)
		anglePOB = angle_to_be_covered - angleAOP 

		angle_in_x = anglePOB
		reduce_angle = angle_to_be_covered
		# print (reduce_angle)
		for i in range(0, int(len(start_points)/2)):
			angle = reduce_angle - dtheta
			angles.append(angle)
			reduce_angle = angle 
			
		angles  = np.asarray(angles)
		##Calculating lower half of angles
		bot_angles  =  -angles[::-1]
		angles = np.append(angles, bot_angles)
		angles_in_x  = angles - angle_in_x
		return angles, angles_in_x 

	def points_on_spray_range(self, pose, start_points, start_angles, angles_not_in_x):
		##Look  at  notes to understand wtf is this
		length_PY = self.sprayer_range/np.cos(angles_not_in_x)
		# print( (start_points.shape, start_angles.shape))
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
		start_points = self.points_on_spray_width(pose)
		start_points = np.asarray([[0.05,0.0],[0.03,0.0],[0.01,0.0],[-0.01,0.0],[-0.03,0.0],[-0.05,0.0]])
		angles_not_in_x, start_angles = self.angles_for_start_points(pose, start_points)
		end_points = self.points_on_spray_range(pose, start_points, start_angles, angles_not_in_x) 

		for i in range(len(start_points)):
			area_cells.append(self.scan_convert(start_points[i],  end_points[i]))

		# print ((start_points.shape))
		# print (start_points[0,0], start_points[0,1])
		# print (start_points[len(start_points)-1,0],start_points[len(start_points)-1,1])
		self.cov_area = Polygon([(start_points[0,0], start_points[0,1]), (start_points[len(start_points)-1,0],start_points[len(start_points)-1,1]), (end_points[0,0], end_points[0,1]), (end_points[len(end_points)-1,0],end_points[len(end_points)-1,1])])

		return  area_cells

	def distance_cov(self, cell):
		distance = math.sqrt((cell[0] - self.pose[0])**2 + (cell[1] - self.pose[1])**2)

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

##TODO: Make sure values being sent make sense for the normals
	def angle_cov(self, cell, surface_norms, norm_sprayer):
		# print (np.dot(norm_sprayer, surface_norms[0, 1]))
		cos_theta = np.dot(norm_sprayer, surface_norms[cell[0], cell[1]])/(math.sqrt(norm_sprayer[0]*norm_sprayer[0] + norm_sprayer[1]*norm_sprayer[1])*math.sqrt(surface_norms[cell[0]]*surface_norms[cell[0]] + surface_norms[cell[1]]*surface_norms[cell[1]]))
		# cos_theta = np.dot(norm_sprayer, surface_norms[0, 1])/(math.sqrt(norm_sprayer[0,0]*norm_sprayer[0,0] + norm_sprayer[0,1]*norm_sprayer[0,1])*math.sqrt(surface_norms[0,0]*surface_norms[0,0] + surface_norms[0,1]*surface_norms[0,1]))
		# print (cos_theta.shape)
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
	# Sprayer()
	unit_test = Sprayer()
	# start = [0,0,0]
	# end = [0,6,0]
	# ans = unit_test.scan_convert(start, end)
	# ans = unit_test.points_on_spray_width(start)
	# print ("LOOK HERE",ans.shape)
	pose = [0,0,0]
	# start = [0.05,0.0]
	# end = [-0.05,0.0]

	# points = np.asarray([[0.05,0.0],[0.03,0.0],[0.01,0.0],[-0.01,0.0],[-0.03,0.0],[-0.05,0.0]])
	# ans_not_x, ans_in_x = unit_test.angles_for_start_points(pose, points)
	# ans = unit_test.points_on_spray_range(pose, points, ans_in_x, ans_not_x)
	# ans = unit_test.compute_spray_area(pose)

	# ans = unit_test.distance_cov([0,8])
	# ans = unit_test.angle_cov(np.asarray([[0,8]]),np.asarray([[0.1,0.1]]),np.asarray([[0.2,0.2]]))


	print (ans)
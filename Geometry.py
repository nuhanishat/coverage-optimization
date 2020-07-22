#! /usr/bin/env python3

# Author : Nuha Nishat
# Date: 6/26/20


import numpy as np

class Geometry():
	def __init__(self, file_name = "model.stl", cube_size= 0.01):
		''' Class that deals with all things mold geometry'''

		# Load model
		self.model = file_name

		# Cube size/cell resolution
		# self.cube_size = cube_size
		self.cube_size = 0.01

		# Save the mold grid as a class variable
		self.voxel_grid = self.compute_mesh_to_volume()

		# Save a seperate grid for coverage
		grid_size = 64
		self.covered_grid = np.zeros(grid_size)

		# Made up surface for testing defined by a series of points
		self.test_surface = [[0, 0.1],[0.3, 0.1],[0.3, 0.3],[0.7, 0.3],[0.7, 0.1],[1.0, 0.1]]



	def compute_mesh_to_volume(self):
		'''Returns SDF grid'''
		grid = []
		# Do Math
		return grid

	def get_mold_surface_normals(self): 
		'''Returns normals of surface cells'''
		norm_list = []
		# Do more math....
		return norm_list


	def get_sprayer_pose_offset_cells (self):
		'''Get an offset for each the sprayer'''
		cells = []
		return cells 


	def compute_coverage(self, pose, surface_norms):
		'''Calculate coverage based of dot product and distance of sprayer
		from surface. Update the class variable'''

		# Update with dot_product coverage percentage
		covered_dot = np.zeros(64)
		self.covered_grid += covered_dot

		# Use Sprayer().is_inside_sprayer() for distance coverage
		covered_dist = np.zeros(64)
		self.covered_grid += covered_dist
		

	def check_if_move_is_possible(self,pose):
		''' Check if transition between two poses is possible. 
		No collision with mold or arm itself'''
		flag = False
		if yes:
			flag = True

		return flag


	# Find grid not covered 
	def find_uncovered_pose(self):
		'''Find pose for uncovered cubes in grid'''
		return poses


	def compute_cell_to_cartesian(self,cell_location):
		''' Given a grid cell location, calculate the cartesian
		location of the point in workspace'''
		point = []
		return point


	def compute_cartesian_to_cell(self, cartesian_point):
		'''Given a cartesian location in the workspace,
		calculate the grid cell location of that point'''
		cell = []
		return cell

	

if __name__ == '__main__':
	Geometry()
	
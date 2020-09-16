#! /usr/bin/env python3

# Author : Nuha Nishat
# Date: 6/26/20

# from mesh_to_sdf import mesh_to_voxels

import trimesh
# import skimage



import numpy as np


class Geometry():
	def __init__(self, file_name = "model.stl", cube_size= 0.01):
		''' Class that deals with all things mold geometry'''

		# Load model
		#self.model = file_name

		# Cube size/cell resolution
		# self.cube_size = cube_size
		self.cube_size = 0.008

		self.grid_size = 66


		
		self.voxel_sprayer = self.compute_mesh_to_volume('voxel_sprayer.npy')

		# Save a seperate grid for coverage
		
		self.covered_grid = np.zeros(self.grid_size)

		# Made up surface for testing defined by a series of points
		#self.test_surface = [[0, 0.1],[0.1, 0.1],[0.3, 0.3],[0.7, 0.3],[0.7, 0.1],[1.0, 0.1]]

		# Make the robot base
		self.robot_base = [[0, 0.05],[0.2, 0.05],[0.2, 0],[0, 0]]

		# Sprayer geometry 

		# Trimesh test geometry
		#self.new_voxel = self.my_compute_mesh_to_voxel()


	def my_compute_mesh_to_voxel(self):
		'''Attempting to understand this voxel mess'''
		mesh = trimesh.load('/home/nuhanishat/kinova_ws/src/Mold1.STL')
		voxel = mesh.voxelized(pitch=self.cube_size)

		print(voxel.as_boxes)


	def compute_mesh_to_volume(self, file_name):
		'''Returns SDF grid'''
		grid = np.load('/home/nuhanishat/kinova_ws/src/' + file_name)
		return grid


	def get_2D_mold_slice(self, grid, slice_index):

		plane_slice = np.zeros((self.grid_size,self.grid_size))
		for i in range(66):
			for j in range(66):
				plane_slice[i,j] = grid[i,j,slice_index] # Get the slice at depth, z = 30 
		
		# Do Math
		return plane_slice

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
		'''param cell_location: list
		point is at the center of cube'''
		# point = [x*self.cube_size/2.0 for x in cell_location]

		point = [x*self.cube_size for x in cell_location]
		return point


	def compute_cartesian_to_cell(self, cartesian_point):
		'''Given a cartesian location in the workspace,
		calculate the grid cell location of that point'''
		cell = [x/self.cube_size for x in cartesian_point]
		return cell

	def compute_square_vertices(self, voxel_location):
		'''Input the upper left vertex to get the other three vertices'''
		
		vertices = []

		#Upper left
		upper_left = voxel_location
		
		#Lower left
		lower_left = [voxel_location[0], voxel_location[1] - 1]
		
		#Upper right
		upper_right = [voxel_location[0] + 1, voxel_location[1]]
		
		#Lower right
		lower_right = [voxel_location[0] + 1, voxel_location[1] - 1]
		
		vertices.append(upper_left)
		vertices.append(upper_right)
		vertices.append(lower_left)
		vertices.append(lower_right)

		return vertices

	def sdf_linear_interpolation(self, point1, sdf_value1, point2, sdf_value2):
		'''Takes in the coordinates of two vertices and the 
		sdf value and returns the point at the surface with sdf value 0'''

		# If two points are horizontally adjacent
		x1 = point1[0]
		x2 = point2[0]
		y1 = point1[1]
		y2 = point2[1]

		int_point = []

		if y1 == y2:
			int_x = x1 + (x2 - x1)*((0.00 - sdf_value1)/(sdf_value2 - sdf_value1))
			int_point = [int_x, y1]

		if x1 == x2:
			int_y = y1 + (y2 - y1)*((0.00 - sdf_value1)/(sdf_value2 - sdf_value1))
			int_point = [x1, int_y]

		return int_point


	def marching_cubes_2D_per_cell(self, slice_grid ,point):
		'''Extracts the surface from voxels'''

		# Get the four vertices of cube
		vertices = self.compute_square_vertices(point)

		# Get values of vertices 
		sdf_values = [slice_grid[x[0],x[1]] for x in vertices]

		# Do some linear interpolation to find the point in an edge
		# with an sdf value of 0. This is where the surface is.

		# Save each vertices as cartesian values
		v_1 = self.compute_cell_to_cartesian(vertices[0])
		v_2 = self.compute_cell_to_cartesian(vertices[1])
		v_3 = self.compute_cell_to_cartesian(vertices[2])
		v_4 = self.compute_cell_to_cartesian(vertices[3])

		# Save sdf values for each vertex
		sdf_1 = sdf_values[0]
		sdf_2 = sdf_values[1]
		sdf_3 = sdf_values[2]
		sdf_4 = sdf_values[3]

		
		# Surface point
		surface_points = []

		# if v1 and v2 values have different signs, surface falls on this edge
		if sdf_1*sdf_2 < 0:
			# print('Appending1')
			surface_points.append(self.sdf_linear_interpolation(v_1, sdf_1, v_2, sdf_2))

		# if v1 and v3 values have different signs, surface falls on this edge
		if sdf_1*sdf_3 < 0:
			# print('Appending2')
			surface_points.append(self.sdf_linear_interpolation(v_1, sdf_1, v_3, sdf_3))

		# if v2 and v4 values have different signs, surface falls on this edge
		if sdf_2*sdf_4 < 0:
			# print('Appending3')
			surface_points.append(self.sdf_linear_interpolation(v_2, sdf_2, v_4, sdf_4))

		#
		if sdf_3*sdf_4 < 0:
			# print('Appending4')
			surface_points.append(self.sdf_linear_interpolation(v_3, sdf_3, v_4, sdf_4))

		return surface_points
	

if __name__ == '__main__':
	Geometry()
	
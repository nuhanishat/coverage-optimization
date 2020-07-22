#! /usr/bin/env python3

# Author : Nuha Nishat
# Date: 6/26/20

# from MoveSprayer import*
# from Geometry import*
# from Sprayer import*

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from coverage_gui import *

import numpy as np
import sys



class CoverageTest():
	'''Runs the test and updates Geometry().covered_grid and Sprayer().pose'''
	def __init__(self):
		self.test()
		

	def reset(self):
		'''Clear all calculated coverage. Reset sprayer pose
		to 0'''
		pass

	def test(self):
		# Get geometry
		# grid = self.my_geometry.mesh_to_volume()

		# Get initial offset
		# volume = self.sprayer_volume()

		''' - Get sprayer path
			- Adjust height
			- Calculate coverage
			- While uncovered 
				- find nearest uncoverd pose 
				- Add spin in path
				- Recalculate coverage'''

		
		grid = np.load('/home/nuhanishat/kinova_ws/src/voxel_grid.npy')

		x = []
		y = []
		z = []

		

		plane_slice = np.zeros((66,66))
		
		for i in range(66):
			for j in range(66):
				plane_slice[i,j] = grid[i,j,30] # Get the slice at depth, z = 30 



		# fig = plt.figure()

		# ax = fig.add_subplot(111, projection='3d')
		# ax.scatter(x,y,z)
		# plt.show()

		plt_points = []
		for i in range(66):
			for j in range(66):
				if plane_slice[i,j] <= 0:
					x.append(i)
					y.append(j)


		color_map = plt.imshow(plane_slice, vmax=0)
		color_map.set_cmap("gray")
		plt.colorbar()
		# plt.plot(x,y)

		# print(x)
		# print(y)

		plt.show()





if __name__ == '__main__':
	CoverageTest()
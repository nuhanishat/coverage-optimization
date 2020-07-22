#! /usr/bin/env python3

# Author: Nuha Nishat
# Date: 6/30/20

import numpy as np

import sys

# def translate():
# 	pass

# def rotate_point(angle, vector):
# 	pass

def transform_poly(poly, pose):
	'''Transforms Spray geometry to given pose'''
	
	# Rotation Matrix
	angle = pose[2]

	R = np.identity(3)
	R[0][0] = np.cos(angle)
	R[0][1] = -np.sin(angle)
	R[1][0] = np.sin(angle)
	R[1][1] = np.cos(angle)


	# Translation Matrix
	T = np.identity(3)
	T[0,2] = pose[0]
	T[1,2] = pose[1]

	# Accumalated Matrix
	mat = np.matmul(T, R)

	poly_new = mat @ np.transpose(poly)
	poly_new = np.transpose(poly_new)

	return poly_new


if __name__ == '__main__':
	poly = [[0, 1, 1], [0, 2, 2]]
	poly_new = rotate_poly(poly, 30*np.pi/180)





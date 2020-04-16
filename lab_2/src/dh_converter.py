#! /usr/bin/python

from tf.transformations import *
import json

def dh_to_urdf():
	json_reader = open('../yaml/dh_params.json', 'r')
	dh_params = json.loads(json_reader.read())

	urdf_file_writer = open('../yaml/urdf.yaml', 'w')
	axis_x = (1, 0, 0)
	axis_z = (0, 0, 1)

	for key in dh_params.keys():
		a, d, alpha, theta = dh_params[key]    

		x_translation = translation_matrix((a, 0, 0))  
		x_rotation = rotation_matrix(alpha, axis_x)

		z_translation = translation_matrix((0, 0, d))  
		z_rotation = rotation_matrix(theta, axis_z)      

		dh = concatenate_matrices(z_translation, z_rotation, x_translation, x_rotation)  
		rpy_params = euler_from_matrix(dh)
		xyz_params = translation_from_matrix(dh)

		urdf_file_writer.write(key + ": \n")
		urdf_file_writer.write("	joint_xyz: {} {} {} \n".format(*xyz_params))
		urdf_file_writer.write("	joint_rpy: {} {} {} \n".format(*rpy_params))
		urdf_file_writer.write("	link_xyz: {} 0 0 \n".format(xyz_params[0]/2))
		urdf_file_writer.write("	link_rpy: 0 0 0 \n")
		urdf_file_writer.write("	link_length: {} \n\n".format(a))

if __name__ == '__main__':
    dh_to_urdf()

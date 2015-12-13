#!/usr/bin/env python

#
# FLACtoMP3.py version 1.0
# Author: Jim Sam
#
# This script turns high resolution FLAC files into mp3s for mobile devices.
# It is a work in progress, but it still works.
#
# It assumes you have FFMPEG installed on your system in a way that does not
# require a defined directory to launch.
#

import os
import subprocess

def check_channels(file):
	channels = 0
    return channels

def make_file_list(hi_res_path):

	dir1 = os.listdir(hi_res_path)

	file_list = []

	for file in dir1:
		file_name=str(file)
		if file_name[-5:] == ".flac":
			file_list.append(file_name[:-5])
	
	return file_list

def make_command_list(file_list, hi_res_path, lo_res_path):
	command_list = []
	for file in file_list:
		command_list.append("ffmpeg -i \"" + hi_res_path + str(file) + ".flac\" -write_id3v1 1 -id3v2_version 3 -dither_method modified_e_weighted -out_sample_rate 48k -b:a 320k \"" + lo_res_path + str(file) + ".mp3\"")
		
	return command_list

def main(): 

	hi_res_path = input("The path of the high-resolution files: ")
	lo_res_path = input("The path of the low-resolution files: ")
	
	file_list = make_file_list(hi_res_path)
	command_list = make_command_list(file_list, hi_res_path, lo_res_path)
	
	for command in command_list:
		subprocess.call(command, shell=True)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
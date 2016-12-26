#
# FLACtoMP3.py
# Author: Jim Sam
#
# This script turns high resolution FLAC files into mp3s for mobile devices.
# It is a work in progress, but it still works.
#
# It assumes you have FFMPEG installed on your system in a way that does not
# require a defined directory to launch.
#

import os
import pexpect
import subprocess
import re

def check_channels(file, hi_res_path):
    file = str(file)
    hi_res_path = str(hi_res_path)

    data = pexpect.run('ffmpeg -i \"' + hi_res_path + file + '\".flac')
    data = str(data)

    if "mono" in data:
        channels = 1
    elif "stereo" in data:
        channels = 2

    return channels

def make_command(file, hi_res_path, lo_res_path):
    file = str(file)
    hi_res_path = str(hi_res_path)
    lo_res_path = str(lo_res_path)

    command = ""
    channels = check_channels(file, hi_res_path)

    if channels == 1:
        command = ['ffmpeg','-i',
                    hi_res_path+file+'.flac',
                    '-write_id3v1', '1','-id3v2_version','3',
                    '-dither_method','modified_e_weighted',
                    '-out_sample_rate','48k','-b:a','160k',
					lo_res_path+file+'.mp3']
    if channels == 2:
        command = ['ffmpeg','-i',
                    hi_res_path+file+'.flac',
                    '-write_id3v1','1','-id3v2_version','3',
                    '-dither_method','modified_e_weighted',
                    '-out_sample_rate','48k', '-b:a','320k',
					lo_res_path+file+'.mp3']
    return command

def gimmespace():
    for i in range(10):
        print()

def make_file_list(hi_res_path):
    dir1 = os.listdir(hi_res_path)
    file_list = []

    for file in dir1:
        file_name=str(file)
        if file_name[-5:] == ".flac":
            file_list.append(file_name[:-5])

    return file_list

def validate_path(path):
	result = re.match(r'(^/.+/$)|(^\w:\\$)|(^\w:\\.+\\$)', path)
	return result

def main():
    toggle = False
    while toggle==False:
        hi_res_path = input("The path of the high-resolution files: ")
        lo_res_path = input("The path of the low-resolution files: ")
        a = validate_path(hi_res_path)
        b = validate_path(lo_res_path)
        if a and b:
            toggle=True
        else:
            print('\nAt least one of those paths was invalid. Please try again.\n')

    file_list = make_file_list(hi_res_path)

    for file in file_list:
        gimmespace()
        print("Making mp3 for: " + file)
        command = make_command(file, hi_res_path, lo_res_path)
        subprocess.call(command)

if __name__ == '__main__':
    main()

#
# WAVtoMP3.py
# Author: Jim Sam
#
# This script turns high resolution WAV files into mp3s for mobile devices.
# It is a work in progress, but it still works.
#
# It assumes you have FFMPEG installed on your system in a way that does not
# require a defined directory to launch.
#

import os
import pexpect
import subprocess
import linecache

def check_channels(file, hi_res_path):
    csv_file = hi_res_path+file+'_tech.csv'
    command = ['bwfmetaedit','--out-tech='+csv_file,hi_res_path+file+'.wav']
    subprocess.call(command)

    line2 = linecache.getline(csv_file,2)
    line2 = line2.split(',')
    channels = int(line2[4])
    os.remove(csv_file)
    return channels


def make_command(file, hi_res_path, lo_res_path):
    file = str(file)
    hi_res_path = str(hi_res_path)
    lo_res_path = str(lo_res_path)

    command = ""
    channels = check_channels(file, hi_res_path)

    if channels == 1:
        command = [ 'ffmpeg','-i',hi_res_path+file+'.wav','-write_id3v1','1',
                    '-id3v2_version','3','-dither_method','modified_e_weighted',
                    '-out_sample_rate','48k','-b:a','160k',
                    lo_res_path+file.replace('p0', 'r0')+'.mp3']
    if channels == 2:
        command = [ 'ffmpeg','-i',hi_res_path+file+'.wav','-write_id3v1','1',
                    '-id3v2_version','3','-dither_method','modified_e_weighted',
                    '-out_sample_rate','48k','-b:a','320k',
                    lo_res_path+file.replace('p0', 'r0')+'.mp3']

    return command


def make_file_list(hi_res_path):
    dir1 = os.listdir(hi_res_path)
    file_list = []

    for file in dir1:
        file_name=str(file)
        if file_name[-4:].lower() == ".wav":
            file_list.append(file_name[:-4])

    return file_list


def main():
    hi_res_path = input("The path of the high-resolution files: ")
    lo_res_path = input("The path of the low-resolution files: ")

    file_list = make_file_list(hi_res_path)

    for file in file_list:
        print("Making mp3 for: " + file)
        command = make_command(file, hi_res_path, lo_res_path)
        subprocess.call(command)

    print("Done!")

if __name__ == '__main__':
    main()

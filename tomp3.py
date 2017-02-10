'''tomp3.py turns high resolution files into mp3s.

It assumes you have FFMPEG installed on your system and path.
'''

from linecache import getline
from platform import system

import os
import re
import subprocess
import sys

valid_extensions = ['flac','wav']

def check_channels(hi_res_path, f, extension):
    real = str(os.path.join(hi_res_path, f + '.' + extension))
    new = real.replace('.', '1.')
    command = ['ffmpeg', '-i', real, new]
    try:
        output = subprocess.Popen(command, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, universal_newlines=True)
        message = output.stdout.read()
        output.stdout.close()
        os.remove(new)
    except:
        sys.exit('\r\nHey, something went wrong. Sorry about that.\r\n')

    if 'mono' in message:
        channels = 1
    else:
        channels = 2

    return channels

def make_command(hi_res_path, lo_res_path, f, extension):
    command = ""
    channels = check_channels(hi_res_path, f, extension)

    if channels == 1:
        command = ['ffmpeg','-i',
                    os.path.join(hi_res_path, f + '.' + extension),
                    '-write_id3v1', '1','-id3v2_version','3',
                    '-dither_method','modified_e_weighted',
                    '-out_sample_rate','48k','-b:a','160k',
                    os.path.join(lo_res_path, f + '.mp3')]
    if channels == 2:
        command = ['ffmpeg','-i',
                    os.path.join(hi_res_path, f + '.' + extension),
                    '-write_id3v1','1','-id3v2_version','3',
                    '-dither_method','modified_e_weighted',
                    '-out_sample_rate','48k', '-b:a','320k',
                    os.path.join(lo_res_path, f + '.mp3')]
    return command

def gimmespace():
    for i in range(5):
        print()

def make_file_list(hi_res_path, extension):
    dir1 = os.listdir(hi_res_path)
    file_list = []
    l = len(extension)*-1
    for f in dir1:
        if f[l:] == extension:
            [file_name, ext] = f.split('.')
            file_list.append(file_name)
    return file_list

def validate_path(path):
    if system() == 'Windows':
        if re.match(r'(^\w:\\$)|(^\w:\\.+\\$)', path):
            result = True

    if os.path.exists(path):
        result = True
    else:
        result = False

    return result

def get_extension():
    toggle = False
    while not toggle:
        extension = input("What is the extension of the high-resolution files? (no dot) ")
        if extension in valid_extensions:
            toggle=True
        else:
            print("\r\nSorry, that's not a valid extension.\r\n")
    return extension

def get_paths():
    toggle = False
    while not toggle:
        hi_res_path = input("The path of the high-resolution files: ")
        lo_res_path = input("The path of the low-resolution files:  ")
        a = validate_path(hi_res_path)
        b = validate_path(lo_res_path)
        if a and b:
            toggle=True
        else:
            print('\r\nAt least one of those paths was invalid. Please try again.\r\n')
    return hi_res_path, lo_res_path

def test_apps_there():
    ffmpeg = False

    # Ensure FFMPEG
    if system() == 'Darwin':
        f_command = ['ffmpeg', '-h']

        try:
            output = subprocess.Popen(f_command, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, universal_newlines=True)
            message = output.stdout.read()
            output.stdout.close()
            if 'ffmpeg version' in message:
                ffmpeg = True
        except FileNotFoundError:
            pass

    # This script does not ensure non-Mac computers has FFMPEG installed.
    else:
        ffmpeg = True

    return ffmpeg

def main():
    ffmpeg = test_apps_there()
    if not ffmpeg:
        sys.exit('Please make sure ffmpeg is installed.\r\n')

    hi_res_path, lo_res_path = get_paths()
    extension = get_extension()
    file_list = make_file_list(hi_res_path, extension)

    for f in file_list:
        gimmespace()
        print("Making mp3 for: " + f)
        command = make_command(hi_res_path, lo_res_path, f.strip(), extension.strip())
        subprocess.call(command)

    gimmespace()

if __name__ == '__main__':
    main()

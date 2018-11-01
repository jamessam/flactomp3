import os
from platform import system
import re
import subprocess
import sys


VALID_EXTENSIONS = ['flac','wav']


def main():
    proceed_if_dependencies_there()
    high_res_path, low_res_path = get_valid_high_and_low_resolution_paths()
    extension = get_extension()
    file_list = make_file_list(high_res_path, extension)
    make_mp3s(high_res_path, low_res_path, file_list, extension)


def proceed_if_dependencies_there():
    if 'ffmpeg version' not in call_subprocess(['ffmpeg','-h']):
        sys.exit('Please install FFMPEG.')


def call_subprocess(command):
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, universal_newlines=True)
        message = output.stdout
    except Exception as error:
        raise error.with_traceback(sys.exc_info()[2])
    return message


def get_valid_high_and_low_resolution_paths():
    high_res_path = get_valid_path('high')
    low_res_path = get_valid_path('low')
    return high_res_path, low_res_path


def get_valid_path(resolution):
    while True:
        path = get_input(f'The path of the {resolution}-resolution files: ')
        if validate_path(path):
            break
        print('That path is invalid. Please try again.')        
    return path


def get_input(text):
    return input(text)


def validate_path(path):
    result = True
    if not os.path.exists(path):
        result = False
    if not special_check_against_bad_windows_path_syntax(path):
        result = False
    return result


def special_check_against_bad_windows_path_syntax(path):
    result = True
    if system() == 'Windows':
        if not re.match(r'(^\w:\\$)|(^\w:\\.+$)', path):
            result = False
    return result


def get_extension():
    while True:
        extension = get_input("What is the extension of the high-resolution files? (no dot) ")
        if extension.casefold() in VALID_EXTENSIONS:
            break
        print('\r\nSorry, that\'s not a valid extension.\r\n')
    return extension


def make_file_list(hi_res_path, extension):
    files_in_dir = os.listdir(hi_res_path)
    file_list = [f for f in os.listdir(hi_res_path) if f.endswith(extension)]
    file_list.sort()
    return file_list


def make_mp3s(high_res_path, low_res_path, file_list, extension):
    for f in file_list:
        print("Making mp3 for: " + f)
        command = make_command(high_res_path, low_res_path, f.strip(), 
            extension.strip())
        call_subprocess(command)


def make_command(high_res_path, low_res_path, master_file, extension):
    mp3_file = master_file.replace(extension, 'mp3')
    full_master = os.path.join(high_res_path, master_file)
    full_mp3 = os.path.join(low_res_path, mp3_file)
    command = ['ffmpeg', '-i', full_master, 
        '-write_id3v1', '1','-id3v2_version', '3',
        '-dither_method','modified_e_weighted', 
        '-out_sample_rate','48k', '-b:a','320k', full_mp3]
    channels = check_channels(full_master)
    if channels == 1: 
        command[12]='160k'
    return command


def check_channels(master_file):
    command = ['ffmpeg', '-i', master_file]
    message = call_subprocess(command)
    if 'mono' in message:
        channels = 1
    else:
        channels = 2
    return channels
    

if __name__ == '__main__':
    main()

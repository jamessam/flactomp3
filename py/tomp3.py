import os
from platform import system
import re
import subprocess
import sys


VALID_EXTENSIONS = ['flac','wav']


class MasterFile:
    high_res_path = None
    low_res_path = None
    file_name = None
    extension = None

    def full_high_res_name(self):
        return os.path.join(self.high_res_path, self.file_name)
    
    def full_low_res_name(self):
        return os.path.join(self.low_res_path, 
            self.file_name.replace(self.extension, 'mp3'))

    def __init__(self, high_res_path=None, low_res_path=None, 
        file_name=None, extension=None):
        self.high_res_path = high_res_path.strip()
        self.low_res_path = low_res_path.strip()
        self.file_name = file_name.strip()
        self.extension = extension.strip()


def main():
    proceed_if_dependencies_there()
    high_res_path = get_valid_path('high')
    low_res_path = get_valid_path('low')
    extension = get_extension()
    file_list = make_file_list(high_res_path, low_res_path, extension)
    make_mp3s(file_list)


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


def make_file_list(high_res_path, low_res_path, extension):
    files_in_dir = os.listdir(high_res_path)
    file_list = []
    for f in os.listdir(high_res_path):
        if not f.endswith(extension):
            continue
        master_file = MasterFile(high_res_path=high_res_path, 
            low_res_path=low_res_path, file_name=f, extension=extension)
        file_list.append(master_file)
    file_list.sort(key = lambda x: x.file_name)
    return file_list


def make_mp3s(file_list):
    for master_file in file_list:
        print("Making mp3 for: " + master_file.file_name)
        command = make_command(master_file)
        call_subprocess(command)


def make_command(master_file):
    command = ['ffmpeg', '-i', master_file.full_high_res_name(), 
        '-write_id3v1', '1','-id3v2_version', '3',
        '-dither_method','modified_e_weighted', 
        '-out_sample_rate','48k', '-b:a','320k', 
        master_file.full_low_res_name()]
    channels = check_channels(master_file.full_high_res_name())
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

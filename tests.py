import os
import subprocess
from platform import system
from unittest import main, TestCase

from tomp3 import check_channels, make_file_list, test_apps_there, validate_path


class SystemTests(TestCase):
    def test_system_for_apps(self):
        f, b = test_apps_there()
        self.assertTrue(f)
        self.assertTrue(b)

class UnitTestsForFunctions(TestCase):
    folder_exists = False
    testing_path = 'testing'

    throwaway = os.path.join(testing_path, 'throwaway.txt')
    mp3c = os.path.join(testing_path, 'c.mp3')
    mp3d = os.path.join(testing_path, 'd.mp3')
    wav1 = os.path.join(testing_path, '1.wav')
    wav2 = os.path.join(testing_path, '2.wav')
    flac = os.path.join(testing_path, 'yo.flac')

    def setUp(self):
        if os.path.exists(self.testing_path):
            self.folder_exists = True
        else:
            os.mkdir(self.testing_path)

        command = ['ffmpeg', '-f', 'lavfi', '-i' ,'sine=frequency=1000:duration=5']
        if not os.path.exists(self.throwaway):
            throw = open(self.throwaway, 'w')
            throw.write('Test file. Please delete this file if you find it.')
            throw.close()
        if not os.path.exists(self.mp3c):
            command.append(self.mp3c)
            subprocess.call(command)
            del command[5]
        if not os.path.exists(self.mp3d):
            command.append(self.mp3d)
            subprocess.call(command)
            del command[5]
        if not os.path.exists(self.wav1):
            command.append(self.wav1)
            subprocess.call(command)
            del command[5]
        if not os.path.exists(self.wav2):
            command.append(self.wav2)
            subprocess.call(command)
            del command[5]
        if not os.path.exists(self.flac):
            command.append(self.flac)
            subprocess.call(command)
            del command[5]

    def tearDown(self):
        os.remove(self.throwaway)
        os.remove(self.mp3c)
        os.remove(self.mp3d)
        os.remove(self.wav1)
        os.remove(self.wav2)
        os.remove(self.flac)

        if not self.folder_exists:
            os.rmdir(self.testing_path)

    def test_check_channels(self):
        flac_channels = check_channels(self.testing_path, 'yo', 'flac')
        wav_channels = check_channels(self.testing_path, '1', 'wav')
        self.assertEqual(flac_channels, 1)
        self.assertEqual(wav_channels, 1)

    def test_path_validation(self):
        if system() == "Windows":
            path1 = 'c:\\'
            path2 = 'c:'
        elif system() == "Darwin":
            path1 = '/users/'
            path2 = '/users/fake/path'
        else:
            pass

        self.assertTrue(validate_path(path1))
        self.assertFalse(validate_path(path2))

    def test_file_list(self):
        file_list = make_file_list(self.testing_path, 'wav')
        should = ['1', '2']
        self.assertEqual(file_list, should)

        file_list = make_file_list(self.testing_path, 'flac')
        should = ['yo']
        self.assertEqual(file_list, should)

main()

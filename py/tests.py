import os
from platform import system
from unittest import main, TestCase
from unittest.mock import patch

from tomp3 import (
    call_subprocess, check_channels, get_extension, get_valid_path, 
    make_command, make_file_list, validate_path
)


def create_sound_file_if_not_there(file):
    command = ['ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=1000:duration=5']
    if not os.path.exists(file):
        command.append(file)
        call_subprocess(command)


class UnitTestsForFunctions(TestCase):
    def test_call_subprocess(self):
        message = str(call_subprocess(['ls']))
        self.assertIn('tests.py', message)
        self.assertIn('tomp3.py', message)

    # Note: these next two tests only confirms successful calls. 
    # Bad calls will trigger an infinite loop.
    @patch('tomp3.get_input', return_value='/usr/')
    def test_get_valid_path(self, input):
        if system() != 'Windows':
            self.assertEqual('/usr/', get_valid_path('high'))

    @patch('tomp3.get_input', return_value='flac')
    def test_get_extension(self, input):
        self.assertEqual(get_extension(), 'flac')

    def test_validate_path(self):
        if system() == 'Windows':
            path1 = 'c:\\'
            path2 = 'c:'
        elif system() == 'Darwin':
            path1 = '/users/'
            path2 = '/users/fake/path'
        else:
            path1 = '/usr/'
            path2 = '/users/fake/path'
        self.assertTrue(validate_path(path1))
        self.assertFalse(validate_path(path2))
    
    def test_make_file_list(self):
        file_list = make_file_list(os.getcwd(), 'testing', 'mp3')
        self.assertEqual([], file_list)
        file_list = make_file_list(os.getcwd(), 'testing', 'md')
        self.assertEqual([], file_list)
        mf1 = {
            'high_res_path': os.getcwd(), 'low_res_path': 'testing',
            'file_name': 'tests.py', 'extension': 'py'
        }
        mf2 = {
            'high_res_path': os.getcwd(), 'low_res_path': 'testing',
            'file_name': 'tomp3.py', 'extension': 'py'
        }
        file_list = make_file_list(os.getcwd(), 'testing', 'py')
        self.assertEqual(mf1['extension'], 'py')
        self.assertEqual(mf1['file_name'], file_list[0]['file_name'])
        self.assertEqual(mf2['extension'], 'py')
        self.assertEqual(mf2['file_name'], file_list[1]['file_name'])


class UnitTestsForFunctionsWhereSoundFileIsRequired(TestCase):
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

        if not os.path.exists(self.throwaway):
            throw = open(self.throwaway, 'w')
            throw.write('Test file. Please delete this file if you find it.')
            throw.close()
        create_sound_file_if_not_there(self.mp3c)
        create_sound_file_if_not_there(self.mp3d)
        create_sound_file_if_not_there(self.wav1)
        create_sound_file_if_not_there(self.wav2)
        create_sound_file_if_not_there(self.flac)

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
        test1 = os.path.join(self.testing_path, 'yo.flac')
        test2 = os.path.join(self.testing_path, '1.wav')
        flac_channels = check_channels(test1)
        wav_channels = check_channels(test2)
        self.assertEqual(flac_channels, 1)
        self.assertEqual(wav_channels, 1)

    def test_make_command(self):
        master_file = {
            'high_res_path': 'testing', 'low_res_path': 'testing', 
            'file_name': '1.wav', 'extension': 'wav',
            'full_high_res_name': 'testing/1.wav',
            'full_low_res_name': 'testing/1.mp3'
        }
        expected = ['ffmpeg','-i', 'testing/1.wav',
                    '-write_id3v1', '1','-id3v2_version','3',
                    '-dither_method','modified_e_weighted',
                    '-out_sample_rate','48k','-b:a','160k', 'testing/1.mp3']
        tested = make_command(master_file)
        self.assertEqual(expected, tested)


main()

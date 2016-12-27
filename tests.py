from unittest import main, TestCase
from tomp3 import test_apps_there, validate_path
from platform import system

class SystemTests(TestCase):
    def test_system_for_apps(self):
        f, b = test_apps_there()
        self.assertTrue(f)
        self.assertTrue(b)

class UnitTests(TestCase):
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
        if not os.path.exists(self.mp3c):
            pass
        if not os.path.exists(self.mp3d):
            pass
        if not os.path.exists(self.wav1):
            pass
        if not os.path.exists(self.wav2):
            pass
        if not os.path.exists(self.flac):
            pass

    def tearDown(self):
        os.remove(self.throwaway)

        if not self.folder_exists:
            os.rmdir(self.testing_path)

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
        pass

main()

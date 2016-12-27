from unittest import main, TestCase
from tomp3 import test_apps_there, validate_path
from platform import system

class SystemTests(TestCase):
    def test_system_for_apps(self):
        f, b = test_apps_there()
        self.assertTrue(f)
        self.assertTrue(b)

class UnitTests(TestCase):
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

main()

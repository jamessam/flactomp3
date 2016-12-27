from unittest import main, TestCase
from tomp3 import validate_path
from platform import system

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

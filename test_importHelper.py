from ImportHelper import ImportHelper
import unittest


class TestImportHelper(unittest.TestCase):
    def test_import_helper(self):
        singleton1 = ImportHelper(verbose=True)
        singleton2 = ImportHelper(verbose=True)
        self.assertTrue(singleton1 is singleton2)

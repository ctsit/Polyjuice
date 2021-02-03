import unittest

import os
import os.path
from poly_juice.polyjuice import zip_folder
from poly_juice.lumberjack import Lumberjack


class TestZipFolder(unittest.TestCase):
    """
    This test makes sure that the processed folders are successfully zipped.
    """

    def setUp(self):
        self.directory = os.path.dirname('tests/testOutput/')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def test_zips(self):
        dicom_folders = ['tests/testInput/MRI/101_01_01_2010']
        zip_dir = 'tests/testOutput'
        log = Lumberjack()

        zip_folder(dicom_folders, zip_dir, log)
        result = check_zipped_folder()

        self.assertTrue(result)

    def tearDown(self):
        os.remove('tests/testOutput/101_01_01_2010.zip')
        print("Successfully removed tests/testOutput/101_01_01_2010.zip")


def check_zipped_folder() -> bool:
    existing = os.path.exists("tests/testOutput/101_01_01_2010.zip")
    return existing


if __name__ == "__main__":
    unittest.main()

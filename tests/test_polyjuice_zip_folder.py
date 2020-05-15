import unittest

import os
import os.path
from poly_juice.polyjuice import zip_folder
from poly_juice.lumberjack import Lumberjack


class TestZipFolder(unittest.TestCase):

    def test_zips(self):
        dicom_folders = ['tests/testOutput/mri', 'tests/testOutput/pet']
        zip_dir = 'tests/testOutput'
        log = Lumberjack()

        zip_folder(dicom_folders, zip_dir, log)
        result = check_zipped_folder()

        self.assertTrue(result)

    def tearDown(self):
        # delete the new zip file from tests/test_output
        os.remove('tests/testOutput/mri.zip')
        os.remove('tests/testOutput/pet.zip')
        print("tearDown was successful, ready for next test round.")


def check_zipped_folder() -> bool:
    # checks to see if zip_folder placed a zip file where expected
    existing = os.path.exists("tests/testOutput/mri.zip")
    return existing


if __name__ == "__main__":
    unittest.main()

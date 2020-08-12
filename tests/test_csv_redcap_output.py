# This series of tests checks the functionality of dicom_tools/headers_to_csv_redcap.py

import unittest

import os
import os.path
from dicom_tools.headers_to_csv_redcap import make_csv
from dicom_tools.headers_to_csv_redcap import read_files


class TestRedcapOutput(unittest.TestCase):

    def setUp(self):
        self.directory = os.path.dirname('tests/testOutput/')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        self.mri = os.path.dirname('tests/testOutput/mri/')
        self.pet = os.path.dirname('tests/testOutput/pet/')
        if not os.path.exists(self.mri):
            os.makedirs(self.mri)
        if not os.path.exists(self.pet):
            os.makedirs(self.pet)

    def test_read_files(self):
        pass

    def test_make_csv(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()

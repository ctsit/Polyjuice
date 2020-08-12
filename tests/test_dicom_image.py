# These tests examine polyjuice's functionality for grabbing an ids.csv file and updating PatientID header info if there is a match within the file

import unittest

import os
import os.path
from poly_juice import dicom_image


class TestDicomImage(unittest.TestCase):

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

    def test_modify_item(self):
        pass

    def test_get_value(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()

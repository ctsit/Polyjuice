# These tests examine polyjuice's check_directory and identify_output functions to make sure that the correct information is used to create the destination folder for processed images

import unittest

import os
import os.path
from poly_juice.polyjuice import check_directory
from poly_juice.polyjuice import identify_output


class TestPolyjuiceOutput(unittest.TestCase):

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

    def test_check_directory(self):
        pass

    def test_identify_output(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()

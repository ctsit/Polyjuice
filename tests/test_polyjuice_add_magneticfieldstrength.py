# These tests determine whether polyjuice is successfully updating empty MagneticFieldStrength header info

import unittest

import os
import os.path
from poly_juice.polyjuice import check_mag_field


class TestConsistentMagneticFieldStrength(unittest.TestCase):

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

    def test_mag_field(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()

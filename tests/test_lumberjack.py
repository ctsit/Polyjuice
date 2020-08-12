# These tests examine lumberjack.py

import unittest

import os
import os.path
from poly_juice import lumberjack


class TestLumberjack(unittest.TestCase):

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

    def test_logging(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()

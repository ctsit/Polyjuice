

import unittest

import os
import os.path
import shutil
from poly_juice.polyjuice import walk_directory
from poly_juice.polyjuice import check_directory
from poly_juice.polyjuice import identify_output
from poly_juice.filch import DicomCaretaker
from poly_juice.lumberjack import Lumberjack


class TestPolyjuiceOutput(unittest.TestCase):
    """
    These tests examine polyjuice's check_directory and identify_output
    functions. They check that the correct information is used to create a
    destination folder for processed images.
    """
    def setUp(self):
        self.directory = os.path.dirname('tests/testOutput/')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def test_walk_directory(self):
        parent_file = 'tests/testInput'
        out_dir = 'tests/testOutput/test_directory'
        zip_dir = ''
        modifications = {'PatientName': 'Anonymous'}
        id_pairs = {'': ''}
        dicom_folders = []
        log = Lumberjack()

        # expects to find 1 folder in pet and 2 folders in mri
        # each mri folder has 2 files
        expected = ['tests/testOutput/test_directory/103_01_01_2010',
                    'tests/testOutput/test_directory/101_01_01_2010',
                    'tests/testOutput/test_directory/102_01_01_2010']

        result = walk_directory(parent_file, out_dir, zip_dir, modifications,
                                id_pairs, dicom_folders, log)

        self.assertEqual(expected, result)

    def test_check_directory(self):
        check_directory('tests/testOutput/test_directory')

        result = os.path.exists('tests/testOutput/test_directory')
        self.assertTrue(result)

    def test_identify_output(self):
        editor = DicomCaretaker()
        working_file = 'tests/testInput/MRI/101_01_01_2010/1'
        out_dir = 'tests/testOutput'
        id_pairs = {'': ''}
        log = Lumberjack()

        expected = 'tests/testOutput/101_01_01_2010/1'
        result = identify_output(editor, working_file, out_dir, id_pairs, log)

        self.assertEqual(expected, result)

    def tearDown(self):
        if os.path.exists('tests/testOutput/test_directory'):
            shutil.rmtree('tests/testOutput/test_directory')
            print("Successfully removed tests/testOutput/test_directory")


if __name__ == "__main__":
    unittest.main()

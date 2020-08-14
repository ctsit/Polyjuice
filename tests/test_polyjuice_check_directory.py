

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
    These tests examine polyjuice's check_directory and identify_output functions to make sure that the correct information is used to create a destination folder for processed images
    """
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

    def test_walk_directory(self):
        # collects a list of folders within the directory (used for zipping these folders in the output directory at the end)
        parent_file = 'tests/testInput'
        out_dir = 'tests/testOutput/test_directory'
        zip_dir = ''
        modifications = {'PatientName': 'Anonymous'}
        id_pairs = {'': ''}
        dicom_folders = []
        log = Lumberjack()

        # expects to find 1 folder in pet and 2 folders in mri (and each mri folder has 2 files)
        expected = ['tests/testOutput/test_directory/103_01_01_2010', 'tests/testOutput/test_directory/101_01_01_2010', 'tests/testOutput/test_directory/102_01_01_2010']

        result = walk_directory(parent_file, out_dir, zip_dir, modifications, id_pairs, dicom_folders, log)

        self.assertEqual(expected, result)

    def test_check_directory(self):
        check_directory('tests/testOutput/test_directory')

        result = os.path.exists('tests/testOutput/test_directory')
        self.assertTrue(result)

    def test_identify_output(self):
        editor = DicomCaretaker()
        working_file = 'tests/testInput/MRI/101_01_01_2010/1'
        out_dir = 'tests/testOutput/MRI'
        id_pairs = {'': ''}
        log = Lumberjack()

        expected = 'tests/testOutput/MRI/101_01_01_2010/1'
        result = identify_output(editor, working_file, out_dir, id_pairs, log)

        self.assertEqual(expected, result)

    def tearDown(self):
        if os.path.exists('tests/testOutput/test_directory'):
            shutil.rmtree('tests/testOutput/test_directory')
            print("tearDown was successful, ready for next test round.")


if __name__ == "__main__":
    unittest.main()

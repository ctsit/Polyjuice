import unittest

import os
import os.path
import shutil
from poly_juice.polyjuice import clean_files
from poly_juice.filch import DicomCaretaker
from poly_juice.lumberjack import Lumberjack
from poly_juice.dicom_image import DicomImage


class TestDicomImage(unittest.TestCase):
    """
    These tests examine polyjuice's functionality for collecting and updating PatientID header info if there is a match within the file
    """

    def setUp(self):
        self.editor = DicomCaretaker()
        self.working_file = 'tests/testInput/MRI/102_01_01_2010/1'
        self.out_dir = 'tests/testOutput/'
        self.modifications = make_config()
        self.id_pairs = {'PATIENT_ID': 'UPDATE_ID'}
        self.dicom_folders = ['tests/testOutput/mri', 'tests/testOutput/pet']
        self.log = Lumberjack()

        self.directory = os.path.dirname('tests/testOutput/')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        # generate an output file so that we aren't editing the template
        self.output = os.path.dirname('tests/testOutput/102_01_01_2010/1')
        if not os.path.exists(self.output):
            os.makedirs('tests/testOutput/102_01_01_2010/')
            clean_files(self.editor, self.working_file, self.out_dir, self.working_file, self.modifications, self.id_pairs, self.dicom_folders, self.log)

    def test_get_value(self):
        dcm_file = 'tests/testOutput/102_01_01_2010/1'
        with open(dcm_file, 'rb') as working_file:
            test_image = DicomImage(working_file)
            key = 'ManufacturerModelName'

            expected = 'MODEL'
            result = test_image.get_value(key)

        self.assertEqual(expected, result)

    def test_modify_item(self):
        dcm_file = 'tests/testOutput/102_01_01_2010/1'
        with open(dcm_file, 'rb') as working_file:
            test_image = DicomImage(working_file)
            key = 'Manufacturer'
            delete = False

            expected = 'TestValue'
            test_image.modify_item(key, expected, delete)
            # save the edited image in the output folder

            result = test_image.get_value(key)

        self.assertEqual(expected, result)
        pass

    def test_update_patient_id(self):
        id_update = {'102': '202'}
        dcm_file = 'tests/testInput/MRI/102_01_01_2010/1'
        with open(dcm_file, 'rb') as working_file:
            test_image = DicomImage(working_file)

            expected = '202'
            test_image.update_patient_id(id_update, self.log)
            result = test_image.get_patient_id()

        self.assertEqual(expected, result)

    def tearDown(self):
        shutil.rmtree('tests/testOutput/102_01_01_2010')


def make_config() -> dict:
    modifications = {
        # Commented terms should be skipped by clean_files
        # 'StudyDate': '',
        # 'Manufacturer': '',
        # 'SeriesDescription': '',
        # 'ManufacturersModelName': '',
        # 'PatientID': '',
        # 'StudyInstanceUID': '',
        # 'SeriesInstanceUID': '',
        # 'InstanceNumber': '',
        'ReferringPhysicianName': '',
        'PatientName': 'Anonymous',
        'PatientBirthDate': '19010101',
        # 'MagneticFieldStrength': '',
    }
    return modifications


if __name__ == "__main__":
    unittest.main()

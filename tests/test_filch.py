# These tests examine filch.py. One thing to keep in mind while testing filch is that a lot of these functions appear within polyjuice itself and are used as part of test_polyjuice_clean_mris.py

import unittest

import os
import os.path
from poly_juice.filch import DicomCaretaker
from poly_juice.polyjuice import clean_files
from poly_juice.dicom_image import DicomImage
from poly_juice.lumberjack import Lumberjack


class Flags():
    CONFIG_PATH = '<config_file>'
    INPUT_DIR = '<input_path>'
    OUTPUT_DIR = '<output_path>'
    _verbose = '--verbose'
    _zip_folder = '--zip'
    _use_config = '--config'


class TestFilch(unittest.TestCase):

    def setUp(self):

        self.args = Flags()
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

        # if there is no output file to play with, generate one
        self.output = os.path.dirname('tests/testOutput/102_01_01_2010/1')
        if not os.path.exists(self.output):
            os.makedirs('tests/testOutput/102_01_01_2010/')
            clean_files(self.editor, self.working_file, self.out_dir, self.working_file, self.modifications, self.id_pairs, self.dicom_folders, self.log)

    def test_mount_iso(self):
        # result = DicomCaretaker.mount_iso(iso_path, out)
        # returns mount_point
        pass

    def test_scrub(self):
        # this test is run more comprehensively in test_polyjuice_clean_mris.py . do i want to keep it in anyway, for the sake of showing that i'm testing each filch function?
        dcm_image = 'tests/testOutput/102_01_01_2010/1'
        editor = DicomCaretaker()

        # editor.scrub(image, modifications, id_pairs, log)
        # result = check output file values

        # self.assertEqual(expected, result)
        pass

    def test_report_id(self):
        # it looks like this function creates a csv file with a list of ids with "issues". what constitutes an issue seems to be not working properly, because polyjuice frequently prints this file with a list of just ids that were processed that didn't happen to be in the ids.csv file.
        # actually i'm not sure what it's even trying to report here- if there's a "Missing ID" then the output folder can't be created and there's an error anyway?
        dcm_image = 'tests/testOutput/102_01_01_2010/1'
        editor = DicomCaretaker()

        # editor.report_id(id_issue, log)
        # result = check self.unknown_ids (a list within DicomCaretaker)
        # self.assertEqual(expected, result)
        pass

    def test_get_folder_name(self):
        # this function collects the output folder's name by finding and properly formatting a string made out of the patient's id and study date, using the dicom's header info
        dcm_image = 'tests/testOutput/102_01_01_2010/1'
        editor = DicomCaretaker()
        expected = '102_01_01_2010'

        with open(dcm_image, 'rb') as working_file:
            test_image = DicomImage(working_file)
            result = editor.get_folder_name(test_image)

        self.assertEqual(expected, result)

    def test_save_output(self):
        dcm_image = 'tests/testOutput/102_01_01_2010/1'
        editor = DicomCaretaker()

        # editor.save_output(image, identified_folder, filename)
        # result = check to see if the folder is there
        # self.assertEqual(expected, result)
        pass

    def test_unmount_iso(self):
        # DicomCaretacker.unmount_iso()
        # result = see if the iso is unmounted? not sure if i can easily test these iso functions
        pass

    def tearDown(self):
        pass


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

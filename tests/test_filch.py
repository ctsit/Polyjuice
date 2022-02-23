import unittest

import os
import os.path
import shutil
from pydicom import dcmread
from poly_juice.filch import DicomCaretaker
from poly_juice.polyjuice import clean_files
from poly_juice.polyjuice import check_directory
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
    '''
    These tests examine filch.py. One thing to keep in mind while testing filch
    is that a lot of these functions appear within polyjuice itself and are
    used as part of test_polyjuice_clean_mris.py
    '''
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
            clean_files(self.editor, self.working_file, self.out_dir,
                        self.working_file, self.modifications, self.id_pairs,
                        self.dicom_folders, self.log)

    @unittest.skip("Unsure what mount_iso does or if it has something to test")
    def test_mount_iso(self):
        # result = DicomCaretaker.mount_iso(iso_path, out)
        # returns mount_point
        pass

    @unittest.skip("This function is also tested in test_polyjuice_clean_mris.py, within a larger function")
    def test_scrub(self):
        dcm_image = 'tests/testOutput/102_01_01_2010/1'
        editor = DicomCaretaker()
        log = Lumberjack()
        modifications = make_config()
        expected = modifications
        id_pairs = {'': ''}

        with open(dcm_image, 'rb') as working_file:
            test_image = DicomImage(working_file)
            editor.scrub(test_image, modifications, id_pairs, log)

        ds = dcmread(dcm_image)
        data = get_output_results(ds)
        result = dict(data)

        self.assertDictEqual(expected, result)

    @unittest.skip("Unsure what report_id actually reports- it's not IDs that are missing, because it reports IDs that are not missing, and also files that are missing IDs are skipped with an error.")
    def test_report_id(self):
        # dcm_image = 'tests/testOutput/102_01_01_2010/1'
        # editor = DicomCaretaker()

        # editor.report_id(id_issue, log)
        # result = check self.unknown_ids (a list within DicomCaretaker)
        # self.assertEqual(expected, result)
        pass

    def test_get_folder_name(self):
        ''' This function collects the output folder's name by finding and
        properly formatting a string made out of the patient's ID and study
        date, using the dicom's header info.
        '''
        dcm_image = 'tests/testOutput/102_01_01_2010/1'
        editor = DicomCaretaker()
        expected = '102_01_01_2010'

        with open(dcm_image, 'rb') as working_file:
            test_image = DicomImage(working_file)
            result = editor.get_folder_name(test_image)

        self.assertEqual(expected, result)

    def test_validate_folder_name(self):
        # This function tests the validity of the name of the dicom folder
        folder = '320001-01_02032022'
        editor = DicomCaretaker()
        result = editor.validate_folder_name(folder)

        self.assertTrue(result)

    def validate_ptid(self):
        # This function tests the validity of a ptid
        ptid1 = '320001'
        ptid2 = '320001-09'
        ptid3 = '3200019'
        editor = DicomCaretaker()

        expected = [True, True, False]
        output = []
        output.append(editor.validate_ptid(ptid1))
        output.append(editor.validate_ptid(ptid2))
        output.append(editor.validate_ptid(ptid3))

        self.assertEqual(expected, output)

    def test_save_output(self):
        dcm_image = 'tests/testOutput/102_01_01_2010/1'
        editor = DicomCaretaker()
        output_folder = 'tests/testOutput/test_save_output'
        filename = '1'

        with open(dcm_image, 'rb') as working_file:
            test_image = DicomImage(working_file)
            check_directory(output_folder)
            editor.save_output(test_image, output_folder, filename)

            result = os.path.exists('tests/testOutput/test_save_output/1')

        self.assertTrue(result)

    @unittest.skip("Not sure if these iso functions can easily be tested- placeholder for future.")
    def test_unmount_iso(self):
        # DicomCaretacker.unmount_iso()
        # result = see if the iso is unmounted?
        pass

    def tearDown(self):
        if os.path.exists('tests/testOutput/test_save_output'):
            shutil.rmtree('tests/testOutput/test_save_output')
            print("Successfully deleted testOutput/test_save_output")

    @classmethod
    def tearDownClass(self):
        if os.path.exists('tests/testOutput/102_01_01_2010'):
            shutil.rmtree('tests/testOutput/102_01_01_2010')
            print("Successfully deleted testOutput/102_01_01_2010")


def make_config() -> dict:
    modifications = {
        'ReferringPhysicianName': '',
        'PatientName': 'Anonymous',
        'PatientBirthDate': '19010101',
    }
    return modifications


def get_output_results(ds):
    return (
            ["ReferringPhysicianName", ds.get("ReferringPhysicianName", "Value")],
            ["PatientName", ds.get("PatientName", "Value")],
            ["PatientBirthDate", ds.get("PatientBirthDate", "Value")],
        )


if __name__ == "__main__":
    unittest.main()

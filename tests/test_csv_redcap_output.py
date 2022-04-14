import unittest

import csv
import os
import os.path
from dicom_tools.headers_to_csv_redcap import read_files


class TestRedcapOutput(unittest.TestCase):
    """
    This series of tests checks the functionality of
    dicom_tools/headers_to_csv_redcap.py
    """

    def test_read_mri(self):
        dcm_file = 'tests/testInput/MRI/101_01_01_2010/1'
        expected = {
            'ptid': '101',
            'redcap_event_name': 'initial_visit_year_arm_1',
            'image_type___1': '1',
            'image_type___2': '0',
            'img_mri_patient_name': 'PATIENT',
            'img_mri_patient_id': '101',
            'img_mri_date': '20100101',
            'img_mri_study_descrip': 'Average DC',
            'img_mri_modality': 'MR',
            'img_mri_ref_physician': 'REFPHYS',
            'img_mri_inst': 'Anonymous Hospital',
            'img_mri_site': 'MSMC',
            'img_pet_tracer': '',
            'img_pet_patient_name': '',
            'img_pet_patient_id': '',
            'img_pet_date': '',
            'img_pet_study_descrip': '',
            'img_pet_modality': '',
            'img_pet_ref_physician': '',
            'img_pet_inst': '',
            'img_pet_site': '',
            'imaging_metadata_complete': '2'
            }

        fieldnames = make_fieldnames()
        output_csv = 'tests/testOutput/output.csv'
        with open(output_csv, 'w+', newline='') as output:
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            read_files(dcm_file, writer)

        with open(output_csv, 'r', newline='') as test_input:
            reader = csv.DictReader(test_input)
            for row in reader:
                result = collect_results(row)

        self.assertEqual(expected, result)

    def test_read_pet(self):
        dcm_file = 'tests/testInput/PET/103_01_01_2010/10402932'
        expected = {
            'ptid': '103',
            'redcap_event_name': 'initial_visit_year_arm_1',
            'image_type___1': '0',
            'image_type___2': '1',
            'img_mri_patient_name': '',
            'img_mri_patient_id': '',
            'img_mri_date': '',
            'img_mri_study_descrip': '',
            'img_mri_modality': '',
            'img_mri_ref_physician': '',
            'img_mri_inst': '',
            'img_mri_site': '',
            'img_pet_tracer': '',
            'img_pet_patient_name': 'PATIENT2',
            'img_pet_patient_id': '103',
            'img_pet_date': '20100101',
            'img_pet_study_descrip': 'JELLO',
            'img_pet_modality': 'CT',
            'img_pet_ref_physician': 'REFPHY',
            'img_pet_inst': 'INST',
            'img_pet_site': 'MSMC',
            'imaging_metadata_complete': '2'
            }

        fieldnames = make_fieldnames()
        output_csv = 'tests/testOutput/output.csv'
        with open(output_csv, 'w+', newline='') as output:
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            read_files(dcm_file, writer)

        with open(output_csv, 'r', newline='') as test_input:
            reader = csv.DictReader(test_input)
            for row in reader:
                result = collect_results(row)

        self.assertEqual(expected, result)

    def tearDown(self):
        os.remove('tests/testOutput/output.csv')
        print("Successfully removed tests/testOutput/output.csv")


def make_fieldnames():
    return ['ptid',
            'redcap_event_name',
            'image_type___1',
            'image_type___2',
            'img_mri_patient_name',
            'img_mri_patient_id',
            'img_mri_date',
            'img_mri_study_descrip',
            'img_mri_modality',
            'img_mri_ref_physician',
            'img_mri_inst',
            'img_mri_site',
            'img_pet_tracer',
            'img_pet_patient_name',
            'img_pet_patient_id',
            'img_pet_date',
            'img_pet_study_descrip',
            'img_pet_modality',
            'img_pet_ref_physician',
            'img_pet_inst',
            'img_pet_site',
            'imaging_metadata_complete'
            ]


def collect_results(row):
    result = {}

    result['ptid'] = row['ptid']
    result['redcap_event_name'] = row['redcap_event_name']
    result['image_type___1'] = row['image_type___1']
    result['image_type___2'] = row['image_type___2']
    result['img_mri_patient_name'] = row['img_mri_patient_name']
    result['img_mri_patient_id'] = row['img_mri_patient_id']
    result['img_mri_date'] = row['img_mri_date']
    result['img_mri_study_descrip'] = row['img_mri_study_descrip']
    result['img_mri_modality'] = row['img_mri_modality']
    result['img_mri_ref_physician'] = row['img_mri_ref_physician']
    result['img_mri_inst'] = row['img_mri_inst']
    result['img_mri_site'] = row['img_mri_site']
    result['img_pet_tracer'] = row['img_pet_tracer']
    result['img_pet_patient_name'] = row['img_pet_patient_name']
    result['img_pet_patient_id'] = row['img_pet_patient_id']
    result['img_pet_date'] = row['img_pet_date']
    result['img_pet_study_descrip'] = row['img_pet_study_descrip']
    result['img_pet_modality'] = row['img_pet_modality']
    result['img_pet_ref_physician'] = row['img_pet_ref_physician']
    result['img_pet_inst'] = row['img_pet_inst']
    result['img_pet_site'] = row['img_pet_site']
    result['imaging_metadata_complete'] = row['imaging_metadata_complete']

    return result


if __name__ == "__main__":
    unittest.main()

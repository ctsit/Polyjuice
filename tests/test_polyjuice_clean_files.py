import unittest

import os
import os.path
import pydicom
from pydicom import dcmread
from polyjuice.polyjuice import clean_files
from polyjuice.lumberjack import Lumberjack
from polyjuice.filch import DicomCaretaker


class Flags():
    CONFIG_PATH = '<config_file>'
    INPUT_DIR = '<input_path>'
    OUTPUT_DIR = '<output_path>'
    _verbose = '--verbose'
    _zip_folder = '--zip'
    _use_config = '--config'


class TestFileCleaner(unittest.TestCase):
    """
    These tests check that Polyjuice cleans the correct headers and
    leaves the fields required by NACC intact.
    """

    def setUp(self):
        self.args = Flags()
        self.editor = DicomCaretaker()
        self.working_file = 'tests/testInput/mri/101_01_01_2010/1'
        self.out_dir = 'tests/testOutput/'
        self.modifications = make_config()
        self.id_pairs = {'PATIENT_ID': 'UPDATE_ID'}
        self.dicom_folders = ['tests/testOutput/mri', 'tests/testOutput/pet']
        self.log = Lumberjack()

    def test_for_cleaned_file(self):

        expected = self.modifications

        clean_files(self.editor, self.working_file, self.out_dir, self.modifications, self.id_pairs, self.dicom_folders, self.log)

        if os.path.isfile('tests/testOutput/101_01_01_2010/1'):
            output_file = 'tests/testOutput/101_01_01_2010/1'
        else:
            print("Output file not created.")
            pass

        ds = dcmread(output_file)
        data = get_output_results(ds)
        result = dict(data)

        self.assertDictEqual(expected, result)

    def test_for_intact_fields(self):
        expected = {
            'PatientID': '101',
            'Manufacturer': 'MAN',
            'ManufacturerModelName': 'MODEL',
            'StudyInstanceUID': '1.2.840.113845.11.1000000001874101095',
            'StudyDate': '20100101',
            'SeriesInstanceUID': '1.2.840.113619.2.244.6945.200138',
            'MagneticFieldStrength': pydicom.valuerep.DSfloat(3)
            }

        clean_files(self.editor, self.working_file, self.out_dir, self.modifications, self.id_pairs, self.dicom_folders, self.log)

        if os.path.isfile('tests/testOutput/101_01_01_2010/1'):
            output_file = 'tests/testOutput/101_01_01_2010/1'
        else:
            print("Output file not created.")
            pass

        ds = dcmread(output_file)
        data = get_intact_results(ds)
        result = dict(data)

        self.assertDictEqual(expected, result)


def make_config() -> dict:
    modifications = {
        # Commented terms should be skipped by clean_files
        'AccessionNumber': '',
        'InstitutionName': '',
        'ReferringPhysicianName': '',
        'StationName': '',
        'StudyDescription': '',
        'SeriesDescription': '',
        'InstanceNumber': '',
        'OperatorsName': '',
        'PatientName': "Anonymous",
        # 'PatientID': '',
        'PatientBirthDate': "19010101",
        'PatientSex': '',
        'PatientAge': '',
        'PatientWeight': '',
        # 'Manufacturer': '',
        # 'ManufacturersModelName': '',
        'EthnicGroup': '',
        'AdditionalPatientHistory': '',
        'DeviceSerialNumber': '',
        'ProtocolName': '',
        # 'StudyInstanceUID': '',
        # 'StudyDate': '',
        # 'SeriesInstanceUID': '',
        # 'MagneticFieldStrength': '',
        'StudyID': '',
        'FrameOfReferenceUID': '',
    }
    return modifications


def get_output_results(ds):
    return (
            ["AccessionNumber", ds.get("AccessionNumber", "Value")],
            ["InstitutionName", ds.get("InstitutionName", "Value")],
            ["ReferringPhysicianName", ds.get("ReferringPhysicianName", "Value")],
            ["StationName", ds.get("StationName", "Value")],
            ["StudyDescription", ds.get("StudyDescription", "Value")],
            ["SeriesDescription", ds.get("SeriesDescription", "Value")],
            ["InstanceNumber", ds.get("InstanceNumber", "Value")],
            ["OperatorsName", ds.get("OperatorsName", "Value")],
            ["PatientName", ds.get("PatientName", "Value")],
            ["PatientBirthDate", ds.get("PatientBirthDate", "Value")],
            ["PatientSex", ds.get("PatientSex", "Value")],
            ["PatientAge", ds.get("PatientAge", "Value")],
            ["PatientWeight", ds.get("PatientWeight", "Value")],
            ["EthnicGroup", ds.get("EthnicGroup", "Value")],
            ["AdditionalPatientHistory", ds.get("AdditionalPatientHistory", "Value")],
            ["DeviceSerialNumber", ds.get("DeviceSerialNumber", "Value")],
            ["ProtocolName", ds.get("ProtocolName", "Value")],
            ["StudyID", ds.get("StudyID", "Value")],
            ["FrameOfReferenceUID", ds.get("FrameOfReferenceUID", "Value")],
        )


def get_intact_results(ds):
    return (
            ["PatientID", ds.get("PatientID", "Value")],
            ["Manufacturer", ds.get("Manufacturer", "Value")],
            ["ManufacturerModelName", ds.get("ManufacturerModelName", "Value")],
            ["StudyInstanceUID", ds.get("StudyInstanceUID", "Value")],
            ["StudyDate", ds.get("StudyDate", "Value")],
            ["SeriesInstanceUID", ds.get("SeriesInstanceUID", "Value")],
            ["MagneticFieldStrength", ds.get("MagneticFieldStrength", "Value")]
    )


if __name__ == "__main__":
    unittest.main()

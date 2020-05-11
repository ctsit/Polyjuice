import unittest

import os
import os.path
import re
import shutil
import yaml
import time
import csv
from docopt import docopt
from pathlib import Path
import pydicom
from pydicom import dcmread
from polyjuice.polyjuice import clean_files
from polyjuice.lumberjack import Lumberjack
from polyjuice.filch import DicomCaretaker
from polyjuice.dicom_image import DicomImage


class Flags():
    CONFIG_PATH = '<config_file>'
    INPUT_DIR = '<input_path>'
    OUTPUT_DIR = '<output_path>'
    _verbose = '--verbose'
    _zip_folder = '--zip'
    _use_config = '--config'


class TestFileCleaner(unittest.TestCase):
    """ These tests check that Polyjuice cleans the correct headers and leaves the fields required by NACC intact. """

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

        output_folders = clean_files(self.editor, self.working_file, self.out_dir, self.modifications, self.id_pairs, self.dicom_folders, self.log)
        # this just returns dicom folders, not the image. you want to see that the image was placed in the correct folder (i can see in the file tree that it was) and then check that the headers are scrubbed using the same key as the modifications. also check that the white-listed headers were NOT scrubbed.

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
        # make a second test with THAT result returning a dict of the keys that were white-listed, and it should be equal to what it was before going through polyjuice
        expected = {
            'PatientID': '101',
            'Manufacturer': 'MAN',
            'ManufacturerModelName': 'MODEL',
            'StudyInstanceUID': '1.2.840.113845.11.1000000001874101095',
            'StudyDate': '20100101',
            'SeriesInstanceUID': '1.2.840.113619.2.244.6945.200138',
            'MagneticFieldStrength': pydicom.valuerep.DSfloat(3)
            }

        output_folders = clean_files(self.editor, self.working_file, self.out_dir, self.modifications, self.id_pairs, self.dicom_folders, self.log)

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
    # This dictionary has a dictionary of tags whose value should be modified
    modifications = {
        # 'InstanceCreatorUID': '', not in tuples
        # 'SOPInstanceUID': '', not in tuples
        'AccessionNumber': '',
        'InstitutionName': '',
        # 'InstitutionAddress': '', not in tuples
        'ReferringPhysicianName': '',
        # 'ReferringPhysicianAddress': '', not in tuples
        # 'ReferringPhysicianTelephoneNumbers': '', not in tuples
        'StationName': '',
        'StudyDescription': '',
        'SeriesDescription': '',
        # 'RequestingPhysician': '', not in tuples- but RequestingService is, and has a value
        # 'InstitutionalDepartmentName': '', not in tuples
        'InstanceNumber': '',
        # 'PhysiciansOfRecord': '', not in tuples
        # 'PerformingPhysicianName': '', not in tuples
        # 'NameOfPhysicianReadingStudy': '', not in tuples
        'OperatorsName': '',
        # 'AdmittingDiadnosesDescription': '', not in tuples
        # 'ReferencedSOPInstanceUID': '', not in tuples- but ReferencedImageSequence is
        # 'DerivationDescription': '', not in tuples
        'PatientName': "Anonymous",
        # 'PatientID': '',
        'PatientBirthDate': "19010101",
        # 'PatientBirthTime': '', not in tuples
        'PatientSex': '',
        # 'OtherPatientIDs': '', not in tuples
        # 'OtherPatientNames': '', not in tuples
        'PatientAge': '',
        # 'PatientSize': '', not in tuples
        'PatientWeight': '',
        # 'MedicalRecordLocator': '', not in tuples
        # 'Manufacturer': '',
        # 'ManufacturersModelName': '',
        'EthnicGroup': '',
        # 'Occupation': '', not in tuples
        'AdditionalPatientHistory': '',
        # 'PatientComments': '', not in tuples
        'DeviceSerialNumber': '',
        'ProtocolName': '',
        # 'StudyInstanceUID': '',
        # 'StudyDate': '',
        # 'SeriesInstanceUID': '',
        # 'MagneticFieldStrength': '',
        'StudyID': '',
        'FrameOfReferenceUID': '',
        # 'SynchronizationonFrameOfReferenceUID': '', not in tuples
        # 'ImageComments': '', not in tuples
        # 'RequestAttributesSequence': '', not in tuples
        # 'UID': '', not in tuples
        # 'ContentSequence': '', not in tuples- but ContentDate and ContentTime are
        # 'StorageMediaFileSetUID': '', not in tuples
        # 'ReferencedFrameOfReferenceUID': '', not in tuples
        # 'RelatedFrameOfReferenceUID': '', not in tuples
        # 'RescaleIntercept': 'Null', not in tuples
        # 'RescaleSlope': 'Null', not in tuples
        # 'RescaleType': 'Null', not in tuples
        # Commented terms should not be modified; check that they are intact
    }
    return modifications


def get_output_results(ds):
    return (
            # ["InstanceCreatorUID", ds.get("InstanceCreatorUID", "Value")],
            # ["SOPInstanceUID", ds.get("SOPInstanceUID", "Value")],
            ["AccessionNumber", ds.get("AccessionNumber", "Value")],
            ["InstitutionName", ds.get("InstitutionName", "Value")],
            # ["InstitutionAddress", ds.get("InstitutionAddress", "Value")],
            ["ReferringPhysicianName", ds.get("ReferringPhysicianName", "Value")],
            # ["ReferringPhysicianAddress", ds.get("ReferringPhysicianAddress", "Value")],
            # ["ReferringPhysicianTelephoneNumbers", ds.get("ReferringPhysicianTelephoneNumbers", "Value")],
            ["StationName", ds.get("StationName", "Value")],
            ["StudyDescription", ds.get("StudyDescription", "Value")],
            ["SeriesDescription", ds.get("SeriesDescription", "Value")],
            # ["RequestingPhysician", ds.get("RequestingPhysician", "Value")],
            # ["InstitutionalDepartmentName", ds.get("InstitutionalDepartmentName", "Value")],
            ["InstanceNumber", ds.get("InstanceNumber", "Value")],
            # ["PhysiciansOfRecord", ds.get("PhysiciansOfRecord", "Value")],
            # ["PerformingPhysicianName", ds.get("PerformingPhysicianName", "Value")],
            # ["NameOfPhysicianReadingStudy", ds.get("NameOfPhysicianReadingStudy", "Value")],
            ["OperatorsName", ds.get("OperatorsName", "Value")],
            # ["AdmittingDiadnosesDescription", ds.get("AdmittingDiadnosesDescription", "Value")],
            # ["ReferencedSOPInstanceUID", ds.get("ReferencedSOPInstanceUID", "Value")],
            # ["DerivationDescription", ds.get("DerivationDescription", "Value")],
            ["PatientName", ds.get("PatientName", "Value")],
            ["PatientBirthDate", ds.get("PatientBirthDate", "Value")],
            # ["PatientBirthTime", ds.get("PatientBirthTime", "Value")],
            ["PatientSex", ds.get("PatientSex", "Value")],
            # ["OtherPatientIDs", ds.get("OtherPatientIDs", "Value")],
            # ["OtherPatientNames", ds.get("OtherPatientNames", "Value")],
            ["PatientAge", ds.get("PatientAge", "Value")],
            # ["PatientSize", ds.get("PatientSize", "Value")],
            ["PatientWeight", ds.get("PatientWeight", "Value")],
            # ["MedicalRecordLocator", ds.get("MedicalRecordLocator", "Value")],
            ["EthnicGroup", ds.get("EthnicGroup", "Value")],
            # ["Occupation", ds.get("Occupation", "Value")],
            ["AdditionalPatientHistory", ds.get("AdditionalPatientHistory", "Value")],
            # ["PatientComments", ds.get("PatientComments", "Value")],
            ["DeviceSerialNumber", ds.get("DeviceSerialNumber", "Value")],
            ["ProtocolName", ds.get("ProtocolName", "Value")],
            ["StudyID", ds.get("StudyID", "Value")],
            ["FrameOfReferenceUID", ds.get("FrameOfReferenceUID", "Value")],
            # ["SynchronizationonFrameOfReferenceUID", ds.get("SynchronizationonFrameOfReferenceUID", "Value")],
            # ["ImageComments", ds.get("ImageComments", "Value")],
            # ["RequestAttributesSequence", ds.get("RequestAttributesSequence", "Value")],
            # ["UID", ds.get("UID", "Value")],
            # ["ContentSequence", ds.get("ContentSequence", "Value")],
            # ["StorageMediaFileSetUID", ds.get("StorageMediaFileSetUID", "Value")],
            # ["ReferencedFrameOfReferenceUID", ds.get("ReferencedFrameOfReferenceUID", "Value")],
            # ["RelatedFrameOfReferenceUID", ds.get("RelatedFrameOfReferenceUID", "Value")],
            # ["RescaleIntercept", ds.get("RescaleIntercept", "Value")],
            # ["RescaleSlope", ds.get("RescaleSlope", "Value")],
            # ["RescaleType", ds.get("RescaleType", "Value")]
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

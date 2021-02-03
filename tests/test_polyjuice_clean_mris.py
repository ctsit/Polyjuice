import unittest

import os
import os.path
import shutil
import pydicom
from pydicom import dcmread
from pathlib import Path
from poly_juice.polyjuice import clean_files
from poly_juice.polyjuice import check_mag_field
from poly_juice.lumberjack import Lumberjack
from poly_juice.filch import DicomCaretaker


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
        self.working_file = 'tests/testInput/MRI/101_01_01_2010/1'
        self.out_dir = 'tests/testOutput/'
        self.first_file = 'tests/testInput/MRI/101_01_01_2010/1'
        self.modifications = make_config()
        self.id_pairs = {'PATIENT_ID': 'UPDATE_ID'}
        self.dicom_folders = ['', '']
        self.log = Lumberjack()

        self.directory = os.path.dirname('tests/testOutput/')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.mri = os.path.dirname('tests/testOutput/101_01_01_2010/1')
        if not os.path.exists(self.mri):
            os.makedirs(self.mri)

    def test_for_cleaned_file(self):
        expected = self.modifications

        clean_files(self.editor, self.working_file, self.out_dir,
                    self.first_file, self.modifications, self.id_pairs,
                    self.dicom_folders, self.log)

        Path('tests/testOutput/101_01_01_2010/1').touch()
        output_file = 'tests/testOutput/101_01_01_2010/1'

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
            'InstanceNumber': pydicom.valuerep.IS('59'),
            'SeriesDescription': 'Average DC',
            'MagneticFieldStrength': pydicom.valuerep.DSfloat("3")
            }

        clean_files(self.editor, self.working_file, self.out_dir,
                    self.first_file, self.modifications, self.id_pairs,
                    self.dicom_folders, self.log)

        if os.path.isfile('tests/testOutput/101_01_01_2010/1'):
            output_file = 'tests/testOutput/101_01_01_2010/1'
        else:
            print("Output file not created.")

        ds = dcmread(output_file)
        data = get_intact_results(ds)
        result = dict(data)

        self.assertDictEqual(expected, result)

    def test_mag_field_get(self):
        output_file = 'tests/testOutput/101_01_01_2010/1'
        mag_field = ''

        expected = float('3')
        result = check_mag_field(self.editor, output_file, mag_field, self.log)

        self.assertEqual(expected, result)

    def test_mag_field_replace(self):
        output_file = 'tests/testOutput/101_01_01_2010/1'
        ds = dcmread(output_file)
        ds.MagneticFieldStrength = ''
        mag_field = '3'

        expected = float('3')
        result = check_mag_field(self.editor, output_file, mag_field, self.log)

        self.assertEqual(expected, result)

    @classmethod
    def tearDownClass(self):
        if os.path.exists('tests/testOutput/101_01_01_2010'):
            shutil.rmtree('tests/testOutput/101_01_01_2010')
            print("Successfully removed tests/testOutput/101_01_01_2010")


def make_config() -> dict:
    modifications = {
        # Commented terms should be skipped by clean_files
        'SpecificCharacterSet': '',
        'ImageType': '',
        'SOPClassUID': '',
        'SOPInstanceUID': '',
        # 'StudyDate': '',
        'SeriesDate': '',
        'AcquisitionDate': '',
        'ContentDate': '',
        'StudyTime': '',
        'SeriesTime': '',
        'AcquisitionTime': '',
        'ContentTime': '',
        'AccessionNumber': '',
        'Modality': '',
        # 'Manufacturer': '',
        'InstitutionName': '',
        'StationName': '',
        'StudyDescription': '',
        # 'SeriesDescription': '',
        'OperatorsName': '',
        # 'ManufacturersModelName': '',
        'ReferencedImageSequence': [],
        # 'PatientID': '',
        'SliceThickness': '',
        'DeviceSerialNumber': '',
        'SoftwareVersions': '',
        'ProtocolName': '',
        'ReconstructionDiameter': '',
        'PatientPosition': '',
        # 'StudyInstanceUID': '',
        # 'SeriesInstanceUID': '',
        'StudyID': '',
        'SeriesNumber': '',
        'AcquisitionNumber': '',
        # 'InstanceNumber': '',
        'ImagePositionPatient': '',
        'ImageOrientationPatient': '',

        'AcquisitionMatrix': '',
        'AngioFlag': '',
        'CardiacNumberOfImages': '',
        'EchoNumbers': '',
        'EchoTime': '',
        'EchoTrainLength': '',
        'EthnicGroup': '',
        'FlipAngle': '',
        'HeartRate': '',
        'ImagedNucleus': '',
        'ImagesInAcquisition': '',
        'ImagingFrequency': '',
        'InPlanePhaseEncodingDirection': '',
        'MRAcquisitionType': '',
        'NumberOfAverages': '',
        'PercentPhaseFieldOfView': '',
        'PercentSampling': '',
        'PerformedProcedureStepDescription': '',
        'PerformedProcedureStepID': '',
        'PixelBandwidth': '',
        'ReceiveCoilName': '',
        'RepetitionTime': '',
        'RequestingService': '',
        'SAR': '',
        'ScanOptions': '',
        'ScanningSequence': '',
        'SequenceVariant': '',
        'SpacingBetweenSlices': '',
        'StackID': '',
        'TriggerWindow': '',
        'VariableFlipAngleFlag': '',

        'ReferringPhysicianName': '',
        'PatientName': 'Anonymous',
        'PatientBirthDate': '19010101',
        'PatientSex': '',
        'PatientAge': '',
        'PatientWeight': '',
        'AdditionalPatientHistory': '',
        # 'MagneticFieldStrength': '',
    }
    return modifications


def get_output_results(ds):
    return (
            ["SpecificCharacterSet", ds.get("SpecificCharacterSet", "Value")],
            ["ImageType", ds.get("ImageType", "Value")],
            ["SOPClassUID", ds.get("SOPClassUID", "Value")],
            ["SOPInstanceUID", ds.get("SOPInstanceUID", "Value")],
            ["SeriesDate", ds.get("SeriesDate", "Value")],
            ["AcquisitionDate", ds.get("AcquisitionDate", "Value")],
            ["ContentDate", ds.get("ContentDate", "Value")],
            ["StudyTime", ds.get("StudyTime", "Value")],
            ["SeriesTime", ds.get("SeriesTime", "Value")],
            ["AcquisitionTime", ds.get("AcquisitionTime", "Value")],
            ["ContentTime", ds.get("ContentTime", "Value")],
            ["AccessionNumber", ds.get("AccessionNumber", "Value")],
            ["Modality", ds.get("Modality", "Value")],
            ["InstitutionName", ds.get("InstitutionName", "Value")],
            ["StationName", ds.get("StationName", "Value")],
            ["StudyDescription", ds.get("StudyDescription", "Value")],
            ["OperatorsName", ds.get("OperatorsName", "Value")],
            ["ReferencedImageSequence", ds.get("ReferencedImageSequence", "Value")],
            ["SliceThickness", ds.get("SliceThickness", "Value")],
            ["DeviceSerialNumber", ds.get("DeviceSerialNumber", "Value")],
            ["SoftwareVersions", ds.get("SoftwareVersions", "Value")],
            ["ProtocolName", ds.get("ProtocolName", "Value")],
            ["ReconstructionDiameter", ds.get("ReconstructionDiameter", "Value")],
            ["PatientPosition", ds.get("PatientPosition", "Value")],
            ["StudyID", ds.get("StudyID", "Value")],
            ["SeriesNumber", ds.get("SeriesNumber", "Value")],
            ["AcquisitionNumber", ds.get("AcquisitionNumber", "Value")],
            ["ImagePositionPatient", ds.get("ImagePositionPatient", "Value")],
            ["ImageOrientationPatient", ds.get("ImageOrientationPatient", "Value")],
            ["AcquisitionMatrix", ds.get("AcquisitionMatrix", "Value")],
            ["AngioFlag", ds.get("AngioFlag", "Value")],
            ["CardiacNumberOfImages", ds.get("CardiacNumberOfImages", "Value")],
            ["EchoNumbers", ds.get("EchoNumbers", "Value")],
            ["EchoTime", ds.get("EchoTime", "Value")],
            ["EchoTrainLength", ds.get("EchoTrainLength", "Value")],
            ["EthnicGroup", ds.get("EthnicGroup", "Value")],
            ["FlipAngle", ds.get("FlipAngle", "Value")],
            ["HeartRate", ds.get("HeartRate", "Value")],
            ["ImagedNucleus", ds.get("ImagedNucleus", "Value")],
            ["ImagesInAcquisition", ds.get("ImagesInAcquisition", "Value")],
            ["ImagingFrequency", ds.get("ImagingFrequency", "Value")],
            ["InPlanePhaseEncodingDirection", ds.get("InPlanePhaseEncodingDirection", "Value")],
            ["MRAcquisitionType", ds.get("MRAcquisitionType", "Value")],
            ["NumberOfAverages", ds.get("NumberOfAverages", "Value")],
            ["PercentPhaseFieldOfView", ds.get("PercentPhaseFieldOfView", "Value")],
            ["PercentSampling", ds.get("PercentSampling", "Value")],
            ["PerformedProcedureStepDescription", ds.get("PerformedProcedureStepDescription", "Value")],
            ["PerformedProcedureStepID", ds.get("PerformedProcedureStepID", "Value")],
            ["PixelBandwidth", ds.get("PixelBandwidth", "Value")],
            ["ReceiveCoilName", ds.get("ReceiveCoilName", "Value")],
            ["RepetitionTime", ds.get("RepetitionTime", "Value")],
            ["RequestingService", ds.get("RequestingService", "Value")],
            ["SAR", ds.get("SAR", "Value")],
            ["ScanOptions", ds.get("ScanOptions", "Value")],
            ["ScanningSequence", ds.get("ScanningSequence", "Value")],
            ["SequenceVariant", ds.get("SequenceVariant", "Value")],
            ["SpacingBetweenSlices", ds.get("SpacingBetweenSlices", "Value")],
            ["StackID", ds.get("StackID", "Value")],
            ["TriggerWindow", ds.get("TriggerWindow", "Value")],
            ["VariableFlipAngleFlag", ds.get("VariableFlipAngleFlag", "Value")],
            ["ReferringPhysicianName", ds.get("ReferringPhysicianName", "Value")],
            ["PatientName", ds.get("PatientName", "Value")],
            ["PatientBirthDate", ds.get("PatientBirthDate", "Value")],
            ["PatientSex", ds.get("PatientSex", "Value")],
            ["PatientAge", ds.get("PatientAge", "Value")],
            ["PatientWeight", ds.get("PatientWeight", "Value")],
            ["AdditionalPatientHistory", ds.get("AdditionalPatientHistory", "Value")],
        )


def get_intact_results(ds):
    return (
            ["PatientID", ds.get("PatientID", "Value")],
            ["Manufacturer", ds.get("Manufacturer", "Value")],
            ["ManufacturerModelName", ds.get("ManufacturerModelName", "Value")],
            ["StudyInstanceUID", ds.get("StudyInstanceUID", "Value")],
            ["StudyDate", ds.get("StudyDate", "Value")],
            ["SeriesInstanceUID", ds.get("SeriesInstanceUID", "Value")],
            ["InstanceNumber", ds.get("InstanceNumber", "Value")],
            ["SeriesDescription", ds.get("SeriesDescription", "Value")],
            ["MagneticFieldStrength", ds.get("MagneticFieldStrength", "Value")]
    )


if __name__ == "__main__":
    unittest.main()

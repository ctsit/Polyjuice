#!/usr/bin/env python3

import os
import os.path
import csv
import sys
from pydicom import dcmread


def convert_tuple_to_dict(tup, di):
    di = dict(tup)
    return di


def search_directory(parent_file: str, out_dir: str, dicom_folders: list, writer):
    if os.path.isfile(parent_file):
        try:
            # Send files to be read
            read_files(parent_file, writer)
        except Exception as e:
            print("{} failed".format(parent_file))
            print(str(e))

    else:
        for path, dirs, files in os.walk(parent_file):
            first_file = ''
            for name in files:
                try:
                    working_file = os.path.join(path, name)
                    ds = dcmread(working_file)
                    # Send files to be read
                    if first_file == '':
                        first_file = working_file
                    if first_file == working_file:
                        print("Working on {}".format(working_file))
                        read_files(working_file, writer)
                except Exception as e:
                    print("{} failed".format(name))
                    print(str(e))


def read_files(dcm_file, writer):
    ds = dcmread(dcm_file)
    folder_name = dcm_file.split("/")[-2]
    visit_num = 1;
    try:
        visit_num = int(folder_name.split("_")[0].split("-")[1])
    except Exception as e:
        print("no visit number in folder name")

    visit_event_name = get_visit_event_name(visit_num)

    data = (
            ["PatientID", ds.get("PatientID", "")],
            ["EventName", visit_event_name],
            ["PatientName", ds.get("PatientName", "")],
            ["StudyDate", ds.get("StudyDate", "")],
            ["SeriesDescription", ds.get("SeriesDescription", "")],
            ["Modality", ds.get("Modality", "")],
            ["ReferringPhysicianName", ds.get("ReferringPhysicianName", "")],
            ["InstitutionName", ds.get("InstitutionName", "")],
            )

    data_dictionary = {}
    converted = convert_tuple_to_dict(data, data_dictionary)
    final = make_csv(converted, dcm_file)
    writer.writerow(final)


def main():
    input_directory = sys.argv[1]
    output_file = sys.argv[2]

    with open(output_file, 'w+', newline='') as output:
        fieldnames = ['ptid',
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
                      'imaging_metadata_complete']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        dcm_folders = []
        # Take a stroll through the folders
        search_directory(input_directory, output_file, dcm_folders, writer)

def get_visit_event_name(visit_num):
    visit_num_event_name_map = {
        1: 'initial_visit_year_arm_1',
        2: 'followup_visit_yea_arm_1',
        3: 'followup_visit_yea_arm_1b',
        4: 'followup_visit_yea_arm_1c',
        5: 'followup_visit_yea_arm_1d',
        6: 'followup_visit_yea_arm_1e',
        7: 'followup_visit_yea_arm_1f',
        8: 'followup_visit_yea_arm_1g',
        9: 'followup_visit_yea_arm_1h',
        10: 'followup_visit_yea_arm_1i',
        11: 'followup_visit_yea_arm_1j',
        12: 'followup_visit_yea_arm_1k'
    }
    return visit_num_event_name_map.get(visit_num)


def make_csv(row: dict, dcm_file: str) -> dict:

    filled = {
        'ptid': row['PatientID'],  # Is ptid present for all MRI / PET images?
        'redcap_event_name': row['EventName'],
        'image_type___1': '',
        'image_type___2': '',
        # REDCap form can have 1, 2, or 1 AND 2 as answers.
        # The MRI and PET data for the same visit must be manually combined.
        'img_mri_patient_name': '',
        'img_mri_patient_id': '',
        'img_mri_date': '',
        'img_mri_study_descrip': '',
        'img_mri_modality': '',
        'img_mri_ref_physician': '',
        # This is a tuple; use the value of 'original_string'
        'img_mri_inst': '',
        'img_mri_site': '',  # MSMC, UF, or UM
        'img_pet_tracer': '',  # I can't find anything like this in the headers
        'img_pet_patient_name': '',
        'img_pet_patient_id': '',
        'img_pet_date': '',
        'img_pet_study_descrip': '',
        'img_pet_modality': '',
        'img_pet_ref_physician': '',
        'img_pet_inst': '',
        'img_pet_site': '',  # MSMC, UF, or UM - couldn't find in dcmread
    }

    if '/MRI' in dcm_file:
        filled['image_type___1'] = '1'
        filled['image_type___2'] = '0'
        filled['img_mri_patient_name'] = row['PatientName']
        filled['img_mri_patient_id'] = row['PatientID']
        filled['img_mri_date'] = row['StudyDate']
        filled['img_mri_study_descrip'] = row['SeriesDescription']
        filled['img_mri_modality'] = row['Modality']
        filled['img_mri_ref_physician'] = row['ReferringPhysicianName']
        filled['img_mri_inst'] = row['InstitutionName']
        filled['img_mri_site'] = 'MSMC'

    elif '/PET' in dcm_file:
        filled['image_type___1'] = '0'
        filled['image_type___2'] = '1'
        filled['img_pet_tracer'] = ''
        filled['img_pet_patient_name'] = row['PatientName']
        filled['img_pet_patient_id'] = row['PatientID']
        filled['img_pet_date'] = row['StudyDate']
        filled['img_pet_study_descrip'] = row['SeriesDescription']
        filled['img_pet_modality'] = row['Modality']
        filled['img_pet_ref_physician'] = row['ReferringPhysicianName']
        filled['img_pet_inst'] = row['InstitutionName']
        filled['img_pet_site'] = 'MSMC'

    filled['imaging_metadata_complete'] = '2'

    return filled


if __name__ == '__main__':
    main()

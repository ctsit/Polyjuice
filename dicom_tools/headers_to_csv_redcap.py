#!/usr/bin/env python3

import os
import os.path
import csv
from pydicom import dcmread


def convert_tuple_to_dict(tup, di):
    di = dict(tup)
    return di


def main():
    with open('dicom_tools/output.csv', 'w+', newline='') as output:
        # fieldnames = ['redcap_event_name', 'patient_id', 'series_instance_id', 'study_instance_id', 'instance_number', 'series_description', 'study_date', 'magnetic_field_strength', 'manufacturer', 'manufacturer_model_name', 'form_dicom_complete']
        fieldnames = ["PatientID",
                      "ImageType",
                      "PatientName",
                      "StudyDate",
                      "SeriesDescription",
                      "Modality",
                      "ReferringPhysicianName",
                      "InstitutionName"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        dcm_files = []
        for root, dirs, files in os.walk('/Users/s.emerson/Documents/Code/polyjuice_examplefiles/input'):
            for names in files:
                if names.endswith(".dcm"):
                    dcm_files.append(os.path.join(root, names))

        for dcm_file in dcm_files:
            ds = dcmread(dcm_file)

            data = (
                    ["PatientID", ds.get("PatientID", "None")],
                    ["ImageType", ds.get("ImageType", "None")],
                    ["PatientName", ds.get("PatientName", "None")],
                    ["StudyDate", ds.get("StudyDate", "None")],
                    ["SeriesDescription", ds.get("SeriesDescription", "None")],
                    ["Modality", ds.get("Modality", "None")],
                    ["ReferringPhysicianName", ds.get("ReferringPhysicianName", "None")],
                    ["InstitutionName", ds.get("InstitutionName", "None")],
                    )

            data_dictionary = {}
            converted = convert_tuple_to_dict(data, data_dictionary)
            final = make_csv(converted)
            writer.writerow(final)


# it looks like for the REDCap csv output we do not want to look at every file in every folder (no instance number + only one row per PTID/visit) - only the first file for the visit. does every folder have a file called '1.dcm'? i could specify to look at that one rather than walking through every file or figuring out how to stop once it finds the first .dcm file and move to the next folder.
# No, all the files have different names in each folder. 


def make_csv(row) -> dict:

    filled = {
        'ptid': row['PatientID'],  # Is ptid present for all MRI and PET images?
        'redcap_event_name': 'initial_visit_year_arm_1',  # this isn't just initial visit year data- the PET, maybe, depending on how close the visit dates are to the corresponding MRI. this might need to mostly be done by hand in excel.
        'image_type': row['ImageType'],  # This is a checkbox question that can have 1, 2, or 1 AND 2 as the value based on if there is MRI(1) and PET(2) data present
        # ImageType is a tuple with a few internal lists- ('_list' item 2 'M' or 'P')
        # ImageType will determine if MRI or PET fields are filled
        'img_mri_patient_name': '',
        'img_mri_patient_id': '',
        'img_mri_date': '',
        'img_mri_study_descrip': '',
        'img_mri_modality': '',  # 'MR' or
        'img_mri_ref_physician': '',  # This is a tuple; use the value of item 'original_string'
        'img_mri_inst': '',
        'img_mri_site': '',  # MSMC, UF, or UM
        'img_pet_tracer': '',  # ??
        'img_pet_patient_name': '',
        'img_pet_patient_id': '',
        'img_pet_date': '',
        'img_pet_study_descrip': '',
        'img_pet_modality': '',  # 'MR' or
        'img_pet_ref_physician': '',
        'img_pet_inst': '',
        'img_pet_site': '',  # MSMC, UF, or UM
    }

    if row['image_type'] == 'M':
        filled['image_type'] = '1'
        filled['img_mri_patient_name'] = row['PatientName']
        filled['img_mri_patient_id'] = row['PatientID']
        filled['img_mri_date'] = row['StudyDate']
        filled['img_mri_study_descrip'] = row['SeriesDescription']
        filled['img_mri_modality'] = row['Modality']  # 'MR' or
        filled['img_mri_ref_physician'] = row['ReferringPhysicianName']  # This is a tuple; use the value of item 'original_string'
        filled['img_mri_inst'] = row['InstitutionName']
        filled['img_mri_site'] = 'MSMC'  # MSMC, UF, or UM

    elif row['image_type'] == 'P':
        filled['image_type'] = '2'
        filled['img_pet_tracer'] = row['']  # ??
        filled['img_pet_patient_name'] = row['PatientName']
        filled['img_pet_patient_id'] = row['PatientID']
        filled['img_pet_date'] = row['StudyDate']
        filled['img_pet_study_descrip'] = row['SeriesDescription']
        filled['img_pet_modality'] = row['Modality']  # 'MR' or
        filled['img_pet_ref_physician'] = row['ReferringPhysicianName']
        filled['img_pet_inst'] = row['InstitutionName']
        filled['img_pet_site'] = 'MSMC'  # MSMC, UF, or UM

    filled['imaging_metadata_complete'] = '2'

    return filled


if __name__ == '__main__':
    main()

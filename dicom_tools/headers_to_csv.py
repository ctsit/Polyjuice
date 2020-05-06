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
                      "SeriesInstanceUID",
                      "StudyInstanceUID",
                      "InstanceNumber",
                      "SeriesDescription",
                      "StudyDate",
                      "MagneticFieldStrength",
                      "Manufacturer",
                      "ManufacturerModelName"]
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
                    ["SeriesInstanceUID", ds.get("SeriesInstanceUID", "None")],
                    ["StudyInstanceUID", ds.get("StudyInstanceID", "None")],
                    ["InstanceNumber", ds.get("InstanceNumber", "None")],
                    ["SeriesDescription", ds.get("SeriesDescription", "None")],
                    ["StudyDate", ds.get("StudyDate", "None")],  # (min: 1/1/2000, max: current date)
                    ["MagneticFieldStrength", ds.get("MagneticFieldStrength", "None")],
                    ["Manufacturer", ds.get("Manufacturer", "None")],
                    ["ManufacturerModelName", ds.get("ManufacturerModelName", "None")]
                    )
# Patient ID (Put your internal PTID in this tag, we will extract it and replace with NACCID)
# Series instance ID
# Study instance ID
# Instance number
# Series description
# Study date (min: 1/1/2000, max: current date)
# Magnetic field strength
# Manufacturer
# Manufacturer model name

            data_dictionary = {}
            final = convert_tuple_to_dict(data, data_dictionary)
            writer.writerow(final)


# fieldnames on redcap:
# ptid
# redcap_event_name
# image_type
# img_mri_patient_name
# img_mri_patient_id
# img_mri_date
# img_mri_study_descrip
# img_mri_modality
# img_mri_ref_physician
# img_mri_inst
# img_mri_site
# img_pet_tracer
# img_pet_patient_name
# img_pet_patient_id
# img_pet_date
# img_pet_study_descrip
# img_pet_modality
# img_pet_ref_physician
# img_pet_inst
# img_pet_site
# imaging_metadata_complete

# it looks like for the REDCap csv output we do not want to look at every file in every folder (no instance number + only one row per PTID/visit) - only the first file for the visit. does every folder have a file called '1.dcm'? i could specify to look at that one rather than walking through every file or figuring out how to stop once it finds the first .dcm file and move to the next folder.


if __name__ == '__main__':
    main()

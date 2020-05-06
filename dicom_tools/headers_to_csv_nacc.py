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
                    # (Put your internal PTID in this tag,
                    # we will extract it and replace with NACCID)
                    ["SeriesInstanceUID", ds.get("SeriesInstanceUID", "None")],
                    ["StudyInstanceUID", ds.get("StudyInstanceID", "None")],
                    ["InstanceNumber", ds.get("InstanceNumber", "None")],
                    ["SeriesDescription", ds.get("SeriesDescription", "None")],
                    ["StudyDate", ds.get("StudyDate", "None")],
                    # (min: 1/1/2000, max: current date)
                    ["MagneticFieldStrength", ds.get("MagneticFieldStrength", "None")],
                    ["Manufacturer", ds.get("Manufacturer", "None")],
                    ["ManufacturerModelName", ds.get("ManufacturerModelName", "None")]
                    )

            data_dictionary = {}
            final = convert_tuple_to_dict(data, data_dictionary)
            writer.writerow(final)


if __name__ == '__main__':
    main()

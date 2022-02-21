#!/usr/bin/env python3

from fnmatch import fnmatch
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
            for name in files:
                try:
                    working_file = os.path.join(path, name)
                    # Send files to be read
                    read_files(working_file, writer)
                except Exception as e:
                    print("{} failed".format(name))
                    print(str(e))


def read_files(dcm_file, writer):
    # if !verifyFolderTitleFormat(dcm_writer):
    #     dcm_writer = rename_file(dcm_writer)
    print("Inside read files of headers to csv nacc")

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


def main():
    input_directory = sys.argv[1]
    output_file = sys.argv[2]

    with open(output_file, 'w+', newline='') as output:
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
        writer.writeheader()
        dcm_folders = []
        # Take a stroll through the folders
        search_directory(input_directory, output_file, dcm_folders, writer)


if __name__ == '__main__':
    main()

# def verifyFolderTitleFormat(filename):
#     return fnmatch(filename, '[0-9]*_.._.._....')

# def rename_file(filename):
#     if fnmatch(filename, '[0-9]*_.._.._..'):
#         return os.rename(filename, )
#     return os.rename(filename, get_new)
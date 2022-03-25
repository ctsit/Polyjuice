#!/usr/bin/env python3

import os
import os.path
import shutil
import yaml
import csv
import pydicom
from pydicom import dcmread
from docopt import docopt
from poly_juice.lumberjack import Lumberjack
from poly_juice.filch import DicomCaretaker
from poly_juice.dicom_image import DicomImage

docstr = """
Polyjuice
Usage:
    polyjuice.py (-h | --help)
    polyjuice.py [-vz]  (<input_path> <output_path>) [<config_file>]
    polyjuice.py [-vzc] [<config_file>]

Options:
  -h --help                     Show this message and exit
  -z --zip                      Archives the output folder
  -v --verbose                  Give progress of program in terminal
  -c --config                   Use config file to get input and output paths

Instructions:
    Run polyjuice on individual files, ISOs, or directories. This will give an
    ouput folder containing dicom files that have had their tags cleaned
    according to your standards set in the config file.
"""

CONFIG_PATH = '<config_file>'
INPUT_DIR = '<input_path>'
OUTPUT_DIR = '<output_path>'
_verbose = '--verbose'
_zip_folder = '--zip'
_use_config = '--config'


def get_config(config_path: str) -> dict:
    '''
        Read in the config file. If the config file is missing or the wrong
        format, exit the program.
    '''
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read(), Loader=yaml.FullLoader)
    except Exception as e:
        print("Error: Check config file")
        exit(e)
    return config


def check_directory(out_dir: str) -> None:
    '''
        Check if directory exists. If not, create it.
    '''
    if not os.path.exists(out_dir):
        try:
            os.makedirs(out_dir)
        except Exception as e:
            raise e


def check_mag_field(editor: DicomCaretaker, output_file, value,
                    log: Lumberjack) -> str:

    ds = dcmread(output_file)

    try:
        name = os.path.basename(output_file)
        working_message = "Checking header on {}".format(name)
        log(working_message)

        if ds.MagneticFieldStrength is not None:
            value = ds.MagneticFieldStrength
    except Exception:
        ds.MagneticFieldStrength = value
        ds.save_as(output_file)
        log("MagneticFieldStrength added for {}".format(name))

    return value


def identify_output(editor: DicomCaretaker, working_file: str, out_dir: str,
                    id_pairs: dict, log: Lumberjack) -> str:

    name = os.path.basename(working_file)
    with open(working_file, 'rb') as working_file:
        working_message = "Working on {}".format(name)
        log(working_message)
        image = DicomImage(working_file)

        id_issue = image.update_patient_id(id_pairs, log)
        if id_issue:
            editor.report_id(id_issue, log)

        folder_name = editor.get_folder_name(image)
        identified_folder = os.path.join(out_dir, folder_name)

        output_name = os.path.join(identified_folder, name)

    return output_name


def walk_directory(parent_file: str, out_dir: str, zip_dir: str,
                   modifications: dict, id_pairs: dict, dicom_folders: list,
                   log: Lumberjack) -> list:
    '''
        Walk through directories and send individual files to be cleaned.
    '''
    editor = DicomCaretaker()
    mag_field = ''

    if os.path.isfile(parent_file):
        try:
            if parent_file.endswith(".iso"):
                # Mount and unmount ISO
                new_parent_dir = editor.mount_iso(parent_file, out_dir)
                dicom_folders = walk_directory(new_parent_dir, out_dir,
                                               zip_dir, modifications,
                                               id_pairs, dicom_folders, log)
                editor.unmount_iso()
            else:
                # Send file to be cleaned
                first_file = parent_file
                output_file = identify_output(editor, parent_file, out_dir,
                                              id_pairs, log)
                dicom_folders = clean_files(editor, parent_file, out_dir,
                                            first_file, modifications,
                                            id_pairs, dicom_folders, log)
                mag_field = check_mag_field(editor, output_file, mag_field, log)
        except Exception as e:
            print("{} failed".format(parent_file))
            print(str(e))
            failure_message = "{} failed".format(parent_file) + "\n" + str(e)
            log(failure_message)

    else:
        for path, subdirs, files in os.walk(parent_file):
            first_file = ''
            if (len(files)) > 1:
                editor = DicomCaretaker()
                try:
                    if not (editor.validate_folder_name(path, log)):
                        new_folder_name = get_correct_folder_name(path, files[0], editor)
                        new_output_path = '{}/{}'.format(out_dir, new_folder_name)
                        new_input_path = '{}/{}'.format("/".join(path.split("/")[:-1]), new_folder_name)
                        os.rename(path, new_input_path)

                        if (os.path.exists(new_output_path)):
                            error_msg = 'output folder named {} already exists. skipping folder {}'.format(new_output_path, path)
                            log(error_msg)
                            print(error_msg)
                            continue
                        else:
                            path = new_input_path
                except Exception as e:
                    failure_message = "{} failed".format(parent_file) + "\n" + str(e)
                    log(failure_message)

            for name in files:
                path_message = os.path.join(path, name)
                log(path_message)
                try:
                    check_file_type = os.path.join(path, name)
                    working_file = os.path.join(path, name)
                    if check_file_type.endswith(".iso"):
                        # Mount and Unmount ISO
                        new_parent_dir = editor.mount_iso(working_file,
                                                          out_dir)
                        dicom_folders = walk_directory(new_parent_dir, out_dir,
                                                       zip_dir, modifications,
                                                       id_pairs, dicom_folders,
                                                       log)
                        editor.unmount_iso()
                    else:
                        # Send file to be cleaned
                        output_file = identify_output(editor, working_file,
                                                      out_dir, id_pairs, log)
                        if first_file == '':
                            first_file = working_file
                        dicom_folders = clean_files(editor, working_file, out_dir,
                                                    first_file, modifications,
                                                    id_pairs, dicom_folders, log)
                        mag_field = check_mag_field(editor, output_file, mag_field, log)

                except Exception as e:
                    print("{} failed".format(name))
                    print(str(e))
                    failure_message = "{} failed".format(name) + "\n" + str(e)
                    log(failure_message)
    return dicom_folders



def get_correct_folder_name(path: str, first_file: str, editor):
    # Taking the first file from the folder
    working_file = os.path.join(path, first_file)

    with open(working_file, 'rb') as working_file:
        image = DicomImage(working_file)
        return editor.get_folder_name(image)

def clean_files(editor: DicomCaretaker, working_file: str, out_dir: str,
                first_file: str,
                modifications: dict, id_pairs: dict, dicom_folders: list,
                log: Lumberjack) -> list:
    '''
        Use DicomCaretaker to clean files and find approprite folders
        to save the output
    '''
    try:
        name = os.path.basename(working_file)
        with open(working_file, 'rb') as working_file:
            image = DicomImage(working_file)

            editor.scrub(image, modifications, id_pairs, log)

            folder_name = editor.get_folder_name(image)
            identified_folder = os.path.join(out_dir, folder_name)

            check = os.path.join(folder_name, name)
            if check in first_file:
                check_directory(identified_folder)
                dicom_folders.append(identified_folder)

            editor.save_output(image, identified_folder, name)
            saving_message = "Saved to {}".format(identified_folder)
            log(saving_message)

    except Exception as e:
        print("{} failed".format(name))
        failure_message = "{} failed".format(name) + "\n" + str(e)
        log(failure_message)
    return dicom_folders


def zip_folder(dicom_folders: list, zip_dir: str, log: Lumberjack) -> None:
    '''
        Zip folders with cleaned DICOM images and
        move them to zip directory specified in config file
    '''
    for folder in dicom_folders:
        shutil.make_archive(folder, 'zip', folder)
        zipped_message = "{} archived".format(folder)
        log(zipped_message)

        check_directory(zip_dir)
        os.system("mv {}.zip {}".format(folder, zip_dir))
        move_zip_message = "{} moved to {}".format(folder, zip_dir)
        log(move_zip_message)


def main(args):
    if not args[CONFIG_PATH]:
        args[CONFIG_PATH] = 'poly_juice/config.yaml'

    config = get_config(args[CONFIG_PATH])
    modifications = config.get('modifications')

    reset_IDS = config.get('new_IDs')
    if reset_IDS is None:
        reset_IDS = 'poly_juice/ids.csv'
    try:
        with open(reset_IDS, mode='r') as in_oldIDfile:
            reader = csv.reader(in_oldIDfile)
            id_pairs = {rows[0]:rows[1] for rows in reader}
    except Exception as e:
        print("Check CSV. \n" + str(e))
        return

    if args[_zip_folder]:
        zip_dir = config.get('zip')
        print("zip folder " + str(zip_dir))
    else:
        zip_dir = None

    verbose = args[_verbose]

    dicom_folders = []
    if args[_use_config]:
        # Get inputs/outputs from config file
        in_root = config.get('in_data_root')
        out_root = config.get('out_data_root')
        io_pairs = config.get('io_pairs')

        for io_pair in io_pairs:
            out_dir = os.path.join(out_root, io_pair['output'])
            check_directory(out_dir)
            log_path = os.path.join(out_dir, 'log.txt')
            log = Lumberjack(log_path, verbose)
            parent_file = os.path.join(in_root, io_pair['input'])
            dicom_folders = walk_directory(parent_file, out_dir, zip_dir,
                                           modifications, id_pairs,
                                           dicom_folders, log)

    else:
        # Loop through ISOs and subdirectories
        parent_file = args[INPUT_DIR]
        out_dir = args[OUTPUT_DIR]
        check_directory(out_dir)
        log_path = os.path.join(out_dir, 'log.txt')
        log = Lumberjack(log_path, verbose)
        dicom_folders = walk_directory(parent_file, out_dir, zip_dir,
                                       modifications, id_pairs, dicom_folders,
                                       log)

    if zip_dir:
        zip_folder(dicom_folders, zip_dir, log)


if __name__ == '__main__':
    args = docopt(docstr)
    main(args)

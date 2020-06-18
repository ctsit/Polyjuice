polyjuice
======

Polyjuice is a modification of pydicom meant to anonymize DICOM images in a
specific directory by scrubbing or changing their header information. It then
saves the images in another specified directory in order to preserve the
original data, and is also capable of archiving the scrubbed images into
compressed .zip files.

The input and output locations, and the headers that are edited, are all
included in the config.yaml file. The default settings for the config file are
to scrub every header except those required for a successful upload to NACC's
database.

Polyjuice has a secondary function of reading the existing DICOM image headers
into a .csv file. This process is currently tailored to the 1Florida ADRC's
REDCap project fields.


## Requirements

Polyjuice works on OSX and Linux.
Use with Python 3.

## Setting up the environment

While running polyjuice, make sure a virtual environment is activated in the
command terminal by navigating into the polyjuice directory and running the
command:

`python3 -m venv venv` (for first-time setup)
`source venv/bin/activate`

During the first-time setup, within the polyjuice directory you also need to
run:

`pip install -e .`

This will install polyjuice's package dependencies.

## Using polyjuice

Open the `config.yaml.example` file within the `poly_juice/` folder. Make sure
your settings are specified and save it as `config.yaml`. 

You can view polyjuice usage in the terminal with the `-h` or `--help` flag.

There are two ways to use polyjuice:

1. Write the input and output paths in the terminal:
`python poly_juice/polyjuice.py /my/path/to/input/folder /my/path/to/output/folder`

2. Write the input and output paths in the config file:
`python poly_juice/polyjuice.py -c`

If you use the second option, you can use either the `-c` or `--config` flag.
The default config file is `config.yaml` within the `poly_juice/` folder, but
another can be specified by naming it after the `-c` flag:
`python poly_juice/polyjuice.py -c /path/to/config.yaml`

The config file allows you to choose the location for .zip files and the
list of any IDs that need to be updated.

You can use the `-z` or `--zip` flag to archive the output folders. The
desired location of your archived files is written in the config file.

For more detailed information about polyjuice's progress, use the `-v` or
`--verbose` flag.

Note that neither the output directory nor the archive directory need exist
before running the program. If they do not exist, Polyjuice will make them for
you.

If a file does not have the 'DICM' marker, it will fail. If a file you need to
read is failing, you can add `force=True` on `read_file` (in
`poly_juice/dicom_image.py`).

`self._dataset = dicom.read_file(dicom_file, force=True)`

## Making use of the config file

The config file contains several ways to help you customize your project.

The first key, zip, allows you to choose the location your archived files will
be sent to.

The second key, new_IDs, allows you to provide the path to a .csv file to
update any patient IDs. Patient IDs may need to be edited if they are in the
wrong format, since Polyjuice determines the name of the output folders based
on the final "PatientID" field in the DICOM header in order to conform to NACC
naming convention (`ID_and_scan_date`). The .csv file should have the old IDs
in the first column and the new IDs in the second column.

The next key, modifications, has all the tags that will undergo some change.
The tag to be modified should have its name as the key and the desired change
should be the value. For example, setting `PatientBirthDate:190101` sets the
PatientBirthDate to 1/1/1901, while `PatientBirthDate:''` sets the
PatientBirthDate tag to a blank value. To delete a tag, the value should be
`Null`. To skip a tag and leave it intact, simply comment out that tag with #
or delete it.

The modifications listed in the config file were selected in accordance with 
the [DICOM Standards Committee](ftp://medical.nema.org/medical/dicom/final/sup55_ft.pdf). 
You can add and remove, comment and uncomment as desired for your project.

The next two keys, in_data_root and out_data_root, contain the root for the
input and output folders. Polyjuice will search the entire in_data_root folder
for any folders containing DICOM files, allowing for multiple image series to
be processed at once.

Finally, the io_pairs key contains a dictionary with the input and output
files. If you use the preceding two keys for the file roots, these **must**
not start with a `/` or they will be interpreted as an absolute path and ignore
the roots. However, you can use sub-directories in the io_pair dictionary while
still using the roots.

```
in_data_root: /my/root/input/path
out_data_root: /my/root/output/path

io_pairs:
    - input: with/sub/directory/my_file.iso
    - output: output_folder
```

References
------

Pydicom: <https://github.com/pydicom/pydicom>

License
------

Apache 2: <http://www.apache.org/licenses/LICENSE-2.0>

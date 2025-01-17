# CHANGELOG
# ref: http://keepachangelog.com/en/0.3.0/
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

Example
## [0.0.x] 2017-04-26
### Summary
 * This is a quick summary for people to understand what this release is about.

### Fixed
 * Fixed broke thing 1 (DevMattm)

### Added
 * Added cool new feature (DevMattm)

### Changed
 * Changed something to make more awesome (DevMattm)

-------------------------------------------------------------------------
-------------------------------------------------------------------------
## [2.4.0] 2022-09-02
### Summary
* In this release, the handling of erroneous data was improved.

### Added
 * Add a minorcomment to make code more readable (karanasthana)
 * Add conditional addition of redcap event name in th event of presence of a visit number in the folder name for the headers_redcap file (karanasthana)
 * Add mapping from ptid-visit_no to ptid (karanasthana)
 * Add parsing of the visit id included in the folder name (karanasthana)
 * Add event name parsing in headers_to_csv_redcap (karanasthana)

### Changed
 * Change in logging of old id to new id (karanasthana)
 * Remove logging and fix exception (karanasthana)
 * Fix test cases to incorporate the new redcap event name changes (karanasthana)
 * Fix bugs in the get visit number event name code (karanasthana)

##[2.3.0] 2021-02-03
### Summary
* This release adds more unit tests and adds a default ids.csv file to avoid
errors for new installs.

### Added
* Default "ids.csv" file to simplify setup and add unit tests to polyjuice (Samantha Emerson)
* Unit tests (Samantha Emerson)

##[2.2.0] 2020-07-20
### Summary
* In this release, the NACC required headers were setup in the config example file and further logic was added to update the dicome tool behavior.

### Added
* Add more logic to 'first_file' choice in headers_to_csv_redcap.py (Samantha Emerson)

### Changed
* Adjust config example file to leave important headers untouched (Samantha Emerson)
* Remove typing of non-returned search_directory function in dicom_tools files (Samantha Emerson)

##[2.1.0] 2020-06-17
### Summary
 * The requirements file was update to make use of the latest pydicom version. This lead to pydicom references needing update throughout the program. Also, handling for ids.csv file was enhanced to allow skipping if no IDs specified so that a directory if dicom files could be processed without subject ID renaming.

### Fixed
  * Typos in config.yaml

### Changed
 * Example config.yaml file to reflect DICOM fields to exclude from modification.
 * Unit tests for zip capabilities
 * Ability to create output folders is they don't exist

 ### Added
 * Function to add missing MagneticFieldStrength to DICOM header as per NACC feedback

##[2.0.0] 2019-11-14
### Summary
 * In this release, the function names were updated to removed references to Harry Potter. Additionally, this release includes work to upgrade from Python 2 to 3.

### Changed
 * Python 2 nomenclature to Python 3
 * Renamed function names

##[1.0.0] 2018-05-18
### Summary
 * The requirements file was update to make use of the latest pydicom version. This lead to pydicom references needing update throughout the program. Also, handling for ids.csv file was enhanced to allow skipping if no IDs specified so that a directory if dicom files could be processed without subject ID renaming.

### Fixed
  * ID skipping

### Changed
 * Requirements for program to return
 * Pydicom version

##[0.2.0]
 * Fix id_pairs bug
 * Remove vulnerable libraries from requirements
 * Gracefully handle missing tags
 * Fix typo in Linux unmount command

##[0.1.0]
 * Add DicomImage class
 * Add logger (Lumberjack)
 * Add id csv

##[0.0.1]
 * Add gitignore
 * Create README.md, CHANGELOG.md, AUTHORS and LICENSE
 * Add config file
 * Write polyjuice.py
 * Add DicomCaretaker class

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

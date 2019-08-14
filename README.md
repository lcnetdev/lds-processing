# About

This is small set of python scripts to assist with

- Converting a batch of MARC ISO2709 files to MARC/XML
- Converting MARCXML to Bibframe resources using the LC bibframe2marcxml2 conversion
- Processing bibframe resources to METS files for loading

at scale.

They are used at LC so, for example, assume each MARC ISO2709 file contains 1,000,000
MARC records.  While the first two are generic enough to perhaps be of use generally, the last 
is specific to LC's ID.LOC.GOV loading processes.  Another assumption: these are 
designed to run on a *nix machine.

# Getting Started

~~~bash
virtualenv -p python3 ldspenv
cd ldspenv
. bin/activate
git clone https://github.com/kefo/lds-processing.git
cd lds-processing
pip install -r requirements.txt
~~~

At this point you will need to modify at least one file to get going:

~~~bash
cp config/config.default.yaml config/config.yaml
~~~

A description of each configuration block and options follows.

# marc2marcxml

This process takes a batch of MARC ISO2709 files and ultimately outputs MARC/XML files, but 
it splits the ISO2709 files into smaller chunks, then converts the ISO2709 to MARC/XML, and 
finally ends by running each MARC/XML file through `uconv` to transcode each file to
head off character issues.

Prerequisite:  Ensure `yaz-marcdump` and `uconv` are installed.

To run:

~~~bash
./marc2marcxml --config config/config.yaml
~~~

The config section:

~~~yaml
marc2marcxml:
    threads: 4
    num_records_per_file: 5000
    source_directory: /location/of/marc2709/files/
    tmp_processing_directory: /tmp/
    clean_target_directory: true
    target_directory: /location/of/output/marcxml/files/
~~~

`threads` refers to how many parallel threads should be used.  
`num_records_per_file` indicates the chunk size, meaning how many records should be 
in each file ultimately.
`source_directory` identifies the directory in which the program will find the source
MARC 2709 files.
`tmp_processing_directory` is a directory in which temporary files can be written during processing.
`clean_target_directory` true/false.  If `true` then the contents of the target directory will be deleted prior
to the main function running.
`target_directory` identifies the directory in which the program will write the output files.

# marcxml2bf

This process takes a directory of MARC/XML files and processes each through the 
marc2bibframe2 XSLT-based conversion.

Prerequisite:  Install and configure [marc2bibframe2](https://github.com/lcnetdev/marc2bibframe2)

To run:

~~~bash
./marcxml2bf --config config/config.yaml
~~~

The config section:

~~~yaml
marcxml2bf:
    threads: 5
    command: xsltproc --stringparam baseuri http://id.loc.gov/resources/REPLACE/ --stringparam idsource http://id.loc.gov/vocabulary/organizations/dlcmrc /location/of/xsl/marc2bibframe2.xsl %INFILE% > %OUTFILE% 
    source_directory: /marcxml/source/dir/
    clean_target_directory: true
    target_directory_single_dir: true
    target_directory: /bf/target/dir/
~~~

For `threads`, `source_directory`, `clean_target_directory`, and `target_directory` see the *marc2marcxml* section.

`command` is the base command that will run.  Take note that it includes variables you can set for the 
actual marcxml2bibframe2 conversion.  %INFILE% and %OUTFILE% will be replaced with appropriate values at 
run time by the script itself.  
`target_directory_single_dir` will save all of the output files in a single directory.  Otherwise, if the source files 
come from a multiple sub-directories (within the `source_directory`), the output will be saved in corresponding 
sub-directories in the `target_directory`.

# bf2mets

This may disappear, to be replaced with a more abstract process that would permit
the processing of arbitrary RDF resources into METS files, to be loaded to ID. But 
as it is here now...  This will take a directory of RDF/XML files in which are 
Bibframe resources and process them into METS files for loading to ID.LOC.GOV.

Prerequisite:  Install and configure [zorba](https://github.com/zorba-processor/zorba)

To run:

~~~bash
./bf2mets --config config/config.yaml
~~~

The config section:

~~~yaml
    threads: 3
    command: /where/zorba/is/installed/bin/zorba -i --serialize-text -q file:///source/xquery/resources2mets.xqy -e sourceuri:=%INFILE% -e savedir:=%OUTFILE% -e tableORschedule:= -e letter:=
    source_directory: /bf/source/dir/
    clean_target_directory: true
    target_directory_single_dir: true
    target_directory: /mets/target/dir/
~~~

For `threads`, `source_directory`, `clean_target_directory`, and `target_directory` see the *marc2marcxml* section.
For `command` and `target_directory_single_dir` see the *marcxml2bf* section.


# License
As a work of the United States government, this project is in the
public domain within the United States.

Additionally, we waive copyright and related rights in the work
worldwide through the CC0 1.0 Universal public domain dedication. 

[Legal Code (read the full text)](https://creativecommons.org/publicdomain/zero/1.0/legalcode).

You can copy, modify, distribute and perform the work, even for commercial
purposes, all without asking permission.




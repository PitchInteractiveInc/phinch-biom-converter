# Phinch HDF5 to JSON BIOM Converter

***

## Which BIOM Files Work With Phinch?

[Phinch](http://phinch.org/) works with [BIOM](http://biom-format.org/) file type 1.0, which is formatted as JSON. This is the file format produced by [QIIME](http://qiime.org/) version 1.8 and earlier. If you're using a newer version of [QIIME](https://qiime2.org/), it will produce [BIOM](http://biom-format.org/) file type 2.1, which is formatted as HDF5.

It's possible to convert the HDF5 tables into JSON tables using recent versions of [QIIME](https://qiime2.org/) or the [biom-format](http://biom-format.org/documentation/biom_format.html) package. The following command will create a new JSON-formatted [BIOM](http://biom-format.org/) file: 

`biom convert -i otu_table.biom -o otu_table_json.biom --table-type="OTU table" --to-json`

Alternatively, you can use [this web-based tool](http://phinchconversion.pitchinteractive.com/) to convert an HDF5-formatted [BIOM](http://biom-format.org/) file to a JSON-formatted [BIOM](http://biom-format.org/) file that will work with [Phinch](http://phinch.org/).

***

## Using This Tool on the Web

* First, load [this conversion tool](http://phinchconversion.pitchinteractive.com/) in your web browser.
* Second, drag your HDF5 BIOM file to the area labeled *Drop File Here* or select *Browse* to select it from the file picker.
* Third, click the button labeled *Convert File* and wait for the converted file to be downloaded, or for an Open/Save dialog box to appear.
* Then, choose a name and location for your new converted file.
* Finally, open [Phinch](http://phinch.org/) and upload your new JSON-formatted BIOM file.


***

## Running This Tool Yourself

If you'd like to run this tool locally, first, clone this repository.

`git clone https://github.com/PitchInteractive/phinch-biom-converter`

Then, enter the new directory.

`cd phinch-biom-converter/`

Next, setup a virtual environment in Python. In this case I've named the environment "phin".

`virtualenv phin`

Then, activate the virtual environment.

`source ./phin/bin/activate`

Install numpy.

`pip install numpy`

After that, install the dependencies in requirements.txt using pip.

`pip install -r requirements.txt`

Finally, run main.py to start the server and load the resulting address in your browser of choice.

`python main.py`

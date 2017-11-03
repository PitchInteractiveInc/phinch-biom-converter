#Phinch HDF5 to JSON BIOM Converter

***

##Which BIOM Files Work With Phinch?

[Phinch](http://phinch.org/) works with [BIOM](http://biom-format.org/) file type 1.0, which is formatted as JSON. This is the file format produced by [QIIME](http://qiime.org/) version 1.8 and earlier. If you're using a newer version of [QIIME](https://qiime2.org/), it will produce [BIOM](http://biom-format.org/) file type 2.1, which is formatted as HDF5.

It's possible to convert the HDF5 tables into JSON tables using recent versions of [QIIME](https://qiime2.org/) or the [biom-format](http://biom-format.org/documentation/biom_format.html) package. The following command will create a new JSON-formatted [BIOM](http://biom-format.org/) file: 

`biom convert -i otu_table.biom -o otu_table_json.biom --table-type="OTU table" --to-json`

Alternatively, you can use [this web-based tool](http://link-to-the-tool-tk.com) to convert an HDF5-formatted [BIOM](http://biom-format.org/) file to a JSON-formatted [BIOM](http://biom-format.org/) file that will work with [Phinch](http://phinch.org/).

***

##Running This Tool

If you'd like to run this tool locally, first, clone this repository.

`git clone https://github.com/PitchInteractive/TKTK`

Next, setup a virtual environment in Python. In this case I've named the environment "phin".

`setup virtualenv {phin}`

Then, activate the virtual environment.

`source ./{phin}/bin/activate`

After that, install the dependencies in requirements.txt using pip.

`pip install requirements.txt`

Finally, run main.py to start the server and load the resulting address in your browser of choice.

`python main.py`

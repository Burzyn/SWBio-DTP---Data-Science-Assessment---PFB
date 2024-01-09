
# 
# The following program (Main.py) may be used to visualise any absorbance data that has a timeline as this is
# the current format of the plots produced. Such as that of the bacterial growth in 96-well plates.
# In this example the code was used to assess the imagined/simulated data for
# the Appelmans Method, used to determine the bacteriophage resistance in bacteria.
#
# The idealised purpose of programming is to write the code once. The ‘power’ of the code attached is in its flexibility,
# as no matter the number of bacterial samples, or treatment groups, or timepoints, the code will ‘adjust itself’
# to the data and identify the experimental parameters and then visualise the results. Furthermore, the script can
# load multiple experimental replicate files via dialog window and use the data to obtain the average results with
# the SD of the results. Finally, the code can be used to obtain the table of means and SD as an csv file with the
# custom name which with the PyCharm was saved to the project folder.
#
# The only requirement is to use the constant data format and to remember that all experimental replicates should have
# the same sample labels. In the csv data file, the “Timepoint” has the integer value (hour), “Sample” can be anything
# and all other columns can represent the specimens. Once again, the data attached is and example of how it might look
# like for hypothetical strains and bacteriophages. All values indicate the OD600 in this instance but may indicate any
# other absorbance.
#
# The code was written and tested using the PyCharm Community Edition with the following additional libraries used.
# If these need to be installed a repository also contains the Instalation.py file:
#
# •	Pandas
# •	Matplotlib
# •	Tkinter

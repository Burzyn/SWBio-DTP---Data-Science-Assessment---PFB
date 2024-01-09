
# Piotr Burzynski

# ============================================================================================================= #
#### BANK:

TAB1 = """
"""
TAB2 = "\n"
Loader = 1
FileNumber = 0
LoaderStr = """Load another file as an experiment replicate?
Type '1' if YES, or '0' if NO."""
data_step = 0
Loader_init = True
Files = []
FileNumber = 0
BacteiraList = []
SampleList = []
Control_Present = False

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog


# ============================================================================================================= #
#### STARTER:

print("""


            =================================================================================            

                   Welcome to the automated analysis tool for the data describing the 
                          bacterial phage resistance via the Appelmans Method.
                  Please refer to the ReadMe file for more information and instructions.

            =================================================================================            

""")


while True:
    if Loader == 1:
        print("""Open the csv file via dialog window or specify the file path?
        Type '0' for the dialog window option, or '1' for an example file.""")
        step1 = input(print("      TYPE: "))
        print(TAB2)
        if step1 == "0":
            if Loader_init:
                dataload = filedialog.askopenfilename()
                data0 = pd.read_csv(dataload)
                Files.append(dataload)
                LoadStep = 1
                data0["Replicate"] = LoadStep
                print(LoaderStr)
                step2 = input(print("      TYPE: "))
                if step2 == "0" or  step2 == "'0'":
                    Loader = 0
                    data = data0
                print(TAB2)
                Loader_init = False
            else:
                LoadStep = LoadStep + 1
                dataload = filedialog.askopenfilename()
                dataloaded = pd.read_csv(dataload)
                dataloaded["Replicate"] = LoadStep
                Files.append(dataload)
                print(LoaderStr)
                data = pd.concat([data0, dataloaded])
                step2 = input(print("      TYPE: "))
                if step2 == "0" or  step2 == "'0'":
                    Loader = 0
                print(TAB2)
        elif step1 == "2":
            data = pd.read_csv("https://drive.google.com/file/d/1cRio9VjuNScFA8TrDm7xGKHIob1qqzwk/view?usp=sharing")
            Loader = 0
            data["Replicate"] = 1
            Loader_init = False
        else:
            print("Unknown input")
            print(TAB2)
    else:
        print("Process of data loading complete")
        print(TAB1)
        break

# ============================================================================================================= #
#### VIEWER:

for col in data.columns:
    if col != "Sample" or col != "Timepoint" or col != "Plate":
        BacteiraList.append(col)

for sample in data["Sample"]:
    if sample == "Control" or sample == "control":
        Control_Present = True
    else:
        if sample not in SampleList:
            SampleList.append(sample)

print("  <><><> Initial data summary <><><>  ")
print(TAB1)
print("Following bacteria were identified in the analysis:")
print(BacteiraList)
print(TAB1)
print("The bacteria were challenged with following samples (or phages):")
print(SampleList)
if Control_Present:
    print("The control was present")
else:
    print("The control was NOT present")
print(TAB1)
print("  <><><> End of initial data summary <><><>  ")
print(TAB1)


# ============================================================================================================= #
#### DATA PROCESSOR:

Timepoint = data["Timepoint"]
All_Timepoints = []
All_columns = []
All_columns2 = []
Exclusion = ["Sample", "Timepoint"]

for column in data.columns:
    All_columns.append(column)

DataRef1 = pd.DataFrame(columns=All_columns)

for col in data.columns:
    DataRef1[col] = data[col]

step = 0

DataRef2 = data.loc[:, ~data.columns.isin(Exclusion)]
DataRef3 = pd.DataFrame(columns=All_columns)
Timepoints = []
Samples = []
Replicates = []


for col in DataRef2.columns:
    Updater = DataRef1.groupby(["Sample", "Timepoint", "Replicate"])[col].mean()
    Avg = Updater.tolist()
    Keys = Updater.index.tolist()

    DataRef3[col] = Avg
    for item in Keys:
        Timepointval = item[1]
        Timepoints.append(Timepointval)
        Sample = item[0]
        Samples.append(Sample)
        Replicate = int(item[2])
        Replicates.append(Replicate)
    if step == 0:
        DataRef3["Sample"] = Samples
        DataRef3["Timepoint"] = Timepoints
        DataRef3["Replicate"] = Replicates
        step = step + 1

DataCopy = DataRef3

All_columns = []
for column in DataRef3.columns:
    All_columns.append(column)

DataRef1 = pd.DataFrame(columns=All_columns)
for col in data.columns:
    DataRef1[col] = data[col]

DataRef4 = pd.DataFrame(columns=All_columns)
Timepoints = []
Samples = []
Replicates = []
step = 0
DataCopy = DataRef4

for col in DataRef2.columns:
    Updater2 = DataRef1.groupby(["Sample", "Timepoint"])[col].mean()
    SDUp = DataRef1.groupby(["Sample", "Timepoint"])[col].std()
    Avg2 = Updater2.tolist()
    Keys2 = Updater2.index.tolist()
    DataRef4[col] = Avg2
    SD = SDUp.tolist()
    DataCopy[f"{col}_SD{DataRef1.columns.get_loc(col)}"] = SD
    for item in Keys2:
        Timepointval = item[1]
        Timepoints.append(Timepointval)
        Sample = item[0]
        Samples.append(Sample)
    if step == 0:
        DataCopy["Sample"] = Samples
        DataCopy["Timepoint"] = Timepoints
        DataRef4["Sample"] = Samples
        DataRef4["Timepoint"] = Timepoints
        step = step + 1


# ============================================================================================================= #
#### VISUALISER:

Iterated = []
Excluder = ["Timepoint", "Sample", "Replicate"]
CapValue = DataRef4.columns.get_loc("Sample")
for col in DataRef4.columns:
    if DataRef4.columns.get_loc(col) > CapValue:
        Excluder.append(col)
for col in DataRef4.columns:
    if col not in Excluder:
        for item in DataRef4["Sample"]:
            if item not in Iterated:
                temptable = DataRef4.loc[DataRef4["Sample"] == item]
                # print(temptable)
                Iterated.append(item)
                Sample_Name = temptable["Sample"].iloc[0]
                plt.plot(temptable["Timepoint"], temptable[col], label=Sample_Name, marker='o')
                plt.xticks(range(len(temptable)), temptable["Timepoint"])
                plt.xlabel("Time (h)")
                plt.ylabel("OD-600")
                low = temptable[col]-temptable[f"{col}_SD{DataRef1.columns.get_loc(col)}"]
                up = temptable[col]+temptable[f"{col}_SD{DataRef1.columns.get_loc(col)}"]
                plt.fill_between(temptable["Timepoint"], low, up, alpha=0.3)
                leg = plt.legend(loc="upper center")
                plt.suptitle(f"Appelmans method results for {col}")
        Iterated = []
        plt.show()


# ============================================================================================================= #
#### EXPORTER:

print("Save the combined data with means and SD as a new csv file? ")
print("Type '1' if YES and '0' if NO.")
export = input(print("      TYPE: "))
SamplesExport = []
for col in DataCopy:
    if DataRef4.columns.get_loc(col) < CapValue:
        SamplesExport.append(col)
if export == "1":
    Export_columns = []
    for col in DataCopy:
        if col in SamplesExport:
            Export_columns.append(col)
            Export_columns.append(f"{col}_SD")
    for col in DataCopy:
        if col == "Timepoint":
            Export_columns.append(col)
        elif col == "Sample":
            Export_columns.append(col)
        elif col == "Replicate":
            Export_columns.append(col)
    DataExport = pd.DataFrame(columns=Export_columns)
    for col in DataExport:
        if col in DataRef4:
            DataExport[col] = DataRef4[col]
    for col in DataExport:
        if col in SamplesExport:
            DataExport = DataExport.rename(columns={col: f"{col}_Mean_OD"})
    print("Please specify file name.")
    export_name = input(print("      TYPE: "))
    DataExport.to_csv(f"{export_name}.csv")
    print("Process finished.")
else:
    print("Process finished.")
import os
import pandas as pd
from styleframe import StyleFrame

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

inputdir = dname + "/input"
if not os.path.exists(inputdir):os.mkdir(inputdir)
outputdir = dname + "/output"
if not os.path.exists(outputdir):os.mkdir(outputdir)

os.chdir(inputdir)

for fname in os.listdir(inputdir):
    print(fname)
    companyCols = ["Company", "Address", "City", "Phone", "Contact Name"]
    additiveCols = ["Company", "Additive", "Fuel Code"]
    companyData = []
    additiveData = []

    sf = StyleFrame.read_excel(fname, read_style=True, use_openpyxl_styles=False)

    companyList = list(sf[sf.columns[0]])
    fuelList = list(sf[sf.columns[1]])
    totalRows = len(companyList)

    # First Row inclusion
    companyName = str(sf.columns[0])
    i = 0
    validInfo = True
    tempcdata = []
    infoidx = 0
    while i < totalRows:
        if sf[sf.columns[0]][i].style.bg_color == "00000000":
            if sf[sf.columns[0]][i].style.bold:
                companyName = companyList[i]
                i += 1
                validInfo = True
            
            if validInfo:
                print("Finding company info for " + str(companyName))
                tempcdata = [str(companyName)]
                while infoidx < 4:
                    tempcdata.append(str(companyList[i]))
                    i += 1
                    infoidx += 1
                companyData.append(tempcdata)
                validInfo = False

        infoidx = 0
        tempcdata = []
        i += 1

    # First Row inclusion
    companyName = str(sf.columns[0])
    j = 0
    while j < totalRows:
        if sf[sf.columns[0]][j].style.bold:
            companyName = str(companyList[j])
            print("Finding additives for " + companyName + "...")
            
        if "Additive Name" == str(companyList[j]): 
            j += 1
            while j < totalRows and str(fuelList[j]).lower() != "nan":
                ftype = fuelList[j]
                tempadata = [companyName, str(companyList[j]), str(fuelList[j])]
                additiveData.append(tempadata)
                j+=1
            continue        
        
        j += 1


    os.chdir(outputdir)
    companyInfo_df = pd.DataFrame(companyData, columns=companyCols)
    additiveInfo_df = pd.DataFrame(additiveData, columns=additiveCols)

    companyInfo_df.to_csv("company-info.csv", encoding='utf-8', index=False)
    additiveInfo_df.to_csv("additive-info.csv", encoding='utf-8', index=False)
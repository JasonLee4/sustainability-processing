# This will access the api for the economic census data
import json
import csv
import requests
import time
import re
import os

#******KEY INPUTS******************************************
APPID = ''  # my key

project = "Titan"

#**************************Make Dictionary of State Names *************************************

#states = {}

#with open("State_Abbrev.csv", 'r') as z:

#    reader = csv.reader(z)

#    for row in reader:

#        if reader.line_num != 1:

#            states[row[4]] = row[3]

 

#**************************Load three digit NAICS Codes *************************************
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
projectdir = dname + "/" + project
if not os.path.exists(projectdir):os.mkdir(projectdir)

os.chdir(dname)

NAICS = {}

with open("NAICS3.csv", 'r') as z:
    reader = csv.reader(z)
    for row in reader:
        if reader.line_num != 1:
            NAICS[row[0]] = row[1]

#*************************Load Input file**************************************

NAICS_codes = []
try:
    with open(str(project)+"/NAICS3.csv", 'r') as fi:
        reader = csv.reader(fi)
        for row in reader:
            if reader.line_num != 1:
                NAICS_codes.append(row[0])
except Exception as e:
    print(e)

NAICS_codes = [ "541330", "541360","541370","541620", "541", "237", "237110", "237130", "237210", "237990" ] 

#******************Select Year*******************************************************

# print("Code does not support 2007 yet")
year = ""
yearInput = False
while not yearInput:
    year = input("Enter year (ex.: 2012, 2017, or 2022):  ")
    pattern = re.compile("^(19|20)\d{2}$")
    if not pattern.match(year):
        print(year + " is not a valid year")
        continue
    yearInput = True 

#***********Dataset & Variabes**********************************************************

dataset = input("Use this site for dataset reference: 'https://api.census.gov/data.html'\nEnter dataset name (ex. 'ecnbasic' or 'ewks'): ")

var_url = "https://api.census.gov/data/"+year+"/"+dataset+"/variables"
variable_res = requests.get(var_url)
# variable_res.json()
variable_list = [row[0] for row in variable_res.json()]
print(variable_list)

vars = []
varInput = False
while not varInput:
    vars = list(input("List the variables you want (separated by spaces ex. 'VAR1 VAR2 VAR3...'): ").split())
    temp = [v for v in vars if v not in variable_list]
    if len(temp) > 0:
        print("Variables " + str(temp) + " not valid!")
        continue
    
    varInput = True

variables = ','.join(vars)

#***********Geography**********************************************************

geo = ""
goodInput = False
while not goodInput:
    geo = input("Enter geography ('us' for U.S., 'state' for state, and 'county' for county): ")
    if geo not in ['us', 'state', 'county']:
        print("Enter only the listed inputs")
        continue
    goodInput = True

#*******************************************************************************

flag = 1

timestamp = time.strftime("%H%M%S")

file_out = str(project)+"/"+str(geo)+str(year)+"-"+str(timestamp)+".csv"

print(file_out)

with open(file_out, 'w') as fo:
    for code in NAICS_codes:

        url = "https://api.census.gov/data/"+year+"/"+dataset+"?get="+variables+"&for="+geo+"&NAICS"+year+"="+str(code)+"&key="+str(APPID)

        try:
            response = requests.get(url)

        except:
            continue

        if response.status_code == 200:
            time.sleep(0.1)
            print(code)

            response.raise_for_status()

            EC_Data = json.loads(response.text)

            if flag == 1:
                headers = EC_Data[0]

                for h in headers:
                    fo.write(str(h)+",")

                fo.write("\n")

                flag = 0

            i = 1

            while i < len(EC_Data):
                for item in EC_Data[i]:
                    fo.write(str(item)+",")

                fo.write("\n")

                i += 1
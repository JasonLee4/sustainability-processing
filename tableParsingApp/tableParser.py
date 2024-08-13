# Import libraries
import os
import pandas as pd
from gmft.pdf_bindings import PyPDFium2Document
from gmft import CroppedTable, TableDetector
from gmft import AutoTableFormatter
import pandas as pd


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

inputdir = dname + "/input"
if not os.path.exists(inputdir):os.mkdir(inputdir)
# tablesdir = dname + "/"
# if not os.path.exists(tablesdir):os.mkdir(tablesdir)

os.chdir(inputdir)

detector = TableDetector()
formatter = AutoTableFormatter()

def ingest_pdf(pdf_path) -> list[CroppedTable]:
    doc = PyPDFium2Document(pdf_path)

    tables = []
    for page in doc:
        tables += detector.extract(page)
    return tables, doc

filetables_dict = dict()
for fname in os.listdir(inputdir):
    print("Finding tables in " + fname + "...")
    tables, doc = ingest_pdf(fname)
    print("Extracted tables from ", fname)
    
    tabledfs = []
    for tab in tables:
        ft = formatter.extract(tab)
        try:
            tabledfs.append(ft.df())
        except Exception as e:
            print(e)
            tabledfs.append(ft.df())
    filetables_dict[fname] = tabledfs
    
    doc.close()
    print("Total tables from " + fname + " detected : " + str(len(tables)))



# prev_cols = []
# prev_df = 0
# prev_dfname = "None"
for filename, dflist in filetables_dict.items():
    os.chdir(dname)
    outputdir = dname + "/" + filename
    if not os.path.exists(outputdir):os.mkdir(outputdir)
    os.chdir(outputdir)
    os.rename(inputdir+"/"+filename, outputdir+"/"+filename)
    prev_cols = []
    prev_df = 0
    prev_dfname = "None"
    tidx = 0
    for df in dflist:
        with pd.option_context('display.max_rows', 500, "display.multi_sparse", False):
            if df is not None:
                curr_df = df
                if df.empty:
                    print("DataFrame is Empty!")
                    prev_cols = []
                    prev_df = 0
                    prev_dfname = "None"
                else:
                    if prev_cols == list(df.columns) and prev_dfname != "None":
                        print("common columns found from " + prev_dfname)
                        print("merging tables " + prev_dfname + " with table" + str(tidx))
                        curr_df = pd.concat([prev_df, df])
                        
                        prev_cols = list(curr_df.columns)
                        
                        if os.path.isfile(prev_dfname+".csv"):
                            os.remove(prev_dfname+".csv")
                    else:
                        prev_cols = list(df.columns)
                        prev_df = df

                    prev_dfname = "table"+str(tidx)
                    curr_df.to_csv(prev_dfname+".csv", encoding='utf-8', index=False)
        tidx += 1

# for tablename, df in tabledfs_dict.items():
#     with pd.option_context('display.max_rows', 500, "display.multi_sparse", False):
#         if df is not None:
#             curr_df = df
#             if df.empty:
#                 print("DataFrame is Empty!")
#                 prev_cols = []
#                 prev_df = 0
#                 prev_dfname = "None"
#             else:
#                 if prev_cols == list(df.columns) and prev_dfname != "None":
#                     print("common columns found from " + prev_dfname)
#                     print("merging tables ", prev_dfname, " with ",tablename)
#                     curr_df = pd.concat([prev_df, df])
                    
#                     prev_cols = list(curr_df.columns)
                    
#                     if os.path.isfile(prev_dfname+".csv"):
#                         os.remove(prev_dfname+".csv")
#                 else:
#                     prev_cols = list(df.columns)
#                     prev_df = df

#                 prev_dfname = tablename
#                 curr_df.to_csv(tablename+".csv", encoding='utf-8', index=False)
                
                

# Import libraries
import os
import pandas as pd
import fitz
from pathlib import Path

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
inputdir = dname+"/Project/input"
if not os.path.exists(inputdir):os.mkdir(inputdir)
outputdir = dname+"/Project/output"
if not os.path.exists(outputdir):os.mkdir(outputdir)
pdfdir = dname + "/Project/pdfs"
if not os.path.exists(pdfdir):os.mkdir(pdfdir)
outpdfdir = dname + "/Project/outpdfs"
if not os.path.exists(outpdfdir):os.mkdir(outpdfdir)

textlist_dict = {}
for fname in os.listdir(inputdir):
    f = os.path.join(inputdir, fname)
    try:
        df = pd.read_excel(f)
    except:
        df = pd.read_csv(f)
    keywords = [kw.lower() for kw in df['keyword'].to_list()]
    print(keywords)
    textlist_dict["out-"+Path(fname).stem] = keywords

os.chdir(pdfdir)

for out,tl in textlist_dict.items():
    collist =  ["filename"] + tl
    founddata = []
    for tpdf in os.listdir(pdfdir):
        print(tpdf)

        tempdata = [str(tpdf)]    
        doc = fitz.open(os.path.abspath(tpdf))
        goodpages = set()            


        for text in tl:
            page_detect = set()
            for page in doc:
                text_instances = page.search_for(text)
                if len(text_instances) > 0:
                    page_detect.add(str(page.number+1))
                    goodpages.add(page.number)
                    if page.number > 0:
                        goodpages.add(page.number - 1)
                    if page.number < doc.page_count-1:
                        goodpages.add(page.number + 1)
                for inst in text_instances:
                    page.add_highlight_annot(inst)
            tempdata.append(" ".join(list(page_detect)))

        doc.delete_pages(list(set(range(0, doc.page_count)) - goodpages))
        outf = open(outpdfdir+"/output-"+str(tpdf), "w")
        outf.close()
        if doc.page_count > 0:
            doc.save(outpdfdir+"/output-"+str(tpdf))
        

        founddata.append(tempdata)
        
    resdf = pd.DataFrame(founddata, columns=collist)
    # print(resdf)
    os.chdir(outputdir)
    resdf.to_csv(out+".csv", encoding='utf-8', index=False)
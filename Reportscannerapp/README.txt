In the command line, cd to the current directory and run this command:

	pip install -r requirements.txt


USAGE:
In Project folder, go to pdfs folder. Add .pdf files that you want to analyze into that pdfs folder. 
Go to input folder. Add .csv/excel file(s) for keywords to analyze. The ONE column of the files must be titled "keyword". Cells/values for under that 
column indicate which words you want to be scanned in .pdf files. 
Run keywordscanner.py. 


Directories:
Project: contains related files for the app (.pdf files, .csv input files, and output files)
-->input - directory containing input .csv/excel files. 
	--> keywords.csv - example/use .csv file with single column "keyword" for words for program to search for
-->output - directory containing .csv file output from analyzing files
	--> out-keywords.csv - resulting .csv file from program. Columns consist of file name and "keywords" from input file. Values in under keywords
				are text consisting of page numbers where keyword is found.
-->pdfs - Directory, download location for pdfs to analyze
	--> may contain some example report pdfs
-->outpdfs - Directory, contains output from program. edited .pdf file copies from "/pdfs" with relevant pages and highlight keywords.

Files:
keywordcanner.py : script for analyzing files in Project/pdfs

requirements.txt
README
In the command line, cd to the current directory and run this command:

	pip install -r requirements.txt


USAGE:
Add pdf files in the input folder. Run tableParser.py, which will look for text-based tables on the pages of the pdf.


Directories:
input: contains input pdf files to extract tables from

Files:
tableParser.py : script for analyzing tables in pdfs, ONLY detects text-based tables. Merges tables that share columns together if they are continuous
Continuous tables span more than one page but have the same columns. Creates and populates directories (named the input file name)at the level of the program,
which contain input pdf, resulting tables .csv files.

requirements.txt
README
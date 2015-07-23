## Spreadsheet Evaluation Code

This repo contains the code to evaluate the spreadsheets cells. 

Cell may be (1) numbers, (2) basic binary operations (+, -, *, /), or (3) references to other cells.
The references will be of the form \<column\>\<row\>, where \<column\> is a capital letter, and \<row\> is a positive integer.

After evaluating the cells read from INPUTFILE, new spreadsheets with fully solved values will be written to the OUTPUTFILE.

## Running the code

To evaluate the spreadsheet, run: `./spreadsheet_evaluation.py <INPUTFILE> <OUTPUTFILE>`

## Designing Notes
1. Solving the values recursively to avoid cell which references another cell have not been solved yet
2. Using float variable to store cell values for both float and integer input values
3. Printing error message and stopping running when there is any error occurred
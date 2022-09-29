# mdm_merge_table.py

## Author:
  David Thomas - david_thomas@hakkoda.io

## Change Log:
  09/29/2022 - Created the .py file

## How to use this script

  - In your terminal runf the following command:
               
        python3 “path/to/smdm_merge_table.py --csv_loc “path/to/src.csv”
  
  - The program expects a csv file with the following columns: 
    'Source Table/View, Target Column, Data Target Type, Source Column(s), Source Datatype'

  - **Is advised to use the same csv format as the one obtained by downloading a Google sheets file as csv.** Check the example listed below for further details. 
  
  - To specify the path of the file use the following **_required_** parameter:
           
        --csv_loc: Location of tha csv file to be processed. Wrap the path with "" if it contains any space on it. Ex: "a/b/c/.../path with space/"')

  - Using the optional parameter _--help_ will display the paramater details.

  - The output of the file is a csv file. It will be created in the same location of the csv file and adds the string Merged_ to the name of the file received as input. 
  
    - Example: path/myfile.csv -> path/Merged_myfile.scv

  - An example of an expected csv can be found [here](https://docs.google.com/spreadsheets/d/1Za2bMytZgAzC_d2F-UmVbrge9VhBIRiNX8KE6yUW5gc/edit?usp=sharing).

  - An example of the expected output can be found [here](https://docs.google.com/spreadsheets/d/1Gcx2Z-cT9x0KXLzwnwCin0MXc9igW_kECM8HKxUOaDg/edit?usp=sharing).


## Code summary

- What:
  - Python script that script that Combine CSV Rows for Value. Loads a file with multiple rows for a given target column. Each of these target columns may have 1 or more table sources.
  -  Then, it combines all table sources (column A) and column sources (column D) /w table appended as prefix, plus if they have different source datatypes (column E) into a single cell whenever there is more than one table source for the respective target column.

- Why:
  - Automation of the Table rows merging for same Columns.
 
- How: 
  1. The script captures each row in a dictionary, storing them in a list. 
  2. Iterates over the list to identify duplicated Columns to capture the Source tables and Data Types.
  3. Creates a list of dictionaries to store the ones with unique Columns. 
  4. Creates a dictionary of the duplicated Column list where: 
    - Concatenates the Source table with the column.
    - Capture the Data types
    - Store all this information in the same row.
 
- Steps

      Step 0: Imports required modules & defines the .py parameters.
      Step 1: Function that reads a csv file and obtain a dictionary for each row and stores them in a list.
      Step 2: Function to check if all the expected columns are present in the csv file specified by the user.
      Step 3: Function that runs over the list filled with dictionaries creating a dictionary for each Target Column to store associated info. If a column dictionary have more than one unique Source Table/View it stored in another dictionary called multiple_column_dict.
      Step 4: Function that runs over the multiple_column_dict to create a dictionary for each item in it to associated info. Then append the created dictionary to a list called final_dict_list.
      Step 5:  Function that creates the output of the script.
 


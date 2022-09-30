#!/usr/bin/env python
# coding: utf-8

"""
-- mdm_merge_table.py
--
-- Author:
--  David Thomas - david_thomas@hakkoda.io
--
-- Change Log:
--  09/29/2022 - Created the .py file
--
-- What:
--  Python script that script that Combine CSV Rows for Value. Loads a file with multiple rows for a given target column. Each of these target columns may have 1 or more table sources.
--  Then, it combines all table sources (column A) and column sources (column D) /w table appended as prefix, plus if they have different source datatypes (column E) into a single cell whenever
--  there is more than one table source for the respective target column.
-- Why:
--  Automation of the Table rows merging for same Columns. 
-- How:
--  1. The script captures each row in a dictionary, storing them in a list. 
--  2. Iterates over the list to identify duplicated Columns to capture the Source tables and Data Types.
--  3. Creates a list of dictionaries to store the ones with unique Columns. 
--  4. Creates a dictionary of the duplicated Column list where:
--   a. Concatenates the Source table with the column.  
--   b. Capture the Data types.
--   c. Store all this information in the same row.
--
-- Steps
--      Step 0: Imports required modules & defines the .py parameters.
--      Step 1: Function that reads a csv file and obtain a dictionary for each row and stores them in a list.
--      Step 2: Function to check if all the expected columns are present in the csv file specified by the user.
--      Step 3: Function that runs over the list filled with dictionaries creating a dictionary for each Target Column to store associated info.
--          If a column dictionary have more than one unique Source Table/View it stored in another dictionary called multiple_column_dict.
--      Step 4: Function that runs over the multiple_column_dict to create a dictionary for each item in it to associated info.
--          Then append the created dictionary to a list called final_dict_list.
--      Step 5:  Function that creates the output of the script.
-- 
"""


############################################################################
################################### Step 0 #################################
############################################################################

'''
-- What:
--  Imports required packages and define how to parse command line arguments.
-- Why:
--  In order to use the packages and receive  command line arguments.
-- How:
--  Implementing imports and establish how to parse command line arguments through the argparse package.
'''


# import os
# import sys
import csv
import re
import argparse
from operator import itemgetter

parser = argparse.ArgumentParser(
    description='Python script that script that Combine CSV Rows for Source Table/View with same  Target Column using a csv file as source with the following columns: '+
        'Source Table/View, Target Column, Data Target Type, Source Column(s), Source Datatype')
parser.add_argument('--csv_loc', type=str, required=True,
                    help='Location of tha csv file to be processed. Wrap the path with "" if it contains any space on it. Ex: "a/b/c/.../path with space/"')
args = parser.parse_args()
csvLoc = args.csv_loc

############################################################################
################################### Step 1 #################################
############################################################################

'''
-- What:
--  Function that reads a csv file and obtain a dictionary for each row and stores them in a list.
-- Why:
--  Capture all the information in the csv file. 
-- How:
--  Creates a dictionary for each row and store each dictionary in a list.
'''

def csv_to_dict (csv_location):

    try:
        list_of_dict =[*csv.DictReader(open(csv_location, encoding='utf-8-sig'))]

        return (list_of_dict)
    
    except:
        print('\nUnable to read specified csv\n\n' + csv_location + '\n')
        print('End of the program\n')
        quit()


############################################################################
################################### Step 2 #################################
############################################################################

'''
-- What:
--  Function to check if all the expected columns are present in the csv file specified by the user.
-- Why:
--  Avoid exceptions during the processing of the file due to not recognized keys.
-- How:
--  Test if all the expected columns are present in the list of columns of the first dictionary on the list.
--  Terminates the program if not all the expected columns are found.
'''

def columns_check(list_of_dict):

    list_keys= list(list_of_dict[0].keys())

    expected_keys = ['Source Table/View', 'Target Column', 'Data Target Type', 'Source Column(s)', 'Source Datatype'] 
        
    check = all(item in list_keys for item in expected_keys)

    if check is False:
        print('\nThe specified csv does not have the expected columns, please modify it accordingly\n\n')
        for c in expected_keys:
            print(c)        

        print('\n\nEnd of the program\n')
        quit()


############################################################################
################################### Step 3 #################################
############################################################################

'''
-- What:
--  Function that runs over the list filled with dictionaries creating a dictionary for each Target Column to store associated:
--   1. Each unique Source Table/View.
--   2. Each unique Data Target Type.
--   3. Each unique Source Datatype.
--  If a column dictionary have more than one unique Source Table/View it stored in another dictionary called multiple_column_dict.
-- Why:
--  Identify Target Column with duplicated Source Table/View and not unique Data Target Type & Source Datatype.
-- How:
--  Iterates over the list of dictionaries capturing the Target Column details in a dictionary. Then, append it to the column_dict list.
--  If a column dictionary have more than one unique Source Table/View it stored in the multiple_column_dict.
'''

def init_column_dictionaries(list_of_dict, column_dict, multiple_column_dict):

    for d in list_of_dict:
        if ( d["Source Table/View"] and d["Target Column"]) :
            column_dict[d["Target Column"]]={}
            column_dict[d["Target Column"]]["tables"]=[]
            column_dict[d["Target Column"]]["source_datatype"]=[]
            column_dict[d["Target Column"]]["target_datatype"]=[]

    for d in list_of_dict:
        if ( d["Source Table/View"] and d["Target Column"]):
        
            column_dict[d["Target Column"]]["tables"].append( (d["Source Table/View"]) )    
            
            if (d["Data Target Type"]) not in column_dict[d["Target Column"]]["target_datatype"]:
                column_dict[d["Target Column"]]["target_datatype"].append( (d["Data Target Type"]) )
                
            if (d["Source Datatype"]) not in column_dict[d["Target Column"]]["source_datatype"]:
                column_dict[d["Target Column"]]["source_datatype"].append( (d["Source Datatype"]) )
            
            if len( column_dict[d["Target Column"]]["tables"] ) >1 :
                
                multiple_column_dict.__setitem__( d["Target Column"] , column_dict[d["Target Column"]])
            

############################################################################
################################### Step 4 #################################
############################################################################

'''
-- What:
--  Function that runs over the multiple_column_dict to create a dictionary for each item in it to store:
--   1. Each unique Source Table/View separated by a new line.
--   2. Each unique Data Target Type separated by a new line.
--   3. Each unique Source Datatype separated by a new line.
--   4. The Target Column name
--   5. The Source Table/View concatenated with the Target Column in the Source Column(s) key.
--  Then append the created dictionary to a list called final_dict_list.
-- Why:
--  Create a final list of dictionaries with the modified rows.
-- How:
--  Iterates over the multiple_column_dict storing the deatails of each dictionary in a new dictionary that will be stored in the final_dict_list.
--  Then, appends the orignal dictionaries stored in list_of_dict that are not in multiple_column_dict to the final_dict_list list.
--  Finally sort the dictionaries in final_dict_list by Target Column in descend order/ 
'''

def final_dict_list_filler( final_dict_list ):


    for k,v in multiple_column_dict.items():
        
        new_d = {}

        new_d['Source Table/View'] = '\n'.join(v['tables'])
        
        new_d['Target Column'] = k
                
        new_d['Data Target Type'] = '\n'.join(v['target_datatype'])

        col_list = []
        
        for t in v['tables']:
            col_list.append(t+'.'+k)

        new_d['Source Column(s)'] = '\n'.join(col_list)
        
        new_d['Source Datatype'] = '\n'.join(v['source_datatype'])
        
        final_dict_list.append(new_d)


    for d in list_of_dict:      
        if ( d["Source Table/View"] and not (d["Target Column"] in multiple_column_dict.keys() ) ) :
                       
            final_dict_list.append(d)
                        
        else: 
            continue
               
    
    final_list = sorted(final_dict_list, key=itemgetter('Target Column')) 
    
    return (final_list)


############################################################################
################################### Step 5 #################################
############################################################################

'''
-- What:
--  Function that creates the output of the script.
-- Why:
--  To obtain final .csv file.
-- How:
--  Captures the original path and adds the string Merged_ to the name of the file received as input.
'''

def file_writer(final_list):

    list_keys= list(list_of_dict[0].keys())

    filename = csvLoc

    result = re.search(r"([^\/]+$)", filename)

    new_file_name=filename.replace(result.group(1), "Merged_"+result.group(1))
    
    with open(new_file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = list_keys)
        writer.writeheader()
        writer.writerows( final_list )

    print('\nThe following file was created successfully: \n\n' + new_file_name + '\n')    
    print('End of the program\n')


dictionary = {}
column_dict = {}
multiple_column_dict = {}
final_dict_list = []
final_list = []

list_of_dict = csv_to_dict(csvLoc)

columns_check(list_of_dict)

init_column_dictionaries(list_of_dict, column_dict, multiple_column_dict)

final_list = final_dict_list_filler( final_dict_list )

file_writer(final_list)
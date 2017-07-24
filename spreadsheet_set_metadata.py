#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 10:00:41 2017

@author: jwinton
"""

import pandas as pd
import asset_doctype_creator
import find_plus

# spreadsheet = '/Users/jwinton/Documents/VicNode/MELU/demoIDs.xlsx'
# sheet = 'Sheet1'
spreadsheet = '/Users/jwinton/Documents/VicNode/possums/example_animal_metadata-jw.xlsx'
descriptionSheet = 'Description'
# dataSheet = 'Sheet3'
dataSheet = 'Sheet3'
assetNameCol = "id"

rootNamespace = "/projects/proj-demonstration-1128.4.15/possums"
rootNamespaceName = "/projects"
projectName = "proj-demonstration-1128.4.15"
subnamespace = "possums"
docTypeName = "jaredtestPossum6"
parent = "animal"
uniqueAttributes = ["id","YEAR"]
# docType = "proj-demonstration-1128.4.15:jaredtest"
# description = "Possum project"

full_data = pd.read_excel(spreadsheet, dataSheet, index_row=1, na_values=['NA'])
data_format = pd.read_excel(spreadsheet, descriptionSheet, index_row=1, na_values=['NA'])




# Remove whitespace from headings to allow them to be turned into metadata elements directly
full_data.columns = full_data.columns.str.replace(' ', '_')
full_data.columns = full_data.columns.str.replace('(', '_')
full_data.columns = full_data.columns.str.replace(')', '_')


# Remove whitespace from headings to allow them to be turned into metadata elements directly
data_format.columns = data_format.columns.str.replace(' ', '_')
data_format.columns = data_format.columns.str.replace('(', '_')
data_format.columns = data_format.columns.str.replace(')', '_')


print list(data_format.columns.values)
#
dataTypes = {}
for column in data_format:
    print column
    # print(data_format[column])
    print (data_format[column]['type'])
    # df['MeanTemperatureCT']= df['MeanTemperatureCT'].astype(str)
    # print full_data[column]
    dataTypes.update({column:data_format[column]['type']})
    # if data_format[column]['type'] == 'integer':
    #     full_data[column] = full_data[column].astype(int,errors='ignore')
        # full_data.loc[column] = pd.to_numeric(full_data.loc[column],errors='raise')
print dataTypes
# Turn the pandas dataframe into
# data_format = data_format.to_dict(orient='dict')
# advancedElements = []
#
# for key, value in data_format.items():
#     # print key
#     # print value
#     advElement={}
#     advElement.update({'name':key})
#     advElement.update(value)
#     # print advElement
#     advancedElements.append(advElement)

#Get a list of all of the elements that should be in the doc type
# docTypeElements = []
# for column in full_data:
#     # print column
#     docTypeElements.append(str(column))

#print docTypeElements
# Create the doc type
# asset_doctype_create_fun.create(projectName+":"+docTypeName,description,docTypeElements)

# print full_data
# for i, row in full_data.iterrows():
#     print row


for index, row in full_data.iterrows():
    print row
    # find_id_fun.find(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row)
    # find_id_fun.find_nested(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row,parent)
    # find_id_fun.find_id_nested(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row,parent)
    find_id_fun.find_id_nested_attributes(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row,parent,uniqueAttributes,dataTypes)

# Turn the pandas dataframe into
# full_dict = full_data.to_dict(orient='records')
#print full_dict

# for row in full_dict:
#     print row
#     print row[assetNameCol]
    # find_id_fun.find(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row)


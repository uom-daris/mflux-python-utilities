#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 10:00:41 2017

@author: jwinton
"""

import pandas as pd
import asset_doctype_creator

spreadsheet = '/Users/jwinton/Documents/VicNode/possums/example_animal_metadata-jw.xlsx'
sheet = 'Description'

namespaceCol = "ID"
rootNamespace = "/projects"
projectName = "proj-demonstration-1128.4.15"
docTypeName = "jaredtestPossum6"
parent = "animal"

uniqueAttributes = ["id","YEAR"]

description = "Possum project"

full_data = pd.read_excel(spreadsheet, sheet, index_row=1, na_values=['NA'])

# Remove whitespace from headings to allow them to be turned into metadata elements directly
full_data.columns = full_data.columns.str.replace(' ', '_')
full_data.columns = full_data.columns.str.replace('(', '_')
full_data.columns = full_data.columns.str.replace(')', '_')

#Get a list of all of the elements that should be in the doc type
docTypeElements = []
# for column in full_data:
#     print column
#     dtElement = {}

    # docTypeElements.append(str(column))

#print docTypeElements
# Create the doc type
# asset_doctype_create_fun.create(projectName+":"+docTypeName,description,docTypeElements)

# print full_data
# for i, row in full_data.iterrows():
#     print row

advancedElements = []
advancedAttributes = []

print list(full_data.columns.values)

for column in full_data:
    # print column
    if column in uniqueAttributes:
        print column +" is an attribute"
        advAttribute = {}
        advAttribute.update({'name': column})
        advAttribute.update(full_data[column])
        advancedAttributes.append(advAttribute)
    else:
        print column
        print(full_data[column])
        advElement = {}
        advElement.update({'name': column})
        advElement.update(full_data[column])
        advancedElements.append(advElement)



# Turn the pandas dataframe into
# full_dict = full_data.to_dict(orient='dict')
#
#
# for key, value in full_dict.items():
#     # print key
#     # print value
#     advElement={}
#     advElement.update({'name':key})
#     advElement.update(value)
#     # print advElement
#     advancedElements.append(advElement)
#     # for sub in element:
#     #     print sub
#     # print "test"

#print full_dict

print advancedElements
print advancedAttributes

docType = projectName+":"+docTypeName

# asset_doctype_create_fun.create_advanced(doctype=docType,description=description,elements=advancedElements)


# asset_doctype_create_fun.create_advanced_nested(doctype=docType,description=description,elements=advancedElements,parent=parent)

asset_doctype_creator.create_advanced_nested_attributes(doctype=docType,description=description,elements=advancedElements,parent=parent,uniqueAttributes=advancedAttributes)


# for row in full_dict:
    # print row
    # print row[namespaceCol]
    # create_namespace.create(projectName,rootNamespaceName+"/"+projectName+"/"+row[namespaceCol],projectName+":"+docTypeName,row)

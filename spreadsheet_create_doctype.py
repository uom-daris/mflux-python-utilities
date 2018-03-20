#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import pandas as pd
import asset_doctype_creator
# Configuration variables
import config_spreadsheet_create_doctype as cs



full_data = pd.read_excel(cs.spreadsheet, cs.sheet, index_row=1, na_values=['NA'])

# Remove whitespace from headings to allow them to be turned into metadata elements directly
full_data.columns = full_data.columns.str.replace(' ', '_')
full_data.columns = full_data.columns.str.replace('(', '_')
full_data.columns = full_data.columns.str.replace(')', '_')

advancedElements = []
advancedAttributes = []

print list(full_data.columns.values)

for column in full_data:
    # print column
    if column in cs.uniqueAttributes:
        # print column +" is an attribute"
        advAttribute = {}
        advAttribute.update({'name': column})
        advAttribute.update(full_data[column])
        advancedAttributes.append(advAttribute)
    else:
        # print column
        # print(full_data[column])
        advElement = {}
        advElement.update({'name': column})
        advElement.update(full_data[column])
        advancedElements.append(advElement)

# print advancedElements
# print advancedAttributes

docType = cs.projectName+":"+cs.docTypeName

# asset_doctype_create_fun.create_advanced(doctype=docType,description=description,elements=advancedElements)
# asset_doctype_create_fun.create_advanced_nested(doctype=docType,description=description,elements=advancedElements,parent=parent)
asset_doctype_creator.create_advanced_nested_attributes(doctype=docType,description=cs.description,elements=advancedElements,parent=cs.parent,uniqueAttributes=advancedAttributes)


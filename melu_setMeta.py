#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: jwinton
"""

import pandas as pd
import mfclient
import mf_connect
from xml.sax.saxutils import escape

# spreadsheet = '/Users/jwinton/Documents/VicNode/MELU/file_id_matching/melu_spec_matched_20170822-100105_process_images_dirs.xlsx'
spreadsheet = '/Users/jwinton/Documents/VicNode/Engagements/MELU/all_uploaded2_2.xlsx'
sheet = 'all_uploaded'
# sheet = 'Other_specimens'
# sheet = 'Corymbia&Angophora'
# sheet = 'Banksia_fruit'
# sheet = 'DigiVol#1'


uploaded_col = "Uploaded"

rootNamespace = "/projects/proj-MELU-1128.4.29"

# docType = "proj-demonstration-1128.4.15:jaredtest"
# description = "Possum project"

upl_data = pd.read_excel(spreadsheet, sheet, na_values=['NA'])





# print list(upl_data.columns.values)
#
# dataTypes = {}
# for column in upl_data:
#     print column
#     # print(data_format[column])
#     print (upl_data[column]['type'])
#     # df['MeanTemperatureCT']= df['MeanTemperatureCT'].astype(str)
#     # print full_data[column]
#     # dataTypes.update({column:data_format[column]['type']})
#     # if data_format[column]['type'] == 'integer':
#     #     full_data[column] = full_data[column].astype(int,errors='ignore')
#     # full_data.loc[column] = pd.to_numeric(full_data.loc[column],errors='raise')
#     print dataTypes
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

cxn = mf_connect.connect()

found = []

absent = []

alreadySet = []

try:
    assetsWithMetaQuery = mfclient.XmlStringWriter('args')
    assetsWithMetaQuery.add("where", "namespace >=/projects/proj-MELU-1128.4.29 and xpath (proj-MELU-1128.4.29:SAS_upload) is valid")
    uploaded = cxn.execute("asset.query", assetsWithMetaQuery.doc_text())
    # print uploaded
    assetsWithMeta = uploaded.elements()
    for assetWithMeta in assetsWithMeta:
        # print asset.value()
        alreadySet.append(assetWithMeta.value())

    # > asset.query:where namespace >= / projects / proj - demonstration - 1128.4.15 and xpath(proj - MELU - 1128.4.29:SAS_upload) is valid

    # > asset.set:id 35422605 :meta - action remove <:proj - MELU - 1128.4.29:SAS_upload >

    for index, row in upl_data.iterrows():
        # print row[0]
        stuffs = row[0].split(":")
        # print stuffs
        path = rootNamespace + "/" + stuffs[1] + "/" + stuffs[2]  + "/" + stuffs[3]
        # print path

        # > asset.get:id path = / projects / proj - MELU - 1128.4.29 / Processed_images / Acacia / MELU_D_105497.tif
        # > asset.set:id path = / projects / proj - demonstration - 1128.4.15 / Test_Note_1:meta <:proj - MELU - 1128.4.29:SAS_upload <:uploaded true > >

        sasupl = mfclient.XmlStringWriter('args')
        # sasupl.add("id", '"path='+path+'"')
        path = escape(path)
        sasupl.add("id", 'path=' + path)
        print sasupl.doc_text()
        exists = cxn.execute("asset.exists", sasupl.doc_text())
        if exists.value("exists") == 'true':
            # print "Exists"
            asset = cxn.execute("asset.get",sasupl.doc_text())
            # print asset
            assetElement = asset.element("asset")
            # print assetElement
            assetID = assetElement.attribute("id")
            found.append(assetID)


        else:
            absent.append(path)

        # sasupl.push("meta")
        # sasupl.push("proj-MELU-1128.4.29:SAS_upload")
        # sasupl.add("uploaded", "true")
        # print sasupl.doc_text()


        # print str(index) + " : " + str(row)
        # print "MF ID: " + str(row[1]) + " MELU ID: " + str(row[0])

        # cxn.execute("asset.set", sasupl.doc_text())
        # find_id_fun.find(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row)
        # find_id_fun.find_nested(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row,parent)
        # find_id_fun.find_id_nested(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row,parent)
        # find_plus.find_id_nested_attributes(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row,parent,uniqueAttributes,dataTypes)

finally:
    cxn.close()
    aS = set(alreadySet)
    f = set(found)

    print "Are all of the already set thigns ok? "
    print aS.issubset(f)
    print "All of the things that couldn't be found:"
    for ab in absent:
        print ab



# Turn the pandas dataframe into
# full_dict = full_data.to_dict(orient='records')
#print full_dict

# for row in full_dict:
#     print row
#     print row[assetNameCol]
    # find_id_fun.find(row[assetNameCol],rootNamespaceName+"/"+projectName+"/"+subnamespace,projectName+":"+docTypeName,row)


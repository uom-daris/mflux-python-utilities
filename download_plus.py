#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mfclient
import mf_connect
import csv
import os


# Create connection to MF
cxn = mf_connect.connect()

wsearch = mfclient.XmlStringWriter('args')
wdoctype = mfclient.XmlStringWriter('args')

namespace = '/projects/proj-demonstration-1128.4.15/possums'
localspace = '/Users/jwinton/Desktop/Demo/possums'
doctype = 'proj-demonstration-1128.4.15:jaredtestPossum6'
headings = []
csv_file = "possum_results.csv"
metadataDictionary = []
parent = "animal"


def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        print dict_data
        print csv_columns
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                print data
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return

# From the doctype get a list of headings for the CSV file
wdoctype.add("type",doctype)

dtype = cxn.execute("asset.doc.type.describe",wdoctype.doc_text())

dtypeDefn = dtype.elements("type/definition/element/")


# dtypeDefn = dtype.elements("type/definition/element/element")
print dtypeDefn

for e in dtypeDefn:
    eatr = e.attributes()
    print eatr['name']
    headings.append(eatr['name'])

wsearch.add("where","namespace>="+namespace + " and " + doctype + " has value and asset has content")
wsearch.add('action','get-value')
wsearch.add('xpath',attributes={'ename':'namespace'},value='namespace')
wsearch.add('xpath',attributes={'ename':'name'},value='name')
wsearch.add('xpath',attributes={'ename':'id'},value='id')


results = cxn.execute("asset.query",wsearch.doc_text())

print results

for item in results:
    print item.value('name')
    print item.value('id')
    print item.value('namespace')
    outputs = []
    output_file_path = item.value('namespace')
    output_file_path = output_file_path.replace(namespace, "", 1)
    output_file_path = localspace+output_file_path
    print output_file_path
    ofp = output_file_path+"/"+item.value('name')
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)
    wget = mfclient.XmlStringWriter('args')
    wget.add('id',item.value('id'))
    # wget.add('out','file:'+localspace+"/"+item.value('name'))
    outputs = [mfclient.MFOutput(ofp)] if ofp else None
    # connection.execute("asset.get", w.doc_text(), outputs=outputs)
    print wget.doc_text()
    assetmeta = cxn.execute("asset.get",wget.doc_text(),outputs=outputs)
    print assetmeta
    xmlSidecar = open(output_file_path+"/"+item.value('name')+".xml","w")
    xmlSidecar.write(str(assetmeta))
    xmlSidecar.close()
    # test_results = r.elements("asset/meta/proj-demonstration-1128.4.15:Ping_test/Record")
    possumMeta = assetmeta.element("asset/meta/"+doctype+"/"+parent)
    # print possumMeta
    if possumMeta is not None:
        pMarray = possumMeta.elements()
        pMdict = {}
        # v = pMarray.value('name')

        print pMarray
        for e in pMarray:
            name = e.name()
            value = e.value()
            pMdict.update({name:value})
            # print e.name()
            # print e.value()
        print pMdict
        metadataDictionary.append(pMdict)

WriteDictToCSV(localspace+"/"+csv_file, headings, metadataDictionary)
    # dict(possumMeta)
    # r = possumMeta._elem._children

    # print possumMeta.tostring()
    # print possumMeta.values()





# asset.query :where namespace>='/projects/proj-demonstration-1128.4.15/possums' and (proj-demonstration-1128.4.15:jaredtestPossum hasno value) :action get-value :xpath -ename namespace namespace :xpath -ename name name :xpath -ename id id :output-format csv :out file:/tmp/1.csv

# Get's the file an returns the XML which would then need to be saved, also file name needs to be specified
# > asset.get :id 33613029 :out file:/tmp/1958.txt
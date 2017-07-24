#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 10:00:41 2017

@author: jwinton
"""

import mfclient
import mf_connect

"""
A python module that creates Document types in mediaflux

"""

# A basic document type creator that will create a flat, propagable doctype in which each element is of type string
def create(doctype,description,elements):
    # Create a mediaflux connection
    cxn = mf_connect.connect()

    # dt = mfclient.XmlStringWriter('args')
    # dt.add("type",doctype)

    # match = True
    # dtexists = cxn.execute("asset.doc.type.exists",dt.doc_text())
    # if dtexists.boolean_value("exists"):
    #     mfDType = cxn.execute("asset.doc.type.describe",dt.doc_text())
    #     for element in elements:
    #         dte = mfDType.element("type/definition/" + element)
    #         if dte is None:
    #             match = False

    # if match:
    w = mfclient.XmlStringWriter('args')

    w.add("description",description)
    w.add("create", "true")
    w.add("tag","PROPAGABLE")
    w.add("type",doctype)

    w.push("definition")
    for element in elements:
        w.add("element", "", attributes={"type": "string", "name": str(element)})
    w.pop()

    print w.doc_text()

    cxn.execute("asset.doc.type.update",w.doc_text())

# Creates a more advanced flat, propagable document type that includes element descriptions, instructions and supports
# multiple element types.
# doctype (string) : name of the doctype
# description (string) : description of the doctype
# elements (dictionary) : a dictionary of the elements that will generate the doctype
def create_advanced(doctype, description, elements):
    cxn = mf_connect.connect()

    # dt = mfclient.XmlStringWriter('args')
    # dt.add("type",doctype)

    # match = True
    # dtexists = cxn.execute("asset.doc.type.exists",dt.doc_text())
    # if dtexists.boolean_value("exists"):
    #     mfDType = cxn.execute("asset.doc.type.describe",dt.doc_text())
    #     for element in elements:
    #         dte = mfDType.element("type/definition/" + element)
    #         if dte is None:
    #             match = False

    # if match:
    w = mfclient.XmlStringWriter('args')

    w.add("description", description)
    w.add("create", "true")
    w.add("tag", "PROPAGABLE")
    print str(doctype)
    w.add("type", str(doctype))

    w.push("definition")
    for element in elements:
        attribs = {}
        subAttribs = {}
        # w.add("element", "", attributes={"type": str(element['type']), "name": str(element['name'])})
        for part in element:
            # print str(part)
            # idURLS.update({"icon": iconURL + "&id=" + a})
            # attribs.update({part:element[part]})
            if str(part) == 'description':
                # print "skip"
                subAttribs.update({part:str(element[part])})
            elif str(part) == 'MF_required':
                print "skip"
            elif str(part) == 'instructions':
                subAttribs.update({str(part):str(element[part])})
            # elif str(part) == 'enumerated_values':
            #     if str(element[part]) != 'nan':
            #         attribs.update({str(part): str(element[part])})
            # elif str(part) == 'default':
            #     if str(element[part]) != 'nan':
            #         subAttribs.update({str(part): str(element[part])})
            else :
                print part
                print element[part]
                if str(element[part]) != 'nan':
                    attribs.update({str(part): str(element[part])})
                # attribs.update({str(part): str(element[part])})
        print attribs
        print subAttribs
        w.push ("element", attributes=attribs)
        for sAtrr in subAttribs:
            w.add (sAtrr,subAttribs[sAtrr])
        w.pop()
    # w.push("element","",attribs)
    # w.add(subAttribs)
    # w.pop()
    # w.add("element", "", attributes=attribs)
    w.pop()

    print w.doc_text()

    cxn.execute("asset.doc.type.update", w.doc_text())


# Creates a more advanced doctype that is contained in a parent element to allow for multiple metadata blocks on each
# asset is also propagable, includes element descriptions, instructions and supports multiple element types
# doctype (string) : name of the doctype
# description (string) : description of the doctype
# elements (dictionary) : a dictionary of the elements that will generate the doctype
# parent (string) : the top level parent element
def create_advanced_nested(doctype, description, elements, parent):
    cxn = mf_connect.connect()

    # dt = mfclient.XmlStringWriter('args')
    # dt.add("type",doctype)

    # match = True
    # dtexists = cxn.execute("asset.doc.type.exists",dt.doc_text())
    # if dtexists.boolean_value("exists"):
    #     mfDType = cxn.execute("asset.doc.type.describe",dt.doc_text())
    #     for element in elements:
    #         dte = mfDType.element("type/definition/" + element)
    #         if dte is None:
    #             match = False

    # if match:
    w = mfclient.XmlStringWriter('args')

    w.add("description", description)
    w.add("create", "true")
    w.add("tag", "PROPAGABLE")
    print str(doctype)
    w.add("type", str(doctype))

    w.push("definition")

    w.push("element",attributes={"name":parent,"type":"document","max-occurs":"999999"})

    for element in elements:
        attribs = {}
        subAttribs = {}
        # w.add("element", "", attributes={"type": str(element['type']), "name": str(element['name'])})
        for part in element:
            # print str(part)
            # idURLS.update({"icon": iconURL + "&id=" + a})
            # attribs.update({part:element[part]})
            if str(part) == 'description':
                # print "skip"
                subAttribs.update({part:str(element[part])})
            elif str(part) == 'MF_required':
                print "skip"
            elif str(part) == 'instructions':
                subAttribs.update({str(part):str(element[part])})
            # elif str(part) == 'enumerated_values':
            #     if str(element[part]) != 'nan':
            #         attribs.update({str(part): str(element[part])})
            # elif str(part) == 'default':
            #     if str(element[part]) != 'nan':
            #         subAttribs.update({str(part): str(element[part])})
            else :
                print part
                print element[part]
                if str(element[part]) != 'nan':
                    attribs.update({str(part): str(element[part])})
                # attribs.update({str(part): str(element[part])})
        print attribs
        print subAttribs
        w.push ("element", attributes=attribs)
        for sAtrr in subAttribs:
            w.add (sAtrr,subAttribs[sAtrr])
        w.pop()
    # w.push("element","",attribs)
    # w.add(subAttribs)
    # w.pop()
    # w.add("element", "", attributes=attribs)
    w.pop()
    w.pop()

    print w.doc_text()

    cxn.execute("asset.doc.type.update", w.doc_text())


# Creates a more advanced doctype that is contained in a parent element to allow for multiple metadata blocks on each
# asset that has N attributes which define its uniqueness is also propagable, includes element descriptions,
# instructions and supports multiple element types
# doctype (string) : name of the doctype
# description (string) : description of the doctype
# elements (dictionary) : a dictionary of the elements that will generate the doctype
# parent (string) : the top level parent element
# uniqueAttributes (dictionary) : a dictionary of the elements that form the attributes of the top level element
def create_advanced_nested_attributes(doctype, description, elements, parent, uniqueAttributes):
    cxn = mf_connect.connect()

    # dt = mfclient.XmlStringWriter('args')
    # dt.add("type",doctype)

    # match = True
    # dtexists = cxn.execute("asset.doc.type.exists",dt.doc_text())
    # if dtexists.boolean_value("exists"):
    #     mfDType = cxn.execute("asset.doc.type.describe",dt.doc_text())
    #     for element in elements:
    #         dte = mfDType.element("type/definition/" + element)
    #         if dte is None:
    #             match = False

    # if match:
    w = mfclient.XmlStringWriter('args')

    w.add("description", description)
    w.add("create", "true")
    w.add("tag", "PROPAGABLE")
    print str(doctype)
    w.add("type", str(doctype))

    w.push("definition")

    w.push("element",attributes={"name":parent,"type":"document","max-occurs":"999999"})

    for attrib in uniqueAttributes:
        attribs = {}
        subAttribs = {}
        # w.add("element", "", attributes={"type": str(element['type']), "name": str(element['name'])})
        for part in attrib:
            # print str(part)
            # idURLS.update({"icon": iconURL + "&id=" + a})
            # attribs.update({part:element[part]})
            if str(part) == 'description':
                # print "skip"
                subAttribs.update({part:str(attrib[part])})
            elif str(part) == 'MF_required':
                print "skip"
            elif str(part) == 'max-occurs':
                print "skip"
            elif str(part) == 'instructions':
                subAttribs.update({str(part):str(attrib[part])})
            # elif str(part) == 'enumerated_values':
            #     if str(element[part]) != 'nan':
            #         attribs.update({str(part): str(element[part])})
            # elif str(part) == 'default':
            #     if str(element[part]) != 'nan':
            #         subAttribs.update({str(part): str(element[part])})
            else :
                print part
                print attrib[part]
                if str(attrib[part]) != 'nan':
                    attribs.update({str(part): str(attrib[part])})
                # attribs.update({str(part): str(element[part])})
        print attribs
        print subAttribs
        w.push ("attribute", attributes=attribs)
        for sAtrr in subAttribs:
            w.add (sAtrr,subAttribs[sAtrr])
        w.pop()

    for element in elements:
        attribs = {}
        subAttribs = {}
        # w.add("element", "", attributes={"type": str(element['type']), "name": str(element['name'])})
        for part in element:
            # print str(part)
            # idURLS.update({"icon": iconURL + "&id=" + a})
            # attribs.update({part:element[part]})
            if str(part) == 'description':
                # print "skip"
                subAttribs.update({part:str(element[part])})
            elif str(part) == 'MF_required':
                print "skip"
            elif str(part) == 'instructions':
                subAttribs.update({str(part):str(element[part])})
            # elif str(part) == 'enumerated_values':
            #     if str(element[part]) != 'nan':
            #         attribs.update({str(part): str(element[part])})
            # elif str(part) == 'default':
            #     if str(element[part]) != 'nan':
            #         subAttribs.update({str(part): str(element[part])})
            else :
                print part
                print element[part]
                if str(element[part]) != 'nan':
                    attribs.update({str(part): str(element[part])})
                # attribs.update({str(part): str(element[part])})
        print attribs
        print subAttribs
        w.push ("element", attributes=attribs)
        for sAtrr in subAttribs:
            w.add (sAtrr,subAttribs[sAtrr])
        w.pop()
    # w.push("element","",attribs)
    # w.add(subAttribs)
    # w.pop()
    # w.add("element", "", attributes=attribs)
    w.pop()
    w.pop()

    print w.doc_text()

    cxn.execute("asset.doc.type.update", w.doc_text())


# create_advanced(doctype='proj-demonstration-1128.4.15:jaredtestPossum',description='jared tested',elements=testElements)

# tE = ['ID','Location']
# create(doctype='proj-demonstration-1128.4.15:jaredtest2',description='jared tested',elements=tE)




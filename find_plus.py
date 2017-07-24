#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import mfclient
import mf_connect



cxn = mf_connect.connect()

# r = cxn.execute("server.uuid")
#
# print(r)

#def find(assetContains,namespace,metadata):
#find and set metadata
def find(assetContains,namespace,doctype,metadata):

    w = mfclient.XmlStringWriter('args')
    w.add("where","namespace>="+namespace+" and (xpath(asset/name) contains '"+str(assetContains)+"' )")
        #mfcommand = "asset.query :where namespace>="+namespace+" and (xpath(asset/name) contians"+assetContains+")"
    # print w.doc_text()
    r = cxn.execute("asset.query",w.doc_text())
    # print r
    # print metadata
    for a in r.values("id"):
        print assetContains
        print a
        mdw = mfclient.XmlStringWriter('args')
        mdw.add("id",a)
        mdw.push("meta")
        mdw.push(doctype)
        for element, value in metadata.iteritems():
            # print "Val: "+str(value)
            # print element
            # ele = element
            # val = metadata[element]
            if value and str(value)!='nan':
                mdw.add(str(element),str(value))
        mdw.pop()
        mdw.pop()
        print mdw.doc_text()
        cxn.execute("asset.set",mdw.doc_text())

# find and set metadata with a nested parent element
def find_nested(assetContains, namespace, doctype, metadata, parent):

    w = mfclient.XmlStringWriter('args')
    w.add("where", "namespace>=" + namespace + " and (xpath(asset/name) contains '" + unicode(assetContains) + "' )")
    # mfcommand = "asset.query :where namespace>="+namespace+" and (xpath(asset/name) contians"+assetContains+")"
    # print w.doc_text()
    r = cxn.execute("asset.query", w.doc_text())
    # print r
    # print metadata
    for a in r.values("id"):
        print assetContains
        print a
        mdw = mfclient.XmlStringWriter('args')
        mdw.add("id", a)
        mdw.push("meta")
        mdw.push(doctype)
        mdw.push(parent,attributes={"pid":str(assetContains)})
        for element, value in metadata.iteritems():
            # print "Val: "+str(value)
            # print element
            # ele = element
            # val = metadata[element]
            if value and str(value) != 'nan':
                mdw.add(str(element), str(value))
        mdw.pop()
        mdw.pop()
        mdw.pop()
        print mdw.doc_text()
        cxn.execute("asset.set", mdw.doc_text())

# find by id in metadata not file name
def find_id_nested(id, namespace, doctype, metadata, parent):

    w = mfclient.XmlStringWriter('args')
    w.add("where", "namespace>=" + namespace + " and (xpath(proj-demonstration-1128.4.15:jaredtestPossums/pid) = '" + str(id) + "' )")
    # and (xpath(proj - demonstration - 1128.4.15:jaredtestPossums / pid) = '1958'
    # mfcommand = "asset.query :where namespace>="+namespace+" and (xpath(asset/name) contians"+assetContains+")"
    # print w.doc_text()
    r = cxn.execute("asset.query", w.doc_text())
    # print r
    # print metadata
    for a in r.values("id"):
        print id
        print a
        mdw = mfclient.XmlStringWriter('args')
        mdw.add("id", a)
        mdw.push("meta")
        mdw.push(doctype)
        mdw.push(parent, attributes={"pid": str(id)})
        for element, value in metadata.iteritems():
            # print "Val: "+str(value)
            # print element
            # ele = element
            # val = metadata[element]
            if value and str(value) != 'nan':
                mdw.add(str(element), str(value))
        mdw.pop()
        mdw.pop()
        mdw.pop()
        print mdw.doc_text()
        cxn.execute("asset.set", mdw.doc_text())


# find by id in metadata not file name
def find_id_nested_attributes(id, namespace, doctype, metadata, parent, uniqueAttributes,dataTypes):

    w = mfclient.XmlStringWriter('args')
    w.add("where", "namespace>=" + namespace + " and (xpath(proj-demonstration-1128.4.15:jaredtestPossums/pid) = '" + str(id) + "' )")
    # and (xpath(proj - demonstration - 1128.4.15:jaredtestPossums / pid) = '1958'
    # mfcommand = "asset.query :where namespace>="+namespace+" and (xpath(asset/name) contians"+assetContains+")"
    # print w.doc_text()
    r = cxn.execute("asset.query", w.doc_text())
    # print r
    # print metadata
    for a in r.values("id"):
        print id
        print a
        attributes = {}
        mdw = mfclient.XmlStringWriter('args')
        mdw.add("id", a)
        mdw.push("meta")
        mdw.push(doctype)
        for element, value in metadata.iteritems():
            if value and str(value) != 'nan' and element in uniqueAttributes:
                if dataTypes[element] == "integer":
                    value = int(value)
                print "attrib name: " + str(element)
                print "attrib value: "+ str(value)
                attributes.update({str(element):str(value)})
        mdw.push(parent, attributes=attributes)
        for element, value in metadata.iteritems():
            # print "Val: "+str(value)
            # print element
            # ele = element
            # val = metadata[element]
            if value and str(value) != 'nan' and element not in uniqueAttributes:
                if dataTypes[element] == "integer":
                    value = int(value)
                mdw.add(str(element), str(value))
        mdw.pop()
        mdw.pop()
        mdw.pop()
        print mdw.doc_text()
        cxn.execute("asset.set", mdw.doc_text())


#Find and return URLs
def getURLs(assetContains,namespace,token):

    # iconURL = "https://mediaflux.vicnode.org.au/mflux/icon.mfjp?_token="+token+"&version=1&ext=png&size=480"
    # contentURL = "https://mediaflux.vicnode.org.au/mflux/content.mfjp?_token="+token+"&version=1"
    iconURL = ""
    contentURL = ""
    urls={}
    w = mfclient.XmlStringWriter('args')
    whereClause = "namespace>="+namespace
    i=0
    # "^MELU[ _]?[A-Z]{1}[ _]?6834[a-z]?"
    # "^MELU[ _]?D[ _]?6834[a-z]?"
    for option in assetContains:
        if i == 0:
            whereClause +=" and (xpath(asset/name) contains literal('"+option+"') )"
            i+=1
        else:
            whereClause += " or (xpath(asset/name) contains literal('"+option+"') )"

        # > asset.query:where namespace >= / projects / proj - MELU - 1128.4.29:where(xpath(asset / name) contains literal('MEL'))

    # w.add("where","namespace>="+namespace+" and (xpath(asset/name) contains '"+assetContains+"' )")
    w.add("where",whereClause)
        #mfcommand = "asset.query :where namespace>="+namespace+" and (xpath(asset/name) contians"+assetContains+")"
    print w.doc_text()
    r = cxn.execute("asset.query",w.doc_text())
    print r

    for a in r.values("id"):
        idURLS = {}
        print a
        # aContent =
        assetw = mfclient.XmlStringWriter('args')
        assetw.add("id",a)
        asset = cxn.execute("asset.get",assetw.doc_text())
        name = asset.element("asset/name")
        type = asset.element("asset/type")
        # idURLS.update({"content": contentURL + "&id="+a+"&name="+unicode(name.value())})
        content = contentURL + "&id=" + a + "&name=" + unicode(name.value())
        content = content.encode('utf-8').strip()
        idURLS.update({"content": content})
        print type.value()
        if type.value() == "image/tiff":
            # idURLS.update({"icon":iconURL+"&id="+a+"&name="+unicode(name.value())})
            contentimage = iconURL + "&id=" + a + "&name=" + unicode(name.value())
            contentimage = contentimage.encode('utf-8').strip()
            idURLS.update({"icon": contentimage})
        idu = {a:idURLS}
        urls.update(idu)
    return urls
#    metadata.iteritems()
#     for key in metadata:
#         mfcommand += ":{0} \"{1}\" ".format(str(key), str(metadata[key]))
#     return mfcommand+"> >"

#Find and return URLs
def getURLs_melu(assetContainsParts,namespace,token):

    iconURL = "https://mediaflux.vicnode.org.au/mflux/icon.mfjp?_token="+token+"&version=1&ext=png&size=480"
    contentURL = "https://mediaflux.vicnode.org.au/mflux/content.mfjp?_token="+token+"&version=1"
    urls={}
    w = mfclient.XmlStringWriter('args')
    whereClause = "namespace>="+namespace
    i=0
    # "^MELU[ _]?[A-Z]{1}[ _]?6834[a-z]?"
    # "^MELU[ _]?D[ _]?6834[a-z]?"
    # for option in assetContains:
    #     if i == 0:
    #         whereClause +=" and (xpath(asset/name) contains '"+option+"' )"
    #         i+=1
    #     else:
    #         whereClause += " or (xpath(asset/name) contains '"+option+"' )"

    w.add("where","namespace>="+namespace+" and (xpath(asset/name) contains pattern ('"+assetContainsParts[0]+"[ _]?"+assetContainsParts[1]+"[ _]?"+assetContainsParts[2]+"[a-z]?'))")
    # w.add("where",whereClause)
        #mfcommand = "asset.query :where namespace>="+namespace+" and (xpath(asset/name) contians"+assetContains+")"
    print w.doc_text()
    r = cxn.execute("asset.query",w.doc_text())
    print r
    #
    # for a in r.values("id"):
    #     idURLS = {}
    #     print a
    #     # aContent =
    #     idURLS.update({"content": contentURL+"&id="+a})
    #     assetw = mfclient.XmlStringWriter('args')
    #     assetw.add("id",a)
    #     asset = cxn.execute("asset.get",assetw.doc_text())
    #     type = asset.element("asset/type")
    #     print type.value()
    #     if type.value() == "image/tiff":
    #         idURLS.update({"icon":iconURL+"&id="+a})
    #     idu = {a:idURLS}
    #     urls.update(idu)
    # return urls



#find("jared","/projects/proj-demonstration-1128.4.15")
# print getURLs("jared","/projects/proj-demonstration-1128.4.15","jkl")

# asset.query :where namespace>='/projects/proj-MELU-1128.4.29’ and (xpath(asset/name) contains ‘MELUD’)
# > asset.set :id 33101818 :meta < :proj-vlsci_storage-1128.4.16:jaredtest < :ID "number" :Age "number" :Location "number" :Somethingelse "number" > >

    #
    #
    # w = mfclient.XmlStringWriter('args')
    #
    # w.add("description",description)
    # w.add("create", "true")
    # w.add("tag","PROPAGABLE")
    # w.add("type",doctype)
    #
    # w.push("definition")
    # for element in elements:
    #     w.add("element", "", attributes={"type": "string", "name": str(element)})
    # w.pop()
    #
    # print w.doc_text()
    #
    # cxn.execute("asset.doc.type.update",w.doc_text())

#Find number of assets
def getNumAssets(assetContains,namespace):

    w = mfclient.XmlStringWriter('args')
    w.add("where","namespace>="+namespace+" and (xpath(asset/name) contains '"+assetContains+"' )")
        #mfcommand = "asset.query :where namespace>="+namespace+" and (xpath(asset/name) contians"+assetContains+")"
    r = cxn.execute("asset.query",w.doc_text())
    # print r
    num = r.values("id")
    return len(num)

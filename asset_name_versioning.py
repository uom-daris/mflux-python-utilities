#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 10:00:41 2017

@author: jwinton
"""

import mfclient
import mf_connect
from xml.sax.saxutils import escape

"""
A python module that renames mediaflux assets and copies the name metadata to a versioned metadata chunk

"""


def set_mf_name(namespace):

    # Create a mediaflux connection
    cxn = mf_connect.connect()

    w = mfclient.XmlStringWriter('args')
    w.add("where","namespace>="+namespace+" and mf-name hasno value"
                                          "")
    w.add("size","infinity")
    # mfcommand = "asset.query :where namespace>="+namespace+" and (xpath(asset/name) contians"+assetContains+")"
    # print w.doc_text()
    r = cxn.execute("asset.query",w.doc_text())
    # print r
    for a in r.values("id"):
        # print a
        nameq = mfclient.XmlStringWriter('args')
        nameq.add("where","id="+a)
        nameq.add("action","get-name")
        # assetname = ""
        name = cxn.execute("asset.query", nameq.doc_text())

        if isinstance(name.value('name'), unicode):
            print "skip " + name.value('name')
        else:
            assetname = name.value("name")
            assetname = escape(assetname)
            print name.value("name")
            nameset = mfclient.XmlStringWriter('args')
            nameset.add("id",a)
            nameset.push("meta")
            nameset.push("mf-name")
            # nameset.add("name",name.value("name"))
            nameset.add("name", assetname)
            # print nameset.doc_text()
            cxn.execute("asset.set",nameset.doc_text())

ns = "/projects/proj-MELU-1128.4.29"
# ns = "/projects/proj-demonstration-1128.4.15/audio"
set_mf_name(ns)
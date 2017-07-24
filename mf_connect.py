import mfclient
import config_connect as cc

def connect():

    cxn = mfclient.MFConnection(cc.mfhost, cc.mfport, cc.transport)
    cxn.connect(domain=cc.connect_domain,user=cc.connect_user,password=cc.connect_password)
    return cxn

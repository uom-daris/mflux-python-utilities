#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mfclient
import mf_connect
import socket
import os
import timeit
try:
    import ConfigParser
except:
    import configparser
import io
import pickle
import pickletools
import time


# getting the IP address
if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip

ipaddress = get_lan_ip()

# Load configuration file
with open("ping_test.ini") as f:
    ini_config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(ini_config))

# Get setup information from ini file
location = config.get('pingtest','location')
pingFile = config.get('pingtest','pingFile')
namespace = "/projects/proj-demonstration-1128.4.15/ping_test"
# Set Carbon server details
CARBON_SERVER = config.get('pingtest','CARBON_SERVER')
CARBON_PICKLE_PORT = config.get('pingtest','CARBON_PICKLE_PORT')

# Create mediaflux connection
cxn = mf_connect.connect()

# Connect to Carbon server
sock = socket.socket()
try:
    sock.connect( (CARBON_SERVER, CARBON_PICKLE_PORT) )
except socket.error:
    raise SystemExit("Couldn't connect to %(server)s on port %(port)d, is carbon-cache.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PICKLE_PORT })

# Run metric tests, will do a server.ping, asset.create and a asset.get
try:
    # Server.ping
    # Execute server ping test
    pingResults = cxn.execute("server.ping", inputs=[mfclient.MFInput(pingFile)])

    # Parse XML test results
    size = pingResults.element("size")
    rate = pingResults.elements("rate")
    rateAttribs = rate[0].attributes()
    rateUnits = rateAttribs["units"]

    sizeAttribs = size.attributes()
    sizeBytes = sizeAttribs["bytes"]

    readtime = pingResults.value("read-time")
    readunits = pingResults.value("read-time/@units")


    # Build tuple for (server.ping)
    now = int(time.time())
    tuples = ([])
    tuples.append((unicode('mediaflux-1128.ping.size.bytes'), (now, unicode(sizeBytes))))
    tuples.append((unicode('mediaflux-1128.ping.speed.mbs'), (now, unicode(rate[0].value()))))
    tuples.append((unicode('mediaflux-1128.ping.read.'+readunits), (now, unicode(readtime))))

    # Create package and send it to Carbon
    package = pickle.dumps(tuples, protocol=2)
    size = struct.pack('!L', len(package))
    sock.sendall(size)
    sock.sendall(package)
    pickletools.dis(package)

    # asset.create
    # Create arguments for create asset test
    cAsset = mfclient.XmlStringWriter('args')
    cAsset.push("service", attributes={"name":"asset.create"})
    cAsset.add("namespace",namespace)
    cAsset.add("action","get-meta")
    cAsset.pop()
    cAsset.add("time", True)
    create = pingResults

    def createtest():
        global create
        create = cxn.execute("service.execute",cAsset.doc_text(),inputs=[mfclient.MFInput(pingFile)])

    pythoncreatetime = timeit.timeit(createtest,number=1)

    # Parse XML test results
    asset = create.element("reply/response/asset")
    assetID = create.value("reply/response/asset/@id")
    content = create.element("reply/response/asset/content")
    size = content.value("size")
    copytime = content.value("copy-ctime")
    timetocopy = create.value("time")
    timetocopyunits = create.value("time/@units")
    storeName = content.value("store")
    # Calculate upload rate in bytes/S
    uploadRate = float(size)/float(pythoncreatetime)

    # Build tuple for (asset.create)
    now = int(time.time())
    tuples = ([])
    tuples.append((unicode('mediaflux-1128.create.size.bytes'), (now, unicode(size))))
    tuples.append((unicode('mediaflux-1128.create.speed.bs'), (now, unicode(uploadRate))))
    tuples.append((unicode('mediaflux-1128.create.timeto.'+timetocopyunits), (now, unicode(timetocopy))))
    tuples.append((unicode('mediaflux-1128.create.pythontime.sec'), (now, unicode(pythoncreatetime))))
    tuples.append((unicode('mediaflux-1128.create.store.name'), (now, unicode(storeName))))

    # Create package and send it to Carbon
    package = pickle.dumps(tuples, protocol=2)
    size = struct.pack('!L', len(package))
    sock.sendall(size)
    sock.sendall(package)
    pickletools.dis(package)

    # Download asset to a null file
    dlAsset = mfclient.XmlStringWriter('args')
    dlAsset.push("service", attributes={"name":"asset.get","outputs":"1"})
    dlAsset.add("id", assetID)
    dlAsset.pop()
    dlAsset.add("time",True)
    dlResults = create

    def dltest():
        global dlResults
        dlResults = cxn.execute("service.execute", dlAsset.doc_text(),
                                outputs=[mfclient.MFOutput(file_obj=open(os.devnull, "wb"))])
    # Parse XML test results
    pythondltime = timeit.timeit(dltest,number=1)
    dlAsset = dlResults.element("reply/response/asset")
    dlContent = dlResults.element("reply/response/asset/content")
    dlSize = dlContent.value("size")
    dlCopytime = dlContent.value("copy-ctime")
    timetodownload = dlResults.value("time")
    timetodownloadunits = dlResults.value("time/@units")
    dlStoreName = dlContent.value("store")

    # Calculate download rate
    dlRate = float(dlSize)/float(pythondltime)

    # Build tuple for (asset.get)
    fields = [dlCopytime, location, ipaddress, "asset.get", dlSize, dlRate, "bytes/S", timetodownload, timetodownloadunits, pythondltime, "Sec", dlStoreName, "N/A","N/A"]
    now = int(time.time())
    tuples = ([])
    tuples.append((unicode('mediaflux-1128.get.size.bytes'), (now, unicode(dlSize))))
    tuples.append((unicode('mediaflux-1128.get.speed.bs'), (now, unicode(dlRate))))
    tuples.append((unicode('mediaflux-1128.get.timeto.'+timetodownloadunits), (now, unicode(timetodownload))))
    tuples.append((unicode('mediaflux-1128.get.pythontime.sec'), (now, unicode(pythondltime))))
    tuples.append((unicode('mediaflux-1128.get.store.name'), (now, unicode(dlStoreName))))

    # Create package and send it to Carbon
    package = pickle.dumps(tuples, protocol=2)
    size = struct.pack('!L', len(package))
    sock.sendall(size)
    sock.sendall(package)
    pickletools.dis(package)

    # Remove created asset
    rmAsset = mfclient.XmlStringWriter('args')
    rmAsset.add("id",assetID)
    cxn.execute("asset.destroy",rmAsset.doc_text())

finally:
    cxn.disconnect()
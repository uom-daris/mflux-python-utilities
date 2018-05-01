
import mfclient
import mf_connect
import csv
import time

projSummary = "MFProjectSummary"
storeSummary = "MFStoreSummary"
timestr = time.strftime("%Y%m%d-%H%M%S")

with open(projSummary+timestr+".csv", 'ab') as f:
    header = ["project","allocation","usage"]
    writer = csv.writer(f)
    writer.writerow(header)
    f.close()


with open(storeSummary+timestr+".csv", 'ab') as f:
    header = ["Store","Size","Used","Free"]
    writer = csv.writer(f)
    writer.writerow(header)
    f.close()

# Create mediaflux connection
cxn = mf_connect.connect()

try:
    projsList = cxn.execute("vicnode.project.list")

    print projsList

    for proj in projsList:
        if proj.value() == "proj-cryoem_instrument_data-1128.4.51":
            namespace = "/projects/cryo-em/" + proj.value()
            projDetailsQuery = mfclient.XmlStringWriter('args')
            projDetailsQuery.add("namespace", namespace)
            projDetails = cxn.execute("asset.namespace.describe", projDetailsQuery.doc_text())
            allocation = projDetails.element("namespace/quota/inherited/allocation")
            usage = projDetails.element("namespace/quota/inherited/used")
        else:
            namespace = "/projects/"+proj.value()
            projDetailsQuery = mfclient.XmlStringWriter('args')
            projDetailsQuery.add("namespace", namespace)
            projDetails = cxn.execute("asset.namespace.describe", projDetailsQuery.doc_text())
            allocation = projDetails.element("namespace/quota/allocation")
            usage = projDetails.element("namespace/quota/used")
        print namespace
        # projDetailsQuery = mfclient.XmlStringWriter('args')
        # projDetailsQuery.add("namespace",namespace)
        # projDetails = cxn.execute("asset.namespace.describe",projDetailsQuery.doc_text())
        print projDetails
        # allocation = projDetails.element("namespace/quota/allocation")
        # usage = projDetails.element("namespace/quota/used")
        # Build new line for CSV results file
        # Format project, allocation, used
        fields = [proj.value(), allocation.value(), usage.value()]
        # Write results to file
        with open(projSummary+timestr+".csv", 'ab') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            f.close()

    storesList = cxn.execute("asset.store.list")

    for store in storesList:
        print store
        name = store.value("name")
        print name
        w = mfclient.XmlStringWriter('args')
        w.add("name", name)
        storeDeets = cxn.execute("asset.store.describe",w.doc_text())
        storeTotal = storeDeets.value("store/mount/max-size")
        storeUsed = storeDeets.value("store/mount/size")
        storeFree = storeDeets.value("store/mount/free")
        storeFields = [name, storeTotal, storeUsed, storeFree]
        with open(storeSummary + timestr + ".csv", 'ab') as f:
            writer = csv.writer(f)
            writer.writerow(storeFields)
            f.close()

finally:
    cxn.close()
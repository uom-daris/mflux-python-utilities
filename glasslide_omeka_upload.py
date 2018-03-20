import mfclient
import mf_connect
import omeka_integrator


# > asset.query :size 2000 :where namespace >='/projects/proj-MELU-1128.4.29' :action get-value :xpath -ename name name :xpath -ename namespace namespace :xpath -ename type type

cxn = mf_connect.connect()

doctype = "proj-VSF_Lantern_Glass_Slides-1128.4.47:glass-slide"
namespace = "/projects/proj-VSF_Lantern_Glass_Slides-1128.4.47"

OMEKA_ENDPOINT = 'https://omeka-test.cloud.unimelb.edu.au/omeka14/api/'
OMEKA_APIKEY = 'af245b62482735fb6758c39c7f5ce5369152b91f'
OMEKA_COLLECTION_ID = 14

wsearch = mfclient.XmlStringWriter('args')
wsearch.add("size","1")
wsearch.add("where","namespace>="+namespace + " and " + doctype + " has value and asset has content and (xpath(asset/type) = 'image/jpeg')")
results = cxn.execute("asset.query",wsearch.doc_text())

for result in results:
    print result.value()
    omeka_integrator.omeka_upload(mf_id=result.value(),mf_doctype=doctype,OMEKA_ENDPOINT=OMEKA_ENDPOINT,OMEKA_APIKEY=OMEKA_APIKEY,OMEKA_COLLECTION_ID=OMEKA_COLLECTION_ID,OMEKA_ITEM_ID=55)

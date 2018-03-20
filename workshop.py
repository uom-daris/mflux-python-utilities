# Mediaflux imports
import mfclient
# Helper connection
import mf_connect

#create a connection
cxn = mf_connect.connect()

try:

    # test my first connection, a service with no arguments
    print cxn.execute("server.uuid")


    # get a list of the things I'm looking for using an aterm query, a service with arguments

    # > asset.query :size 2000 :where namespace >='/projects/proj-MELU-1128.4.29'

    # create a variable which will hold the arguments
    query_args = mfclient.XmlStringWriter('args')

    # arguments are in the form of XML
    query_args.add('size', "1000")
    query_args.add("where", "namespace>=/projects/proj-demonstration-1128.4.15")

    # execute the query and store the results in a variable
    asset_IDs = cxn.execute('asset.query', args=query_args.doc_text())
    print asset_IDs

    for asset_ID in asset_IDs:
        # print the element
        print asset_ID
        # print the value
        print asset_ID.vale()
        # print the attribute
        print asset_ID.attribute("version")

    #asset.get :id 35344023
    asset_Get_args = mfclient.XmlStringWriter('args')
    # 33653336
    asset_Get_args.add("id","35344023")
    asset_Meta = cxn.execute('asset.get', args=asset_Get_args.doc_text())
    print asset_Meta

    # compare with aterm result of similar query

    # xpath to find what we want



    # asset.set :id 31277557 :meta < :proj-demonstration-1128.4.15:Ping_test < :Record -date "29-Nov-2016 16:51:27" < :Location "location" :type "ping" :size "100" :rate -Unit "MB/s" "10" > > >
    # Create arguments for create asset test, complicated example
    cAsset = mfclient.XmlStringWriter('args')
    cAsset.add("id","1322")
    cAsset.push("meta")
    cAsset.push("proj-demonstration-1128.4.15:Ping_test")
    cAsset.push("Record",attributes={"date": "29-Nov-2016 16:51:27"})
    cAsset.add("Location","location")
    cAsset.add("type", "ping")
    cAsset.add("size", "100")
    cAsset.add("rate", "10", attributes={"Unit": "MB/s"})
    cAsset.pop()
    cAsset.pop()
    cAsset.pop()

finally:
    cxn.close()
import mfclient

MF_HOST = 'mediaflux.vicnode.org.au'
MF_PORT = 443
MF_SSL = True
MF_DOMAIN = 'VicNode-Admin'
MF_USER = 'provision'
MF_PASSWORD = 'Kjdsar_1287^!'

OMEKA_ENDPOINT = 'https://omeka-test.cloud.unimelb.edu.au/omeka14/api/'
OMEKA_APIKEY = 'af245b62482735fb6758c39c7f5ce5369152b91f'
OMEKA_COLLECTION_ID = 14

TEST_ASSET_PATH = '/projects/proj-VSF_Lantern_Glass_Slides-1128.4.47/999s/cchc999s-00002.jpg'


def main():
    cxn = mfclient.MFConnection(MF_HOST, MF_PORT, MF_SSL)
    try:
        # connect to mediaflux
        cxn.connect(MF_DOMAIN, MF_USER, MF_PASSWORD)

        # get asset metadata
        w1 = mfclient.XmlStringWriter('args')
        w1.add('id', 'path=' + TEST_ASSET_PATH)
        ae = cxn.execute('asset.get', w1.doc_text()).element('asset')
        doc = ae.element('meta/proj-VSF_Lantern_Glass_Slides-1128.4.47:glass-slide')

        # create omeka item
        w2 = mfclient.XmlStringWriter('args')
        w2.add('endpoint', OMEKA_ENDPOINT)
        w2.add('api-key', OMEKA_APIKEY)
        w2.add('collection', OMEKA_COLLECTION_ID)
        # mf metadata -> omeka metadata
        item_type = doc.value('type')
        if item_type:
            w2.push('item_type')
            w2.add('name', item_type.title())
            w2.pop()
        title = doc.value('title')
        if title:
            w2.push('element_text')
            w2.push('element')
            w2.add('name', 'Title')
            w2.pop()
            w2.add('text', title)
            w2.pop()
        subject = doc.value('subject')
        if subject:
            w2.push('element_text')
            w2.push('element')
            w2.add('name', 'Subject')
            w2.pop()
            w2.add('text', subject)
            w2.pop()
        description = doc.value('description')
        if description:
            w2.push('element_text')
            w2.push('element')
            w2.add('name', 'Description')
            w2.pop()
            w2.add('text', description)
            w2.pop()
        creator = doc.value('creator')
        if creator:
            w2.push('element_text')
            w2.push('element')
            w2.add('name', 'Creator')
            w2.pop()
            w2.add('text', creator)
            w2.pop()
        publisher = doc.value('publisher')
        if publisher:
            w2.push('element_text')
            w2.push('element')
            w2.add('name', 'Publisher')
            w2.pop()
            w2.add('text', publisher)
            w2.pop()
        date = doc.value('date')
        if date:
            w2.push('element_text')
            w2.push('element')
            w2.add('name', 'Date')
            w2.pop()
            w2.add('text', date)
            w2.pop()
        contributor = doc.value('contributor')
        if contributor:
            w2.push('element_text')
            w2.push('element')
            w2.add('name', 'Contributor')
            w2.pop()
            w2.add('text', contributor)
            w2.pop()
        rights = doc.value('rights')
        if rights:
            w2.push('element_text')
            w2.push('element')
            w2.add('name', 'Rights')
            w2.pop()
            w2.add('text', rights)
            w2.pop()
        format = doc.value('format')
        if format:
            w2.push('element_text')
            w2.push('element')
            w2.add('name', 'Format')
            w2.pop()
            w2.add('text', format)
            w2.pop()
        re = cxn.execute('omeka.item.create', w2.doc_text())
        item_id = re.value('item/@id')
        print("created omeka item: " + item_id)

        # create omeka file
        w3 = mfclient.XmlStringWriter('args')
        w3.add('endpoint', OMEKA_ENDPOINT)
        w3.add('api-key', OMEKA_APIKEY)
        w3.add('item', item_id)
        w3.add('id', "path=" + TEST_ASSET_PATH)
        re = cxn.execute('omeka.file.create', w3.doc_text())
        file_id = re.value('file/@id')
        print("created omeka file: " + file_id)

    finally:
        cxn.disconnect()


if __name__ == '__main__':
    main()

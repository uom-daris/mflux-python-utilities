import mfclient
import mf_connect
import pandas as pd
import time
import csv
import re as reg
import unicodedata

nameSpace = "/projects/proj-MELU-1128.4.29"
# nameSpace = "/projects/proj-MELU-1128.4.29/Diagrams_illustrations_notes"

# spreadsheet = '/Users/jwinton/Documents/VicNode/MELU/demoIDs.xlsx'
spreadsheet = '/Users/jwinton/Documents/VicNode/MELU/MELUSpecifyDBunique_15june2017-JW-just_IDs.xlsx'
# spreadsheet = '/Users/jwinton/Documents/VicNode/MELU/catalognumbers.xlsx'
# spreadsheet = '/Users/jwinton/Documents/VicNode/MELU/two searchers.xlsx'
asheet = 'a'
abcsheet = 'abc'
assetNameCol = "Catalogue no."
# assetNameCol = "ID"
timestr = time.strftime("%Y%m%d-%H%M%S")


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                # print data
                # print dict_data[data]
                writer.writerow(dict_data[data])
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return

def main():
    results = {}
    cxn = mf_connect.connect()
    rind = 0

    try:
        idx=1
        page_size=20000
        completed=False

        while not completed:
            w = mfclient.XmlStringWriter('args')
            w.add('size', page_size)
            w.add('idx', idx)
            w.add("where", "namespace>=" + nameSpace)
            w.add('action','get-value')
            w.add('xpath','name',{'ename':'name'})
            w.add('xpath', 'namespace', {'ename': 'namespace'})
            w.add('xpath', 'type', {'ename': 'type'})

            re = cxn.execute('asset.query', args=w.doc_text())

            # process the query results here
            aes = re.elements('asset')
            if aes:
                # print "\nAssets paths in current page:"
                for ae in aes:
                    line = {}
                    # print ae.attribute('id')

                    if isinstance(ae.value('name'), unicode):
                        print "skip "+ae.attribute('id')+","+ae.value('name')+","+ae.value('namespace')+","+ae.value('type')
                    else:
                        line.update({'id': ae.attribute('id')})
                        # print ae.value('name')
                        line.update({'name': ae.value('name')})
                        # print ae.value('namespace')
                        # line.update({'namespace': ae.value('namespace')})
                        # line.update({'namespace': unicodedata.normalize('NFKD',ae.value('namespace')).encode('ascii','ignore')})
                        line.update({'namespace': ae.value('namespace')})
                        # print ae.value('type')
                        line.update({'type': ae.value('type')})
                        results.update({rind: line})
                        rind = rind + 1

            remaining = re.int_value('cursor/remaining')
            completed = remaining==0
            idx = re.int_value('cursor/next')
        # print results
        # for result in results:
        #     print result['id']

        matched_results = {}
        spreadsheetorphans = {}
        print len(results)
        # print results.values()
        # print results.keys()

        # for i in results.keys():
        #     print results[i]

        # Strip out all of the a IDs
        full_data = pd.read_excel(spreadsheet, asheet, index_row=1, na_values=['NA'])
        # # print full_data
        # # for row in full_data:
        for index, row in full_data.iterrows():
            # print row[assetNameCol]
            # print row[assetNameCol]
            # print assetID
            if not is_number(row[assetNameCol]):    #and row[assetNameCol] != assetNameCol:

                # When wanting to exclude the trailing letter
                mid3 = row[assetNameCol][5:11]
        #         # print mid3
        #
        #         # if mid3 in "102392":
        #         #     print mid3
        #
        #         # When wanting to include the trailing letter
        #         mid4 = row[assetNameCol ][5:12]
        #         # print mid4
        #
                match = 0
                id_match = r"[^0-9]" + reg.escape(str(mid3)) + r"[^0-9]"
                melu_match = r"^MELU"
                for i in results.keys():
                    if reg.search(melu_match, results[i]['name']) and reg.search(id_match, results[i]['name']):
                    # if mid3 in results[i]['name']:
                        print id_match
                        print results[i]
                        line = {}
                        line.update({'meluID': row[assetNameCol]})
                        line.update({'id': results[i]['id']})
                        line.update({'namespace': results[i]['namespace']})
                        line.update({'name': results[i]['name']})
                        line.update({'type': results[i]['type']})
                        matched_results.update({i: line})
                        results.pop(i)
                        match = 1
                if match == 0:
                    for i in results.keys():
                        mid3 = mid3.lstrip("0")
                        id_match = r"[^0-9]" + reg.escape(str(mid3)) + r"[^0-9]"
                        if reg.search(melu_match, results[i]['name']) and reg.search(id_match, results[i]['name']):
                        # if mid3 in results[i]['name']:
                            print id_match
                            print results[i]
                            line = {}
                            line.update({'meluID': row[assetNameCol]})
                            line.update({'id': results[i]['id']})
                            line.update({'namespace': results[i]['namespace']})
                            line.update({'name': results[i]['name']})
                            line.update({'type': results[i]['type']})
                            matched_results.update({i: line})
                            results.pop(i)
                            match = 1
                    if match == 0:
                        line = {}
                        line.update({'meluID': row[assetNameCol]})
                        spreadsheetorphans.update({index: line})



        print len(results)

        # Strip out all of the abcd... IDs
        full_data2 = pd.read_excel(spreadsheet, abcsheet, index_row=1, na_values=['NA'])
        # # print full_data2
        for index, row in full_data2.iterrows():
            # print row[assetNameCol]
            # print row[assetNameCol]
            # print assetID
            if not is_number(row[assetNameCol]) and row[assetNameCol] != assetNameCol:
                # When wanting to exclude the trailing letter
                # mid3 = row[assetNameCol][5:11]
        #         # print mid3
        #
                # When wanting to include the trailing letter
                mid4 = row[assetNameCol][5:12]
        #         # print mid4
                match = 0
                id_match = r"[^0-9]" + reg.escape(str(mid4)) + r"[^0-9]"
                melu_match = r"^MELU"
                for i in results.keys():
                    if reg.search(melu_match, results[i]['name']) and reg.search(id_match, results[i]['name']):
                    # if mid4 in results[i]['name']:
                        print id_match
                        print results[i]
                        line = {}
                        line.update({'meluID': row[assetNameCol]})
                        line.update({'id': results[i]['id']})
                        line.update({'namespace': results[i]['namespace']})
                        line.update({'name': results[i]['name']})
                        line.update({'type': results[i]['type']})
                        matched_results.update({i: line})
                        results.pop(i)
                        match = 1
                if match == 0:
                    for i in results.keys():
                        mid4 = mid4.lstrip("0")
                        id_match = r"[^0-9]" + reg.escape(str(mid4)) + r"[^0-9]"
                        if reg.search(melu_match, results[i]['name']) and reg.search(id_match, results[i]['name']):
                        # if mid4 in results[i]['name']:
                            print id_match
                            print results[i]
                            line = {}
                            line.update({'meluID': row[assetNameCol]})
                            line.update({'id': results[i]['id']})
                            line.update({'namespace': results[i]['namespace']})
                            line.update({'name': results[i]['name']})
                            line.update({'type': results[i]['type']})
                            matched_results.update({i: line})
                            results.pop(i)
                            match = 1
                    if match == 0:
                        line = {}
                        line.update({'meluID': row[assetNameCol]})
                        spreadsheetorphans.update({index: line})

        print len(results)
        # csv_file = "melu_objs_not_a_match_" + timestr + ".csv"
        # WriteDictToCSV(csv_file, ['id', 'namespace', 'name', 'type'], final_results)
        csv_file = "melu_spec_not_a_match_" + timestr + ".csv"
        WriteDictToCSV(csv_file, ['id','namespace','name','type'], results)
        csv_matched_file = "melu_spec_matched_" + timestr + ".csv"
        WriteDictToCSV(csv_matched_file, ['meluID','id','namespace','name','type'], matched_results)
        spreadsheetorphans_file = "melu_spec_orphaned_" + timestr + ".csv"
        WriteDictToCSV(spreadsheetorphans_file, ['meluID'], spreadsheetorphans)


    finally:
        cxn.disconnect()
        # print len(final_results)




if __name__ == '__main__':
    main()


# > asset.query :size 2000 :where namespace >='/projects/proj-MELU-1128.4.29' :action get-value :xpath -ename name name :xpath -ename namespace namespace :xpath -ename type type
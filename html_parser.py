from bs4 import BeautifulSoup
import pprint
class htmlParser():

    def __init__(self, html):
        self.htmlObj = BeautifulSoup(html, 'html.parser')

    def parse_txn_details(self, txnHtml):
        txnObj = {}
        navigator = txnHtml.tr
        txnObj['refCode'] = navigator.contents[1].contents[0]
        navigator = navigator.next_sibling
        txnObj['pmntMthd'] = navigator.contents[1].contents[0]
        navigator = navigator.next_sibling
        txnObj['dateTime'] = navigator.contents[1].contents[0]
        navigator = navigator.next_sibling
        coinAmt = navigator.contents[1].strong.contents[0]
        coinAmt = coinAmt.split()
        txnObj['coinName'] = coinAmt[1]
        txnObj['coinAmt'] = coinAmt[0]
        navigator = navigator.next_sibling
        txnObj['exchgRate'] = navigator.contents[1].contents[0].split()[1]
        navigator = navigator.next_sibling
        txnObj['amtBght'] = navigator.contents[1].contents[0]
        navigator = navigator.next_sibling
        txnObj['fee'] = navigator.contents[1].contents[0]
        navigator = navigator.next_sibling
        txnObj['ttlSpnt'] = navigator.contents[1].contents[0]
        return txnObj

    def get_txn_details(self):
        try:
            mainTable = self.htmlObj.table.next_sibling
            tableBody = mainTable.tbody
            mainRow = tableBody.tr.next_sibling
            mainRowZoomed = mainRow.td.table.tbody.tr
            txnDetails = mainRowZoomed.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.table.tbody
            return self.parse_txn_details(txnDetails)
        except:
            return

        


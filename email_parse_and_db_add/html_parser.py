from bs4 import BeautifulSoup
from datetime import date, datetime
import time
import dateutil.parser as parser

class htmlParser():

    def __init__(self, html):
        self.htmlObj = BeautifulSoup(html, 'html.parser')

# Function to parse the html in order to extract the useful information from the html. Returns an object with all the required fields.
    def parse_txn_details(self, txnHtml):
        # HTML parsing and adding information to the returned object based on values from the parsed html.
        txnObj = {}
        navigator = txnHtml.tr
        txnObj['refCode'] = str(navigator.find_all("td")[1].span.contents[0])
        
        navigator = navigator.find_next_sibling("tr")
        txnObj['pmntMthd'] = str(navigator.find_all("td")[1].contents[0])
        
        navigator = navigator.find_next_sibling("tr")
        dateTime = navigator.find_all("td")[1].contents[0]
        dateTime = dateTime.rsplit(' ', 1)[0]
        dateTimeObj = datetime.strptime(dateTime, "%B %d, %Y %H:%M")
        txnObj['date'] = str(dateTimeObj.strftime("%Y-%m-%d %H:%M:%S"))
        navigator = navigator.find_next_sibling("tr")
        coinAmt = navigator.find_all("td")[1].strong.contents[0]
        coinAmt = coinAmt.split()
        txnObj['coinName'] = str(coinAmt[1])
        txnObj['coinAmt'] = str(coinAmt[0])
        
        navigator = navigator.find_next_sibling("tr")
        # Remove the dollar sign and the comma to allow later calculations on this object.
        txnObj['exchgRate'] = str(navigator.find_all("td")[1].contents[0].split()[1].replace('$', '').replace(',', ''))
        
        navigator = navigator.find_next_sibling("tr")
        txnObj['amtBght'] = str(navigator.find_all("td")[1].contents[0].replace(
            '$', '').replace(',', ''))
        
        navigator = navigator.find_next_sibling("tr")
        txnObj['fee'] = str(navigator.find_all("td")[1].contents[0].replace(
            '$', '').replace(',', ''))
        
        navigator = navigator.find_next_sibling("tr")
        txnObj['ttlSpnt'] = str(navigator.find_all("td")[1].contents[0].replace(
            '$', '').replace(',', ''))
        return txnObj

# Function to check if the html template is valid. Also calls parse_txn_details if html is valid.
    def get_txn_details(self):
        # Try statement to make sure the entire program doesn't crash if the appropriate template is not found.
        # print(self.htmlObj.table.tbody.tr.td)
        try:
        # HTML parsing based on the Coinbase html template.
            mainTable = self.htmlObj.table.tbody.tr.td.table.tbody.tr.td.table.find_next_sibling(
                "table")
            tableBody = mainTable.tbody
            mainRow = tableBody.tr.find_next_sibling("tr")
            mainRowZoomed = mainRow.td.table.tbody.tr
            txnDetails = mainRowZoomed.find_next_siblings("tr")[5].td.table.tbody
            return self.parse_txn_details(txnDetails)
        except:
            # print(self.htmlObj)
            return

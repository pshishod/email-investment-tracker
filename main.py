from fetchEmails import fetchEmail
from html_parser import htmlParser
# Create file to save credentials, if not exists. If exists, read them into the email and password credentials.
fetch = fetchEmail()
# list_messages has to be called first because it makes a list of all the required emails, which is then used in the get_html function.
fetch.list_messages()

htmls = fetch.get_html()

allTxnDetails = []
for i in htmls:
    parser = htmlParser(i)
    allTxnDetails.append(parser.get_txn_details())

print(allTxnDetails)





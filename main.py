from fetchEmails import fetchEmail
from html_parser import htmlParser

# Calling fetchEmail class, which will be looking for a credentials file in the same directory.
# After that is validated, a token file will initially be created after a web sign in into gmail.
# The token file is used for automatic authentication after the initial login.
fetch = fetchEmail()

# list_messages has to be called first because it makes a list of all the required emails, which is then used in the get_html function.
fetch.list_messages()

# Returns a list of all the emails matched from the query in an html format. (query file needed)
htmls = fetch.get_html()

# List to hold the transaction details in a dictionary format for all the emails. 
# If there were some emails with incorrect formatting, the list will include 'None' in its place.
allTxnDetails = []
for i in htmls:
    parser = htmlParser(i)
    txn_details = parser.get_txn_details()
    if not txn_details == None:
        allTxnDetails.append(txn_details)

print(allTxnDetails)





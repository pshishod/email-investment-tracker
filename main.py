from fetchEmails import fetchEmail
from html_parser import htmlParser
import mysql.connector as connector
from dbInteraction import dbInteract

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

# Store the credentials in this array to connect to the local mysql database
credentials = []
with open("./database_credentials", "r") as file:
    for line in file:
        credentials.append(line)
file.close()

cnx = connector.connect(user=credentials[0], password=credentials[1], host='127.0.0.1', database='investment')
db = dbInteract(cnx)
for i in htmls:
    parser = htmlParser(i)
    txn_details = parser.get_txn_details()
    if not txn_details == None:
        allTxnDetails.append(txn_details)

for i in allTxnDetails:
    db.insert_into_db(i)

# Commit all the changes to the database and close the connection
cnx.commit()
cnx.close()         




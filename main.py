from fetchEmails import fetchEmail
# Create file to save credentials, if not exists. If exists, read them into the email and password credentials.
fetch = fetchEmail()
# list_messages has to be called first because it makes a list of all the required emails, which is then used in the get_html function.
fetch.list_messages()

fetch.get_html()




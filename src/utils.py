import difflib
import dropbox
from dotenv import load_dotenv
import os

dbx = dropbox.Dropbox(os.getenv("DBX_TOKEN"))

for entry in dbx.files_list_folder('').entries:
    print(entry.name)

def  closestMatch(query):
    difflib.get_close_matches(query, )





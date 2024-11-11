import difflib
import dropbox
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("DBX_TOKEN"))
dbx = dropbox.Dropbox(os.getenv("DBX_TOKEN"))

#puts dbx contents into list
files = [file.name for file in dbx.files_list_folder('').entries]

# finds closest match with the entry lists
def  closestMatch(query):
    print(difflib.get_close_matches(query, files, n=1, cutoff=0.1))
    
def searchFile(query):
    dbx.files_search("", query)

print(files)
closestMatch("Gu")
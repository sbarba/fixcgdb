import os
import requests
import glob2
from bs4 import BeautifulSoup as bs4

base_url = 'http://localhost:8888/fixcgdb/'
cwd = os.path.dirname(os.path.realpath(__file__)) + '/' # The path to this file

def clean_up():
    for file in glob2.glob(cwd + '../../files/*'):
        os.remove(file)

def upload_and_fix(path):
  '''
  Uploads and fixes files.
  '''
  session = requests.Session()
  session.get(base_url + 'upload.php?fileName=' + os.path.basename(path)  + '&fileContent=' + open(path).read().replace('&', '%26'))
  fixer_response = session.get(base_url + 'fixer.php')
  return(session, fixer_response)

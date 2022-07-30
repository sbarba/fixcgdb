#!/usr/bin/env python3

from cleartest import *
import requests
from bs4 import BeautifulSoup as bs4
import common

def index():
  response = requests.get(common.base_url)
  soup = bs4(response.text, 'html.parser')

  equals(soup.title.text, 'CardGameDB -> OCTGN', 'Title ok')
  not_ok(soup.select_one('[data-test="upload-label"]').has_attr('hidden'), 'Upload label is visible')
  ok(soup.select_one('[data-test="upload-button"]').has_attr('hidden'), 'Upload button is not visible')
  ok(soup.select_one('[data-test="upload-area"]').has_attr('disabled'), 'Upload area is disabled')
  equals('', soup.select_one('[data-test="upload-area"]').text, 'Upload area is empty')
  ok(soup.select_one('[data-test="download-area"]').has_attr('disabled'), 'Download area is disabled')
  equals('Fixed objective sets will appear here.', soup.select('[data-test="download-area"]')[0].text, 'Download area text correct')
  is_in('stevepop', soup.text, 'stevepop is on the page')

def test_main(plan=8):
  index()

if __name__ == '__main__':
  go()

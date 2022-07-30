#!/usr/bin/env python3

from cleartest import *
import requests
import glob2
import common

def invalid_uploads():
  cases = [{
    'description': 'Empty file',
    'file': 'files/empty_file.o8d',
    'expected_fixer_response': 'Invalid File'
  }, {
    'description': 'No fixes necessary',
    'file': 'files/expected_fixed_multi_fix.o8d',
    'expected_fixer_response': 'No fixes necessary'
  }, {
    'description': 'File too big',
    'file': 'files/too_big.md',
    'expected_fixer_response': 'Invalid File'
  }, {
    'description': 'Binary file',
    'file': 'files/binary.o8d',
    'expected_fixer_response': 'Invalid File'
  }, {
    'description': 'Not XML',
    'file': 'files/not_xml.txt',
    'expected_fixer_response': 'Invalid File'
  }, {
    'description': 'XML, but not o8d',
    'file': 'files/valid_xml_but_not.o8d',
    'expected_fixer_response': 'Invalid File'
  }, {
    'description': 'o8d, but not SW',
    'file': 'files/valid_netrunner.o8d',
    'expected_fixer_response': 'Invalid File'
  }, {
    'description': 'Bad Objective name',
    'file': 'files/bad_objective_name.o8d',
    'expected_fixer_response': 'Invalid File'
  }]

  for case in cases:
    session, fixer_response = common.upload_and_fix(case['file'])
    equals(fixer_response.text, case['expected_fixer_response'], case['description'] + ": Fixer response is 'Invalid File'")

    download_response = session.get(common.base_url + 'download.php')
    equals('', download_response.text, case['description'] + ': download.php returns nothing.')

def test_main(plan=18):
  invalid_uploads()
  equals(requests.get(common.base_url + 'fixer.php').text, 'Invalid File', "Requesting fixer.php directly returns 'Invalid File'.")
  equals(requests.get(common.base_url + 'download.php').text, '', 'Requesting download.php returns an empty body.')  

if __name__ == '__main__':
  go()

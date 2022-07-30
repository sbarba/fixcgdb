#!/usr/bin/env python3

from cleartest import *
import common

def content(filename):
  # newline='' is there so that Python doesn't convert CRLF to LF.
  return open(filename, newline='').read()

def end_to_end_fixes():
  cases = [{
      'description': 'One fix',
      'file':   'files/one_fix.o8d',
      'expected_fixer_response': content('files/expected_one_fix_fixer_response.o8d'),
      'expected_download_response': content('files/expected_one_fix_download_response.o8d'),
  }, {
      'description': 'Multiple fixes',
      'file': 'files/multi_fix.o8d',
      'expected_fixer_response': content('files/expected_multi_fix_fixer_response.o8d'),
      'expected_download_response': content('files/expected_multi_fix_download_response.o8d')
  }, {
      'description': 'Curly quotes',
      'file': 'files/curly_quote.o8d',
      'expected_fixer_response': content('files/expected_curly_quote_fixer_response.o8d'),
      'expected_download_response': content('files/expected_curly_quote_download_response.o8d')
  }, {
      'description': 'UTF-8 file name',
      'file': 'files/漢字.o8d',
      'expected_fixer_response': content('files/expected_漢字_fixer_response.o8d'),
      'expected_download_response': content('files/expected_one_fix_download_response.o8d')
  }]

  for case in cases:
      # Upload & fix.
      session, fixer_response = common.upload_and_fix(case['file'])

      # Check fixer.php's response.
      equals(fixer_response.text, case['expected_fixer_response'], case['description'] + ': Fixer response correct')

      # Check download.php's response.
      download_response = session.get(common.base_url + 'download.php')
      equals(download_response.text, case['expected_download_response'], case['description'] + ': Downloaded file correct')

def test_main(plan=8):
  end_to_end_fixes()

if __name__ == '__main__':
  go()

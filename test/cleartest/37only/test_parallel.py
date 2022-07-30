#!/usr/bin/env python3

'''
This is a pared-down version of test_end_to_end.py for checking that users can hit the server simultaneously.
I had to remove the check of the downloaded file since a process could make one before an earlier one has had
a chance to check its own. For now it only runs in Python 3.7 or earlier. I had to use pyenv & virtualenv to
test it.

Run this with the -m option to avoid jumbled output. You could put minimal=True in go() to set it in stone.
'''

from cleartest import *
import common

def end_to_end_fixes():
  cases = [{
      'description': 'One fix',
      'file': common.filedir + 'one_fix.o8d',
      'expected_upload_response': open(common.filedir + 'one_fix.o8d').read(),
      'expected_download_area': 'Fixed Objective Sets:\n    - Superior Numbers\n\nfixed_one_fix.o8d:\n\n' + open(common.filedir + 'expected_fixed_one_fix.o8d').read()
  }, {
      'description': 'Multiple fixes',
      'file': common.filedir + 'multi_fix.o8d',
      'expected_upload_response': open(common.filedir + 'multi_fix.o8d').read(),
      'expected_download_area': 'Fixed Objective Sets:\n    - A Hero\'s Journey\n    - A Deep Commitment\n\nfixed_multi_fix.o8d:\n\n' + open(common.filedir + 'expected_fixed_multi_fix.o8d').read()
  }]

  for case in cases:
      # Upload & fix.
      session, upload_response, fixer_response = common.upload_and_fix(case['file'])
      equals(upload_response.text, case['expected_upload_response'], case['description'] + ': Upload response correct')

      # Compare server response text to download_area w/expected text.
      # The former has Windows line endings so the CRs are stripped for the comparison.
      equals(fixer_response.text.replace('\r', ''), case['expected_download_area'], case['description'] + ': Fixer response correct')

      # Download & check status code.
      download_response = session.get(common.base_url + 'download.php')
      equals(200, download_response.status_code, case['description'] + ': Download status 200.')

def test_main(plan=6):
  end_to_end_fixes()

if __name__ == '__main__':
  go(parallel=16)

#!/usr/bin/env python3

'''
This is just an example for myself where I use asyncio in the test script to run functions concurrently.
I think Python is blocking on file I/O though otherwise 'downloaded.o8d' would get overwritten occasionally
by a process before the original could check it.
'''

from cleartest import *
import filecmp
import asyncio
import common

async def end_to_end_fixes():
  cases = [{
    'description': 'One fix',
    'file': common.filedir + 'one_fix.o8d',
    'expected_fixed_file': common.filedir + 'expected_fixed_one_fix.o8d',
    'expected_download_area': 'Fixed Objective Sets:\n    - Superior Numbers\n\nfixed_one_fix.o8d:\n\n' + open(common.filedir + 'expected_fixed_one_fix.o8d').read()
  }, {
    'description': 'Multiple fixes',
    'file': common.filedir + 'multi_fix.o8d',
    'expected_fixed_file': common.filedir + 'expected_fixed_multi_fix.o8d',
    'expected_download_area': 'Fixed Objective Sets:\n    - A Hero\'s Journey\n    - A Deep Commitment\n\nfixed_multi_fix.o8d:\n\n' + open(common.filedir + 'expected_fixed_multi_fix.o8d').read()
  }]

  shuffle(cases)
  for case in cases:
    # Upload & fix.
    session, fixer_response = common.upload_and_fix(case['file'])

    # Compare server response text to download_area w/expected text.
    # The former has Windows line endings so the CRs are stripped for the comparison.
    equals(fixer_response.text.replace('\r', ''), case['expected_download_area'], case['description'] + ': Fixer response correct')

    # Download & check status code.
    download_response = session.get(common.base_url + 'download.php')
    equals(200, download_response.status_code, case['description'] + ': Download status 200.')

    # Write response content to a file & check against file with expected content.
    open(common.filedir + 'downloaded.o8d', 'wb').write(download_response.content)
    ok(filecmp.cmp(common.filedir + 'downloaded.o8d', case['expected_fixed_file']), case['description'] + ': Downloaded file correct')

async def run_async():
  funcs = []
  for i in range(4):
    funcs.append(end_to_end_fixes())
  await asyncio.gather(*funcs)

def test_main(plan=24):
  asyncio.run(run_async())

if __name__ == '__main__':
  go(minimal=True)

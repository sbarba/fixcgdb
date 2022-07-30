#!/usr/bin/env python3

import subprocess
from cleartest import go
import common

print('Deleting leftover uploaded & fixed files...')
common.clean_up()
print('Starting MAMP...\n')
subprocess.call(['/Applications/MAMP/bin/start.sh >/dev/null 2>&1'], shell=True)

results = go(paths=['test_index.py', 'test_positives.py', 'test_negatives.py'])

print(f'\nFunctional: {results.plan} tests planned. {results.passed} tests passed.')

print('Stopping MAMP...')
subprocess.call(['/Applications/MAMP/bin/stop.sh >/dev/null 2>&1'], shell=True)
print('Deleting leftover uploaded & fixed files...')
common.clean_up()

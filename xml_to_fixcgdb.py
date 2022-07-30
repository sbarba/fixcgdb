#!/usr/bin/python

'''
Makes fixcgdb json from an OCTGN XML file. Redirect results to somewhere useful. Example:

    ./make_list.py set.xml > evasive.json

Takes set.xml and makes evasive.json.
'''

import sys
import xml.etree.ElementTree as xml

tree =  xml.parse(sys.argv[1])
set = tree.getroot()

print '    {'
print '        "name": "%s",' % set.attrib['name']
print '        "id": "%s",' % set.attrib['id']
print '        "cgdb": "%s",' % set.attrib['name'].lower().replace(" ", "-")

pack = []
for cards in set:
    for card in cards:
        card_dict = card.attrib
        for property in card:
            card_dict[property.attrib['name']] = property.attrib['value']
        pack.append(card_dict)

print '        "cards": ['

i = 0
for card in pack:
    name = card.pop('name')
    name = name.replace('"', "'")
    
    id = card.pop('id')
    type = card.pop('Type')
    
    line = '            {"name": "%s", "id": "%s"' % (name, id)
    if type == 'Objective':
        line += ', "type": "objective"'

    line += '}'
    if i < len(pack) - 1:
        line += ','
    print line
    i += 1

print '        ]'
print '    }'


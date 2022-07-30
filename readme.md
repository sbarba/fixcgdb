#### Flow summary

1. User clicks "Choose .o8d file".
2. upload.php uploads the file and echoes its contents back to index.html.
3. fixer.php fixes the file by referencing octgn.json, saving the fixed file, and
   echoing it to index.html.
4. download.php downloads the file.


#### Files and Directories

* index.html is the main page and the only one the user interacts with.
* fixcgdb.css has the styles.
* fixcgdb.js makes the page go.
* upload.php is the script that uploads the file and echoes its contents to
  index.html.
* fixer.php is the script that fixes the file, saves it, and echoes its contents
  to index.html
* octgn.json is the JSON reference that fixer.php uses to fix the file.
* download.php is the script that downloads the fixed file to the user's machine.
* files/ is the directory where uploaded files go. The empty index.html is there on purpose.


#### Updating octgn.json for a new pack

1. Navigate to repo:

  $ cd ~/code/shell/alert_script/Star-Wars-LCG-OCTGN/o8g/Sets/

2. Get up-to-date:

 $ git pull 

3. Navigate to site's home directory:

   $ cd /Applications/MAMP/htdocs/fixcgdb

4. Open octgn.json and put a comma and a newline after the last curly brace.
5. Run xml_to_fixcgdb.py against the pack's set.xml file, e.g.

   $ ./xml_to_fixcgdb.py "~/code/shell/alert_script/Star-Wars-LCG-OCTGN/o8g/Sets/The Forest Moon/set.xml"

6. Copy the output and paste it into octgn.json on the line from step 4.
7. Update index.html with latest set's name.
8. Add & Commit:

   $ git add index.html octgn.json
   $ git commit -m "Updated for The Forest Moon" or whatever.

9. Push

   $ git push

10. scp index.html & octgn.json to dreamhost. I have a shell script called deploycg for this (deploycg index.html; deploycg octgn.json).

   $ scp userid@server:deckply.com/fixcgdb/

#### Example update for steps 4-6


This:
```
        ...
            {"name": "Spice Blitz", "id": "ff4fb461-8060-457a-9c16-000000001229"},
            {"name": "Hallucination", "id": "ff4fb461-8060-457a-9c16-000000001230"}
        ]
    }
]
```

becomes this:
```
         ...
            {"name": "Spice Blitz", "id": "ff4fb461-8060-457a-9c16-000000001229"},
            {"name": "Hallucination", "id": "ff4fb461-8060-457a-9c16-000000001230"}
        ]
    },
    {
        "name": "New Alliances",
        "id": "e1fcc3c7-64f4-4875-814c-b2b552abab73",
        "cgdb": "new-alliances",
        "cards": [
            {"name": "Out of Their Element", "id": "ff4fb461-8060-457a-9c16-000000001195", "type": "objective"},
...
]
```

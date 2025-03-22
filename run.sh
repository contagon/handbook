#!/bin/sh

# Run the script twice just to make sure we didn't miss any downloads
python execute.py download --date all
python execute.py download --date all
python execute.py missing --fill
python execute.py sanitize --date all
#!/bin/sh

# Run the script twice just to make sure we didn't miss any downloads
python run.py download --date all
python run.py download --date all
python run.py missing --fill
python run.py sanitize --date all
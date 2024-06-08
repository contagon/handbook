#!/bin/sh

# Run the script twice just to make sure we didn't miss any downloads
python run.py --kind download --date all
python run.py --kind download --date all
python run.py --kind missing --fill
python run.py --kind sanitize --date all
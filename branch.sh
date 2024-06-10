#!/bin/bash

# Delete previous branch version
git checkout master
git push -d origin diff
git branch -D diff
for dir in 202*; do
    git tag -d ${dir}
    git push origin --delete ${dir}
done

# Remove links
python run.py sanitize --date all --rm-links

# Create new branch
git checkout -b diff
git rm --cached -r 202*
git commit add .
git commit -m "Remove md directories"

# Make all commits & tags
for dir in 202*; do
    rm -rf handbook
    mv $dir handbook
    git add handbook
    git commit -m "${dir} Edition"
    git tag -a ${dir} -m "${dir} Edition"
done

# Push changes
git push -u origin diff
git push --tags
git checkout master
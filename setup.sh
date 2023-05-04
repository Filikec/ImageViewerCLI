#!/bin/bash

# Set the filename variable
filename="./viewer.py"

# Make the file executable
chmod +x "$filename"

# Set the new filename
newname="imviewer"

# Rename the file
mv "$filename" "$newname"

# Copy the file to the /usr/bin directory
cp "$newname" /usr/bin/
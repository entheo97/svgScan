#!/usr/bin/env python3
import re
from pathlib import Path

# Find the folder where this script is saved
script_dir = Path(__file__).parent

# Build full path to testImage.svg
file_path = script_dir / "testImage.svg"

# Context manager opens, reads, stores and closes file
with open(file_path, "r", encoding="utf-8") as file: # reads svg file which are encoded in utf-8
    text = file.read()

# Lazy match for <!-- ... -->; DOTALL lets it span multiple lines
# .*? = any characters (.) repeated zero or more times (*), as few as possible (?)
comments = re.findall(r"<!--(.*?)-->", text, re.DOTALL)

for counter, comment_text in enumerate(comments, start=1):
    print(f"Comment {counter}: {comment_text.strip()}")

if not comments:
    print("No comments found.")

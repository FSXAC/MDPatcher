import re

# Contains the regex for markdown stuff
RE_TRIPLE_DASH = re.compile(r'^---\s*$')
# RE_FRONT_MATTER = re.compile(r'^---\s*$((?:.|\n)*)*^---\s*$', re.MULTILINE)
RE_ALL_HEADERS = re.compile(r'^(#{1,6})\s?(.+)$')

RE_TOC = re.compile(r'^\[(toc|TOC)\]$')

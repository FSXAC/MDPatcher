import re

# Contains the regex for markdown stuff
RE_TRIPLE_DASH = re.compile(r'^---\s*$')
# RE_FRONT_MATTER = re.compile(r'^---\s*$((?:.|\n)*)*^---\s*$', re.MULTILINE)
RE_ALL_HEADINGS = re.compile(r'^(?:#{1,6})\s?(.+)$')
RE_ALL_BAD_HEADINGS = re.compile(r'^(#{1,6})([^ \n#].+)$')

RE_TOC = re.compile(r'^\[(toc|TOC)\]$')

RE_SINGLE_LATEX = re.compile(r'(^|[^\\^\$])\$([^\$]+)\$([^\$]|$)')

RE_CODE_BLOCK = re.compile(r'^```.*$')
RE_MATH_BLOCK = re.compile(r'^(.*)(\$\$)\s*$')
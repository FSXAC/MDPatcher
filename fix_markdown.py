# This program should format markdown files

import argparse
import re
import os

import datetime

from expressions import *

# Arg parser stuff
parser = argparse.ArgumentParser(description='Fixes markdown files')
parser.add_argument('input_file', help='Input file path')
parser.add_argument('-o', '--output_file', nargs=1, help='Output file path')
args = parser.parse_args()

# Extract all the lines
lines = list()
with open(args.input_file, 'r', encoding='utf-8') as md_file:
	lines = md_file.readlines()

# Get front matter data
state = 'nothing'
front_matters = []
front_matter_end_index = 0
for line in lines:
	line = line.rstrip()

	if state == 'nothing':
		if not line:
			pass
		elif RE_TRIPLE_DASH.match(line):
			state = 'inside'
		else:
			break
	elif state == 'inside':
		if not line:
			pass
		if RE_TRIPLE_DASH.match(line):
			break
		else:
			front_matters.append(line)

	front_matter_end_index += 1

# Add the essential things to front matter
# Title
for fm in front_matters:
	if fm.lower().startswith('title:'):
		break
else:
	# Use the first header
	for line in lines:
		heading = RE_ALL_HEADERS.match(line)
		if heading:
			front_matters.append('title: {}'.format(str(heading.group(2))))
			break

# Date
new_date = 'date: {}'.format(datetime.date.today().strftime('%Y-%m-%d'))
for index, fm in enumerate(front_matters):
	if fm.startswith('date:'):
		front_matters[index] = new_date
		break
else:
	front_matters.append(new_date)

print(front_matters)
lines = lines[front_matter_end_index:]

# Reading the content
for line_num, line in enumerate(lines):
	line = line.rstrip()

	if RE_TOC.match(line):
		lines[line_num] = '- toc\n{:toc}\n'

# OUTPUT
if args.output_file:
	with open(args.output_file[0], 'w', encoding='utf-8') as md_file:
		md_file.write('---\n')
		md_file.write('\n'.join(front_matters))
		md_file.write('\n---\n\n')
		md_file.writelines(lines)
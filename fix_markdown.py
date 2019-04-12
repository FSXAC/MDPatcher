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

# Stats TODO: use a counter
stats = {
	'fm': 0,
	'toc': 0,
	'heading': 0,
	'latex_tag': 0
}

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
			front_matter_end_index += 1
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
		heading = RE_ALL_HEADINGS.match(line)
		if heading:
			front_matters.append('title: {}'.format(str(heading.group(1))))
			break

# Date
new_date = 'date: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d $H:$m:$s'))
for index, fm in enumerate(front_matters):
	if fm.startswith('date:'):
		front_matters[index] = new_date
		break
else:
	front_matters.append(new_date)

lines = lines[front_matter_end_index:]

# Reading the content
state = 'normal'
for line_num, line in enumerate(lines):
	line = line.rstrip()

	if state == 'in_math_block':
		# Switch states
		math_block = RE_MATH_BLOCK.match(line)
		if math_block:
			state = 'normal'

			# check if there's a line below
			beginning = math_block.group(1).rstrip()
			if lines[line_num + 1].rstrip() != beginning:
				line = '{}{}\n{}'.format(math_block.group(1), math_block.group(2), beginning)
	
	elif state == 'in_code_block':
		# Switch states
		if RE_CODE_BLOCK.match(line):
			state = 'normal'
			continue

		if RE_MATH_BLOCK.match(line):
			# TODO: fix math block spacing
			continue

	elif state == 'normal':
		# Switch states
		if RE_CODE_BLOCK.match(line):
			state = 'in_code_block'
			continue
		
		math_block = RE_MATH_BLOCK.match(line)
		if math_block:
			state = 'in_math_block'

			# Check if there's a line above
			beginning = math_block.group(1).rstrip()
			if lines[line_num - 1].rstrip() != beginning:
				line = '{}\n{}{}'.format(beginning, math_block.group(1), math_block.group(2))

		# Fix TOC
		line = re.sub(RE_TOC.pattern, '- toc\n{:toc}', line)

		# Fix non standard heading
		line = re.sub(RE_ALL_BAD_HEADINGS.pattern, r'\1 \2', line)
		
		# Fix single $ latex tags
		line = re.sub(RE_SINGLE_LATEX.pattern, r'\1$$\2$$\3', line)

	# Put it together
	lines[line_num] = '{}\n'.format(line)


# Combined regex fixing
# TODO: Fix vertical | in math

combined_lines = ''.join(lines)

# OUTPUT
if args.output_file:
	with open(args.output_file[0], 'w', encoding='utf-8') as md_file:
		md_file.write('---\n')
		md_file.write('\n'.join(front_matters))
		md_file.write('\n---\n\n')
		md_file.write(combined_lines)
		# md_file.writelines(lines)

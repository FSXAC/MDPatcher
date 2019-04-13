# This program should format markdown files

import argparse
import re
import os

import datetime

from expressions import *

# Arg parser stuff
parser = argparse.ArgumentParser(description='Fixes markdown files')
parser.add_argument('input', help='Input file/folder path')
parser.add_argument('-o', '--output_file', nargs=1, help='Output file path')
parser.add_argument('--update-date', action='store_true', help='Update the date of the file to now')
args = parser.parse_args()

# Stats TODO: use a counter
stats = {
	'fm': 0,
	'toc': 0,
	'heading': 0,
	'latex_tag': 0
}

line_ending = '\n'

def main(filepath):

	# Extract all the lines
	lines = list()
	with open(filepath, 'r', encoding='utf-8') as md_file:
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
	if args.update_date:
		new_date = 'date: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
				if line_num + 1 < len(lines):
					if lines[line_num + 1].rstrip() != beginning:
						line = '{}{}{}{}'.format(math_block.group(1), math_block.group(2), line_ending, beginning)

			line = line.replace('|', r'\vert ')
		
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
				if line_num - 1 >= 0:
					if lines[line_num - 1].rstrip() != beginning:
						line = '{}{}{}{}'.format(beginning, line_ending, math_block.group(1), math_block.group(2))

			# Fix TOC
			line = re.sub(RE_TOC.pattern, '- toc\n{:toc}', line)

			# Fix non standard heading
			line = re.sub(RE_ALL_BAD_HEADINGS.pattern, r'\1 \2', line)
			
			# Fix single $ latex tags
			line = re.sub(RE_SINGLE_LATEX.pattern, r'\1$$\2$$\3', line)

			# Replace improper symbols in inline math blocks
			inline_math_iter = RE_INLINE_MATH.finditer(line)
			new_line = ''
			prev_end = 0
			while True:
				try:
					# print(next(inline_math_iter).group(1))
					match = next(inline_math_iter)

					new_line += line[prev_end:match.start()]
					new_line += '{}$${}$${}'.format(
						match.group(1),
						match.group(2)
							.replace('|', r'\vert '),
					match.group(3))
					prev_end = match.end()

				except StopIteration:
					break
			new_line += line[prev_end:]
			line = new_line

		# Put it together
		lines[line_num] = '{}{}'.format(line, line_ending)

	# Combined regex fixing
	# TODO: Fix vertical | in math

	combined_lines = '---\n{}\n---\n{}'.format('\n'.join(front_matters), ''.join(lines))
	combined_lines = line_ending.join([
		'---',
		line_ending.join(front_matters),
		'---',
		''.join(lines)
	])
	return combined_lines

if __name__ == '__main__':
	if os.path.isdir(args.input):
		for file in os.listdir(args.input):
			if not file.endswith('.md'):
				continue

			print('Processing {} ...'.format(file))

			file = os.path.join(args.input, file)
			output = main(file)

			with open(file, 'w', encoding='utf-8') as md_file:
				md_file.write(output)
	else:
		output = main(args.input)
		
		if args.output_file:
			out_file = args.output_file[0]
		else:
			out_file = args.input

		with open(out_file, 'w', encoding='utf-8') as md_file:
				md_file.write(output)

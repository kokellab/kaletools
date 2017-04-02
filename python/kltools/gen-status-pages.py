#!/usr/bin/env python
# coding=utf-8

import os
import json
import argparse
from typing import List, Set, Iterator

_current_dir = os.path.dirname(os.path.realpath(__file__))
_resources_dir = os.path.join(_current_dir, 'resources')

def _make_dirs(output_dir: str):
	"""Makes a directory if it doesn't exist."""
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	elif not os.path.isdir(output_dir):
		raise ValueError("{} already exists and is not a directory".format(output_dir))

def generate(statuses_file: str, template_file: str, output_dir: str):
	_make_dirs(output_dir)
	with open(statuses_file, 'r') as f: statuses = json.load(f)
	with open(template_file, 'r') as f: template = f.read()
	for entry in statuses:
		replaced = template
		for key, value in entry.items(): replaced = replaced.replace('$' + key, value)
		with open(os.path.join(output_dir, entry['code'] + '.html'), 'w') as f: f.write(replaced)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generates a peewee model and fixes the connection info and binary/blob columns.')
	parser.add_argument('--statuses', default=None, type=str, help='JSON file of status codes')
	parser.add_argument('--template', default=None, type=str, help='Status page template')
	parser.add_argument('--output', required=True, type=str, help='Directory for output')
	opts = parser.parse_args()
	statuses = opts.statuses
	statuses = os.path.join(_resources_dir, 'status-codes.json') if opts.statuses is None else opts.statuses
	template = os.path.join(_resources_dir, 'template.html') if opts.statuses is None else opts.template
	generate(statuses, template, opts.output)

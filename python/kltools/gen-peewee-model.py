#!/usr/bin/env python
# coding=utf-8

import re
import os
import sys
import argparse
import subprocess
import fileinput
import peewee
import logging
from typing import List, Set, Iterator

_comment = '  # auto-corrected to BlobField'
_blob_regex = re.compile("^ *\`([^ ]+)\` (?:(?:binary)|(?:[[a-zA-Z]*blob)).*$")
_peewee_field_regex = re.compile('^ *([a-z][a-z0-9_]*) = ([A-Z][A-Za-z]*Field)\(.*\)$')
_type_regex = re.compile('[A-Z][A-Za-z]*Field')

def _lines(filename: str) -> Iterator[str]:
	with open(filename, 'r') as f:
		for line in f: yield line.rstrip('\n\r')

def gen_model(host: str, username: str, db: str, port: int, output: str) -> None:
	with open(output, 'w') as f:
		subprocess.call([sys.executable, '-m', 'pwiz', '-e', 'mysql', '-H', host, '-u', username, '-p', port, '-P', db], stdout=f)

def fix_connection(output: str, header_file: str) -> None:

	header_lines = ''
	if header_file is not None:
		with open(header_file, 'r') as f:
			header_lines = f.read()

	for line in fileinput.input(output, inplace=True):
		if fileinput.filelineno() == 1:
			print(header_lines)
		elif fileinput.filelineno() > 3:
			print(line.rstrip())

def find_blob_columns(schema: str) -> Set[str]:
	"""Returns the names of columns that have binary or *blob types."""
	return {m.group(1) for m in [_blob_regex.match(line) for line in _lines(schema)] if m is not None}

def fix_blobs(columns: Set[str], output: str):
	for line in fileinput.input(output, inplace=True):
		m = _peewee_field_regex.match(line)
		if m is not None and m.group(1) in columns:
			print(_type_regex.sub('BlobField', line.rstrip()) + _comment)
		else:
			print(line.rstrip())

def run(host: str, username: str, db: str, port: int, header_file: str, schema: str, output: str) -> None:
	gen_model(host, username, db, port, output)
	fix_connection(output, header_file)
	blob_columns = find_blob_columns(schema)
	logging.info("Fixing columns {}".format(blob_columns))
	fix_blobs(blob_columns, output)

def main(opts: List[str]) -> None:
	run(opts.host, opts.username, opts.db, opts.port, opts.header_file, opts.schema, opts.output)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generates a peewee model and fixes the connection info and binary/blob columns.')
	parser.add_argument('--output', required=True, type=str, help='Output model.py file')
	parser.add_argument('--host', default='localhost', type=str, help='The database connection server')
	parser.add_argument('--username', required=True, type=str, help='The database username')
	parser.add_argument('--db', required=True, type=str, help='The name of the database')
	parser.add_argument('--port', default=3306, type=str, help='The port number')
	parser.add_argument('--schema', required=True, type=str, help='The path to the schema .sql file; must be for this database ONLY')
	parser.add_argument('--header-file', required=False, type=str, help='File containing header lines to replace the first 3 lines of the model file with')
	opts = parser.parse_args()
	main(opts)


#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# print help to stdout if requested
if (( $# == 1 )) && [[ "${1}" == "--help" ]]; then
	echo "Usage: ${0} [-h/--help] [-f filename-extension = '.csv.'] [-j n-cores = 1] <search-path>" 
	echo "Recursively searches for files under <search-path> in parallel using <j> cores, gzipping each file whose name ends with <f>.
	Does not fail due to too many arguments.
	Arguments:
		-f filename-extension; default '*.csv'
			A unix glob pattern for find
		-j n-cores; default 1
			The number of cores to use
		<search-path>
			The path to search under recursively
"
	exit 0
fi

# okay, these checks got a little ridiculous
# we want to make sure the positional argument comes last

usage() {
	(>&2 echo "Usage: ${0} [-h/--help] [-f filename-extension = '.csv.'] [-j n-cores = 1] <search-path>" )
	exit 1
}

last_arg="${@: -1}"
second_to_last=$(( $#-1 ))
second_to_last_arg=""
if (( $# > 2 )); then
	second_to_last_arg="${!second_to_last}"
fi
if (( $# < 1 )) || (( $# > 5 )) || ( (( $# == 2)) && [[ "${1:0:1}" == '-' ]] ) || [[ "${last_arg:0:1}" == '-' ]] || [[ "${second_to_last_arg:0:1}" == '-' ]] ; then
	usage
fi

filename_glob="*.csv"
n_cores=1
while getopts ":f:j:" flag "${@}"; do
	case "${flag}" in
		f) filename_glob="${OPTARG}";;
		j) n_cores="${OPTARG}";;
		*) usage;;
	esac
done

search_path="${@:$OPTIND:1}"

find "${search_path}" -type f -name "${filename_glob}" -print0 | xargs -0 -P "${n_cores}" gzip


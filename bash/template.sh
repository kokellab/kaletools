#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
# Author: author

# print help to stdout if requested
usage_str = "Usage: ${0} [--some-flag] [--some-optional-arg value] <arg1> <arg2> [optional-arg]"
if (( $# == 1 )) && [[ "${1}" == "--help" ]]; then
	echo "${usage_str}"
	echo "A description of what this does"
	exit 0
fi

# validate the arguments; this example requires between 2 and 6 arguments
if (( $# < 2 )) || (( $# > 6 )); then
	(>&2 echo "${usage_str}")
	exit 1
fi

# set arguments
abc = "${1}"
xyz = "${2}"
# ...

function main {

}

main "${abc}" "${xyz}" 


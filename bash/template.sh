#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# print help to stdout if requested
if (( $# == 1 )) && [[ "${1}" == "--help" ]]; then
	echo "Usage: ${0} [--some-flag] [--some-optional-arg value] <arg1> <arg2> [optional-arg]"
	echo "A description of what this does"
	return 0
fi

# validate the arguments; this example requires between 2 and 6 arguments
if (( $# < 2 )) || (( $# > 6 )); then
	(>&2 	echo "Usage: ${0} [--some-flag] [--some-optional-arg value] <arg1> <arg2> [optional-arg]")
	return 1
fi

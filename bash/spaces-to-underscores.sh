#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

if (( $# == 1 )) && [[ "${1}" == "--help" ]]; then
	echo "Usage: ${0} [-h/--help] <path>"
	echo "Replaces the spaces with underscores in every filename in <path> or its subdirectories (recursively)"
	exit 0
fi

if (( $# != 1 )); then
	(>&2 echo "Usage: [-h/--help] ${0} <path>")
	exit 1
fi

find "${1}" -depth -name '* *' \
| while IFS= read -r f ; do mv -i "$f" "$(dirname "$f")/$(basename "$f"|tr ' ' _)" ; done


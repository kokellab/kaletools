#!/usr/bin/env zsh
set -euo pipefail
IFS=$'\n\t'
# Author: Douglas

usage_str = "Usage: ${0} <webhook_url> <channel> <message>"
if (( $# == 1 )) && [[ "$1" = "--help" ]]; then
	echo "Sends a message on Slack"
	echo "${usage_str}"
	exit 0
fi


if (( $# != 3 )); then
	(>&2 echo "${usage_str}")
	exit 1
fi
webhook_url=$1
channel=$2
text=$3

# TODO isn't this impossible anyway?
if [[ "${text}" == "" ]]; then
	echo "No text specified"
	exit 1
fi

escaped=$(echo $text | sed 's/"/\"/g' | sed "s/'/\'/g" )

json="{\"channel\": \"$channel\", \"attachments\":[{\"text\": \"$escaped\"}]}"

curl -s -d "payload=$json" "$webhook_url"


# Author: Douglas
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

if (( $# != 3 )); then
	(>&2 echo "Usage: ${0} <webhook_url> <channel> <message>")
	exit 1
fi
webhook_url=$1
channel=$2
text=$3

if [[ $text == "" ]]; then
        echo "No text specified"
        exit 1
fi

escaped=$(echo $text | sed 's/"/\"/g' | sed "s/'/\'/g" )

json="{\"link_names\":1,\"channel\": \"$channel\", \"attachments\":[{\"text\": \"$escaped\"}]}"

curl -s -d "payload=$json" "$webhook_url"


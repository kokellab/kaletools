# Author: Douglas
# Usage: <identity-sh-file> <message>
# the identity-sh-file must have the lines:
# export username=...
# export channel=...
# export webhook_url=...
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

if (( $# != 2 )); then
	(>&2 echo "Usage: ${0} <identity-sh-file> <message>")
	exit 1
fi
echo "$1"

source "$1"
text=$2

if [[ $text == "" ]]; then
        echo "No text specified"
        exit 1
fi

escaped=$(echo $text | sed 's/"/\"/g' | sed "s/'/\'/g" )

json="{\"channel\": \"$channel\", \"username\":\"$username\", \"attachments\":[{\"color\":\"danger\" , \"text\": \"$escaped\"}]}"

curl -s -d "payload=$json" "$webhook_url"


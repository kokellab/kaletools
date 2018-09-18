#!/usr/bin/env zsh
set -euo pipefail
IFS=$'\n\t'
# Author: Douglas

usage_str = "Usage: $0 <certificate-file>"
if (( $# == 1 )) && [[ "$1" = "--help" ]]; then
	echo "Adds a certificate to the system keychain"
	echo "Adds it as a trusted root and with 'basic' and 'ssl'"
	echo "Mac OS only"
	echo "${usage_str}"
	exit 0
fi

if (( $# != 1 )); then
	(>&2 echo "${usage_str}")
	exit 1
fi


# ssl, smime, codeSign, IPSec, iChat, basic, swUpdate, pkgSign, pkinitClient, pkinitServer, timestamping, eap
echo "Importing ${1}"
security add-trusted-cert -d -r trustAsRoot -p ssl -p basic -k /Library/Keychains/System.keychain "${1}"
echo "Added ${1} to keychain"


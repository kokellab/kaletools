#!/usr/bin/env bash

date_time=$(date '+%Y-%m-%d')
bup_path=/Volumes/Drobo5D2_Valinor_backup
log_path=/Users/davekokel/valinor-backup-logs/${date_time}.log
echo "Backing up to ${bup_path}"
echo "Logging to ${log_path}"
display_host="Gondor"

bup () {
	echo "Copying $1 to $bup_path/$2"
	rsync --update --recursive --times --no-links --progress --log-file=$log_path valinor:$1 $bup_path/$2
	echo "==========FINISHED COPYING ${1} at $(date '+%Y-%m-%d')==========" >> $log_path
	$HOME/bin/slack.sh "${slack_url}" "notifications" "${display_host} backed up ${1} from Valinor"
}

bup /alpha/backups ""
bup /alpha/plates ""
bup /alpha/legacy ""
bup /alpha/orphaned ""
bup /alpha/logs/submissions "logs/"

echo "==========COMPLETED BACKUP at $(date '+%Y-%m-%d')==========" >> $log_path
$HOME/bin/valinor-to-slack "${display_host} completed series of Valinor backups"

gzip ${log_path}


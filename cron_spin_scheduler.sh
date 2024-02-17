#!/bin/sh

SCHEDULE=$CRON_SCHEDULE
COMMAND="/usr/local/bin/python /app/spin.py >> /var/log/cron.log 2>&1"
(crontab -l 2>/dev/null; echo "$SCHEDULE" "$COMMAND") | crontab


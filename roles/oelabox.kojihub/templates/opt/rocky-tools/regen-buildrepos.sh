#!/bin/bash
# adapted from centos
logfile=/var/tmp/koji-regen-repo.log
for buildroot in $(koji list-tags \*-build); do
  koji regen-repo --nowait $buildroot >> $logfile 2>&1
done

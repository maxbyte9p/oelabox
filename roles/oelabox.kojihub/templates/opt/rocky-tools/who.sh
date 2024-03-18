#!/bin/bash
# adapted from centos tools
for i in `koji list-tags $1*candidate`; do
  USERS="$USERS `koji list-tagged --quiet $i  | rev | cut -d " " -f 1 | rev | uniq | tr '\n' ' '`"
  TMP=`echo ${i} | cut -d "-" -f 1`
  SIG=${TMP%?}
done

echo $1:`echo $USERS|tr " " "\n"|sort|uniq|tr "\n" " "`

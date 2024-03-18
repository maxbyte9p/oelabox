#!/bin/bash
for i in `koji list-tags \*-build`; do
  koji regen-repo --nowait $i;
done

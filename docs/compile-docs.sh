#!/bin/bash

compile() {
  pandoc -s $1 -o ${2}/$(basename ${1%.*}).html --toc --metadata title="$(basename ${1%.*})"
}

[ ! -d /tmp/oeladoc ] && mkdir -pv /tmp/oeladoc/topics

compile README.md /tmp/oeladoc
for i in $(ls -1 topics/*); do echo "Compiling: $i"; compile $i /tmp/oeladoc/topics; done

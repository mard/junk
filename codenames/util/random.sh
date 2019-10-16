#!/usr/bin/env sh
BASEDIR=$(dirname "$0")
for i in $(seq 1 $1)
do
    shuf -n 1 $BASEDIR/../static/adjectives-verbs.txt | tr -d '\r\n' | awk '{printf $1" "}' && \
    shuf -n 1 $BASEDIR/../static/nouns.txt;
done
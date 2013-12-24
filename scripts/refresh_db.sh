#!/bin/sh
SCRIPTS_ROOT=`dirname $0`
ROOT=`dirname $SCRIPTS_ROOT`
cat $ROOT/sql/drop_schema.sql | psql prod
cat $ROOT/sql/schema.sql | psql prod
$ROOT/wordgen/data-importer.py --verified < wordgen/worddata/wiki_words.json

#!/bin/sh
# Fabrique deploy/ (ce qu'on téléverse dans michelgallone.ch/) à partir de site/ et server/.
set -e
cd "$(dirname "$0")"
rm -rf deploy && mkdir deploy
# rsync pour laisser de côté les .DS_Store du Mac
rsync -a --exclude '.DS_Store' site/ deploy/
rsync -a --exclude '.DS_Store' server/ deploy/
echo "deploy/ prêt :"; (cd deploy && find . -type f | sort)

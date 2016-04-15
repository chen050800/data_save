#!/bin/bash

# Quick Package Updater

# John Dong (Fixed by Vinx)


#Licensed under the GPL.

DISTS="radar"

SECTIONS="main"
BINARY_ARCH="binary-i386"

for a in $DISTS; do

for b in $SECTIONS; do

for c in $BINARY_ARCH; do

if [ ! -d dists/$a/$b/$c ]; then
mkdir -p dists/$a/$b/$c
fi

if [ -d dists/$a/$b/$c ]; then
echo "Updating dists/$a/$b/$c/Packages"
dpkg-scanpackages -m pool /dev/null | gzip -9 > dists/$a/$b/$c/Packages.gz
fi
done
done

done

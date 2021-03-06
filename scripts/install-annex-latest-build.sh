#!/bin/bash
set +evx
CD=~/.cache/curl-downloads
FN=git-annex-standalone-amd64.tar.gz
URL=https://downloads.kitenet.net/git-annex/linux/current/$FN

TARGET=~/.local/git-annex

mkdir -p $CD

if  ! [ -f $CD/$FN ]
then
	curl -o $CD/$FN.tmp -C - $URL
	mv $CD/$FN.tmp $CD/$FN
fi

if [ -e $TARGET ]
then
	rm -rf $TARGET
fi

mkdir -p $TARGET
tar --directory=$TARGET --strip-components=1 -x -f $CD/$FN

mkdir -p ~/.local/bin
ln -sf $TARGET/git-annex  ~/.local/bin/git-annex

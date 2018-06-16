#!/bin/bash
set +ev
CD=~/.cache/curl-downloads
FN=borg-linux64
URL=https://github.com/borgbackup/borg/releases/download/1.1.6/$FN
TARGET=~/.local/bin/borg


mkdir -p $CD

if  ! [ -f $CD/$FN ]
then
	curl -L -o $CD/$FN.tmp -C - $URL
	mv $CD/$FN.tmp $CD/$FN
fi

if [ -e $TARGET ]
then
	rm -rf $TARGET
fi

mkdir -p ~/.local/bin
cp $CD/$FN $TARGET
chmod +x $TARGET

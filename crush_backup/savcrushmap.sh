#!/bin/sh
#eric.mourgaya@gmail.com
# Licence MIT
# this script is ruling the  apache Licence.
# keep the last seven backup
#crontab
#0 7 * * * $0 
# be careful we need  a serveur with  ceph.conf and key to do this

crushbinfile="crusmap"
SUFFIX=`date +'%d%m%Y'`
BASEDIR=/opt/crushmap_sink

mkdir -pv $BASEDIR/bin
mkdir -pv $BASEDIR/txt

# extract the current crushmap

ceph osd getcrushmap -o $BASEDIR/bin/$crushbinfile.bin.SUFFIX
crushtool -d $BASEDIR/bin/$crushbinfile.SUFIX -o $BASEDIR/bin/$crushbinfile.txt

find $BASEDIR -type f -ctime +7 -name $crushbinfile* -exec rm {} \;

 


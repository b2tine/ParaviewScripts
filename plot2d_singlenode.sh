#!/bin/bash

#Example usage:

#makegif_singlenode.sh datatype
#datatype is: 3d-intfc 3d-curves etc.

function create_movie_index()
{
    filename=$1
    dname="movie_index"
    if [ ! -d "$dname" ]; then
        mkdir $dname
    fi

    i=0
    echo "...creating movie index for $filename"
    for tsdir in vtk.ts*; do
        i=`expr $i + 1`
        ln -P ${tsdir}/${filename}.vtk ./${dname}/${filename}-${i}.vtk
    done
}



CWD=`pwd`

export DATATYPE=$1

create_movie_index 2d-intfc
create_movie_index $DATATYPE

#The i is generated from the create_movie_index function 
export NUMFRAMES=$i
export MOVIEDIR="$CWD/movie_index"

JPGDIR="$CWD/JPGs"
mkdir -p $JPGDIR
export JPGDIR

echo " ...saving animation"

pvbatch --force-offscreen-rendering /home/brandon/ParaviewScripts/pv_single_reader.py
#pvbatch --force-offscreen-rendering ./pv_single_reader.py

MP4NAME="${CWD}/${DATATYPE}.mp4"

echo "  ...creating $MP4NAME"

ffmpeg -i $JPGDIR/${DATATYPE}%04d.jpg -c:v libx264 $MP4NAME

echo "   ...done"


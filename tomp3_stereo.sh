#!/bin/bash
hi_res_path=$1
lo_res_path=$2
ext=$3

cd $1
for i in ls *.$ext
do
  f=${i/$ext/mp3}
  ffmpeg -i "$i" -write_id3v1 1 -id3v2_version 3 -dither_method modified_e_weighted -out_sample_rate 48k -b:a 320k "$lo_res_path/$f"
done

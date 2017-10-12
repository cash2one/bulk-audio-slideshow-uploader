#!/bin/bash

# This script takes a folder full of images and saves new, resized images that have been 
# either pillarboxed or letterboxed.

#----------------------------------------------------------------
# SETTINGS
image_dir="initial_sample_data/set1/images"
n_files=5                                         # Can this be detected automatically?
files=`ls ${image_dir}/*.jpg | head -${n_files}`  # Broaden to include more than jpg?
x=1280											  # New image width
y=720 											  # New image height

#----------------------------------------------------------------

vf_params="scale=${x}:${y}:force_original_aspect_ratio=decrease,\
pad=${x}:${y}:(ow-iw)/2:(oh-ih)/2"

i=0                                               # Can we prepend 0s?

for f in ${files}; do
  ffmpeg -nostats -loglevel error -i $f -vf $vf_params ${image_dir}/${i}.PNG
  i=$((i+1))
done
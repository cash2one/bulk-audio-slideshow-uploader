#!/bin/bash -

#
# melt -verbose \
#-profile atsc_720p_25 \
#000.png out=50 \
#001.png out=75 -mix 25 -mixer luma \
#002.png out=75 -mix 25 -mixer luma \
#003.png out=75 -mix 25 -mixer luma \
#004.png out=75 -mix 25 -mixer luma \
# -consumer avformat:output.mp4 vcodec=libx264 an=1

#----------------------------------------------------------------
# SETTINGS
input_dir="initial_sample_data/set1/images"  # Replace this by a path to your folder /path/to/your/folder
files=`ls ${input_dir}/*.PNG`    # Change the file type to the correct type of your images
# n_files=`ls ${input_dir}/*.PNG -1 | wc -l`                        # Replace this by a number of images
output_file="video.mp4"           # Name of output video
crossfade=0.9                     # Crossfade duration between two images
#----------------------------------------------------------------

# Making an ffmpeg script...
input="melt -verbose -profile atsc_720p_25"

i=0

for f in ${files}; do
  if [ "${i}" -eq "0" ]
  then
    input+="${f} out=50 "
  else
    input+="${f} out=75 -mix 25 -mixer luma "
  fi
  i=$((i+1))
done

input+="-consumer avformat:output.mp4 vcodec=libx264 an=1"

script="${input}"

echo ${script}

# Run it
eval "${script}"
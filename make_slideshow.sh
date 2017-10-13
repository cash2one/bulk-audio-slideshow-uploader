#!/bin/bash -

#----------------------------------------------------------------
# Example of script generated:

# melt -profile atsc_720p_25 \
# initial_sample_data/set1/images/000.PNG out=50 \
# initial_sample_data/set1/images/001.PNG out=75 -mix 25 -mixer luma \
# initial_sample_data/set1/images/002.PNG out=75 -mix 25 -mixer luma \
# initial_sample_data/set1/images/003.PNG out=75 -mix 25 -mixer luma \
# initial_sample_data/set1/images/004.PNG out=75 -mix 25 -mixer luma \
# -consumer avformat:initial_sample_data/set1/images/output.mp4 vcodec=libx264 an=1

#----------------------------------------------------------------
# Settings

input_dir="initial_sample_data/set1/images"
files=`ls ${input_dir}/*.PNG`    # Change the file type to the correct type of your images
mp3_path="initial_sample_data/set1/BB_B-2200-A_BVE82642-1.mp3"
fade_frames=25
output_path="initial_sample_data/set1/slideshow_video_only.mp4"

#----------------------------------------------------------------
# 

n_files=`ls -1 ${input_dir}/*.PNG | wc -l` 
song_length=`afinfo ${mp3_path} | awk '/estimated duration/ { print$3}'`
rounded_song_length=`printf "%.0f\n" ${song_length}`
fpi_0=$((${rounded_song_length} * 25 / ${n_files} + 1))
fpi_1=$((${fpi_0} + ${fade_frames}))

#----------------------------------------------------------------
# Generate script

input="melt -silent -profile atsc_720p_25 "

i=0

for f in ${files}; do
  if [ "${i}" -eq "0" ]
  then
    input+="${f} out=${fpi_0} "
  else
    input+="${f} out=${fpi_1} -mix ${fade_frames} -mixer luma "
  fi
  i=$((i+1))
done

input+="-consumer avformat:${output_path} vcodec=libx264 an=1"

#----------------------------------------------------------------
# Run script

eval "${input}"
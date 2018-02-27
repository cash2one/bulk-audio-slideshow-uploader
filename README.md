## Overview

This project enables the creation and uploading of automatically generated videos from a large collection of rare recordings that are out of copyright. Each item in the collection contains audio, images, and text metadata. If you'd like to try this yourself and adapt this to a different set of videos, you'll need to install [https://www.mltframework.org/](melt), [https://www.ffmpeg.org/](ffmpeg), and [https://github.com/tokland/youtube-upload](youtube-upload). You'll also need to assemble your data in the same format as frontera/guide.csv and adapt the code accordingly. 

### Sub-tasks:

1) (done) Batch convert a set of images to be equal size and letterboxed to YT proportions (done with shell script and ffmpeg)
2) (done) Create a video from a set of images and an mp3 (done with shell script and melt/ffmpeg)
3) (done) Batch create videos
4) (done) Upload video in a scalable way, with metadata
5) (done) Batch-upload a set of created videos, or batch-create/upload a set of videos

### To do

- Write a script to upload videos according to a scheduler, so it's possible to upload 50 or 100 per day.

_________________________________________
 
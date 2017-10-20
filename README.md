## Overview

This project enables the creation and uploading of automatically generated videos from a large collection of rare recordings that are out of copyright. Each item in the collection contains audio, images, and text metadata. 

### Sub-tasks:

1) (done) Batch convert a set of images to be equal size and letterboxed to YT proportions (done with shell script and ffmpeg)
2) (done) Create a video from a set of images and an mp3 (done with shell script and melt/ffmpeg)
3) Batch create videos
4) Upload video in a scalable way, with metadata (done with someone's youtube-uploader Python script)
5) Batch-upload a set of created videos, or batch-create/upload a set of videos

### To do

- Create a shell script that will make and upload a batch of videos within a specified range within the test_environment folder, containing 4 videos.

### Other ideas:

- Possible user interface: Make/upload videos given indices in the master spreadsheet
- Will batch-deletion of videos be necessary?

_________________________________________
 
import sys
import csv
import os.path
import re
from math import ceil
import subprocess


GUIDE_PATH = 'frontera/guide_20180222.csv'


def get_slideshow_creation_command(output_path, image_paths, duration, transition_frames=25):
    """
    Given an output path, a path to the main (first) image, a list of other images, and a duration in seconds,
    returns a melt command that can be executed to create a slideshow.
    The optional transition frames parameter determines how quickly the crossfade occurs.
    If other_image_paths is equal to [], the slideshow will be one single image
    """
    arhoolie_credits_duration = 10.0
    command = 'melt -silent -profile atsc_720p_25 '
    command += image_paths[0] + ' '

    if len(image_paths) == 1:
        main_image_duration_param = ceil(duration * 25.0)
    else:
        main_image_duration_param = ceil((duration - arhoolie_credits_duration) * 25.0 / (len(image_paths) - 1))
        other_image_duration_param = main_image_duration_param + transition_frames
        credits_duration_param = ceil(arhoolie_credits_duration * 25) + transition_frames

    command += 'out={} '.format(main_image_duration_param)

    if len(image_paths) > 1:
        for image_path in image_paths[1:-1]:
            command += image_path + ' out={} -mix 25 -mixer luma '.format(other_image_duration_param)
        command += image_paths[-1] + ' out={} -mix 25 -mixer luma '.format(credits_duration_param)

    command += '-consumer avformat:{} vcodec=libx264 an=1'.format(output_path)

    return command


def get_video_audio_joining_command(audio_path, video_path, output_path):
    """
    Given an audio path, a video path, and an output path, returns an ffmpeg command that
    can be used to join the audio and video into a single combined video with audio.
    """
    return 'ffmpeg -nostats -loglevel error -i {} -i {} -codec copy -shortest {}'.format(
           video_path, audio_path, output_path)


def get_video_upload_command(title, description, file_path, thumbnail_path=None):
    tags = 'Mexico, Arhoolie'
    if thumbnail_path is None:
        return 'youtube-upload --title="{}" --description="{}" --tags="{}" {}'.format(
               title, description, tags, file_path)
    else:
        return 'youtube-upload --title="{}" --description="{}" --tags="{}" --thumbnail="{}" {}'.format(
               title, description, tags, thumbnail_path, file_path)



def resize_images(image_path_list, x=1280, y=720):

    resized_image_paths = []

    for i, image_path in enumerate(image_path_list):
        dir_path = os.path.dirname(image_path)
        output_file = '{0:03d}'.format(i) + '.PNG'
        output_path = os.path.join(dir_path, output_file)
        resized_image_paths.append(output_path)
        if os.path.isfile(output_path):
            continue

        vf_params = '"scale={0}:{1}:force_original_aspect_ratio=decrease,pad={0}:{1}:(ow-iw)/2:(oh-ih)/2"'.format(x, y)
        resize_command = 'ffmpeg -nostats -loglevel error -i {} -vf {} {}'.format(
                         image_path, vf_params, output_path)
        p = subprocess.Popen(resize_command, shell=True, executable='/bin/sh', stdout=subprocess.PIPE)
        p.wait()
        # print(p.returncode)

    return resized_image_paths


def make_video_from_image_and_mp3_paths(image_paths, audio_path, overwrite=False):
    """
    Given a list of image paths and an audio path (all in mac format), crops/letterboxes the images (if not
    already done), and creates a slideshow in the same folder as the mp3 (if it doesn't already exist).
    Last image will be the Arhoolie credit image, and if there are no other images, this will be the only image.
    """
    arhoolie_path = 'batch_test_environment/frontera/arhoolie_credit_screen_small.PNG'
    audio_suffix = '.mp3'

    # Prepare various file paths
    audio_directory, audio_filename = os.path.split(audio_path)
    slideshow_no_audio_filename = audio_filename.replace(audio_suffix, '_slideshow_no_audio.mp4')
    slideshow_no_audio_path = os.path.join(audio_directory, slideshow_no_audio_filename)
    slideshow_w_audio_filename = audio_filename.replace(audio_suffix, '_slideshow_w_audio.mp4')
    slideshow_w_audio_path = os.path.join(audio_directory, slideshow_w_audio_filename)
    resized_image_paths_w_credits = resize_images(image_paths) + [arhoolie_path]

    # Get audio length
    audio_length_cmd = "ffprobe -loglevel quiet -show_entries format=duration -i " + audio_path
    p = subprocess.Popen(audio_length_cmd, shell=True, executable='/bin/sh', stdout=subprocess.PIPE)
    p.wait()
    duration_str = p.stdout.read().split()[1].decode('ascii')
    audio_duration = float(duration_str.split('=')[1])

    # Get no-audio slideshow command
    slideshow_cmd = get_slideshow_creation_command(slideshow_no_audio_path, resized_image_paths_w_credits,
                                                   duration=audio_duration)

    # Create no-audio slideshow if necessary
    if overwrite and os.path.isfile(slideshow_no_audio_path):
        os.remove(slideshow_no_audio_path)

    if not os.path.isfile(slideshow_no_audio_path):
        p = subprocess.Popen(slideshow_cmd, shell=True, executable='/bin/sh', stdout=subprocess.PIPE)
        p.wait()
    else:
        print("Skipped creation of no-audio slideshow; file already exists. (Set overwrite parameter to true to overwrite.)")

    # Get audio slideshow command
    slideshow_audio_join_cmd = get_video_audio_joining_command(audio_path, slideshow_no_audio_path,
                                                               slideshow_w_audio_path)

    # Create no-audio slideshow if necessary
    if overwrite and os.path.isfile(slideshow_w_audio_path):
        os.remove(slideshow_w_audio_path)

    if not os.path.isfile(slideshow_w_audio_path):
        p = subprocess.Popen(slideshow_audio_join_cmd, shell=True, executable='/bin/sh', stdout=subprocess.PIPE)
        p.wait()
    else:
        print("Skipped creation of audio slideshow; file already exists. (Set overwrite parameter to true to overwrite.)")

    return slideshow_w_audio_path


def verify_spreadsheet_files():
    error_log = []
    with open(GUIDE_PATH) as f:
        file_reader = list(csv.reader(f))
        for i, row in enumerate(file_reader[1:]):
            row_number = i + 2
            row_errors = []

            for field, content in zip(('title', 'description', 'tags', 'record_number'),
                                      (row[0], row[1], row[8], row[9])):
                if not content.strip():
                    row_errors += ['Row {} is missing {}'.format(row_number, field)]

            image_paths = [path.replace('\\', '/') for path in row[2:6]]

            for image_path in image_paths:
                if not image_path:
                    continue
                if not os.path.isfile(image_path):
                    row_errors += ['Row {} references missing image file: {}'.format(row_number, image_path)]

            mp3_path = row[7].replace('\\', '/')
            if not os.path.isfile(mp3_path):
                row_errors += ['Row {} references missing audio file: {}'.format(row_number, mp3_path)]

            if row_errors:
                error_log.append(row_errors)
    for row_errors in error_log:
        for error in row_errors:
            print(error)


def make_slideshows_and_upload_from_spreadsheet(row_start, row_end):
    with open('batch_test_environment/frontera_upload_guide.csv') as f:
        file_reader = list(csv.reader(f))
        for row in file_reader[row_start - 1: row_end - 1]:
            title = row[0]
            description = row[1].replace(';', '\n')
            image_paths = ["batch_test_environment/" + row[i].replace('\\', '/') for i in range(2, 6) if row[i] != '']
            if not all(os.path.isfile(ip) for ip in image_paths):
                print("Skipped processing {} because of invalid image path".format(title))
                continue
            audio_path = "batch_test_environment/" + row[7].replace('\\', '/')
            if not os.path.isfile(audio_path):
                print("Skipped processing {} because of invalid audio path".format(title))
                continue

            if len(image_paths) == 0:
                thumbnail_path = 'batch_test_environment/frontera/arhoolie_credit_screen_small.PNG'
            else:
                thumbnail_path = resize_images(image_paths[:1], x=640, y=360)[0]

            movie_path = make_video_from_image_and_mp3_paths(image_paths, audio_path, overwrite=True)
            upload_command = get_video_upload_command(title, description, movie_path, thumbnail_path)
            p = subprocess.Popen(upload_command, shell=True, executable='/bin/sh', stdout=subprocess.PIPE)
            p.wait()
            if p.returncode == 0:
                print("Successfully uploaded {}".format(movie_path))
            else:
                print("Failed to upload {}".format(movie_path))






test_img_list = ['batch_test_environment\\frontera\\MUS_33JPG\\mus_33_dm-1471_a.jpg',
                 'batch_test_environment/frontera/MUS_33JPG/mus_33_dm-1471_b.jpg',
                 'batch_test_environment/frontera/MUS_33JPG/mus_33_dm-1471_back.jpg',
                 'batch_test_environment/frontera/MUS_33JPG/mus_33_dm-1471_front.jpg']

test_mp3_path = 'batch_test_environment/frontera/MUS_33mp3/mus_33_dm-1471_b1.mp3'


# make_video_from_image_and_mp3_paths(test_img_list, test_mp3_path, overwrite=True

# make_slideshows_and_upload_from_spreadsheet(2, 12)

verify_spreadsheet_files()
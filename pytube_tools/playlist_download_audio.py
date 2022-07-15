import pytube as pt
import json
from os.path import join, splitext
import os
from conversion_tools import mp4_to_mp3
from mp3_metadata_edit import edit_mp3_data
import requests

def main():
    #######################
    #    INPUT PARAMS     #
    #######################

    playlist_link = 'https://www.youtube.com/playlist?list=PLCCyxL9W8FrXtsJtbnZ9Vu0r94bm2NFp3'
    json_dir = r'D:\py-tools\pytube_tools\download_record.json'
    audio_output_dir = r'D:\Music\youtube_downloads'

    #######################

    # loading json
    with open(json_dir) as json_file:
        record = json.load(json_file)

    # creating playlist object
    playlist = pt.Playlist(playlist_link)

    # make directory to playlist
    if not os.path.exists(join(audio_output_dir, playlist.title)):
        os.mkdir(join(audio_output_dir, playlist.title))

    # album art directory
    art_path = join(audio_output_dir, playlist.title + r'\album_art')

    # make a directory to save album art to 
    if not os.path.exists(art_path):
        os.mkdir(art_path)

    # make directory for mp4 files
    if not os.path.exists(join(audio_output_dir, playlist.title + r'\mp4')):
        os.mkdir(join(audio_output_dir, playlist.title + r'\mp4'))

    # check if playlist exists in the record yet
    if playlist.title not in record.keys():
        # make entry if it doesn't exist yet
        record[playlist.title] = {}

    # loop through videos in playlist
    for i, video in enumerate(playlist.videos):
        # check record to see if the video has been downloaded before
        if video.title in record[playlist.title].keys():
            continue
        try:
            # if it hasn't been downloaded then download it
            stream = video.streams.get_audio_only('mp4')
            stream.download(join(audio_output_dir, playlist.title + '\mp4'))

            # update the records
            record[playlist.title][video.title] = playlist.video_urls[i]

            # grab the thumbnail to use as album art
            thumbnail = requests.get(video.thumbnail_url).content
            with open(join(art_path, video.title+'.jpg'), 'wb') as handler:
                handler.write(thumbnail)

        except:
            print(f'ERROR: Unable to download {video.title}')

    # save the record dict to json
    with open(json_dir, 'w') as json_file:
        json.dump(record, json_file)

    # now we want to convert the mp4's to mp3's
    mp4_dir = join(audio_output_dir, playlist.title + '\mp4')

    for i, file in enumerate(os.listdir(mp4_dir)):
        # split the name from file extension
        name = splitext(file)[0]
        print(join(audio_output_dir, playlist.title, name + '.mp3'))

        # convert mp4 to mp3
        mp4_to_mp3(join(mp4_dir,file), join(audio_output_dir, playlist.title, name + '.mp3'))

        # remove the mp4 file
        os.remove(join(mp4_dir,file))

        # add the album art and edit metadata
        edit_mp3_data(join(audio_output_dir, playlist.title, name + '.mp3'), join(art_path, name, + '.jpg'), name)

if __name__ == '__main__':
    main()
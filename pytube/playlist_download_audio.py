import pytube as pt
import json
from os.path import join

#######################
#    INPUT PARAMS     #
#######################

playlist_link = 'https://www.youtube.com/playlist?list=PLCCyxL9W8FrXtsJtbnZ9Vu0r94bm2NFp3'
json_dir = r'D:\py-tools\pytube\download_record.json'
audio_output_dir = r'D:\Music\youtube_downloads'

#######################

# loading json
with open(json_dir) as json_file:
    record = json.load(json_file)

# creating playlist object
playlist = pt.Playlist(playlist_link)

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
        print(video.streams.filter(only_audio=True))
        # if it hasn't been downloaded then download it
        stream = video.streams.get_audio_only('webm')
        stream.download(join(audio_output_dir, playlist.title))
        # update the records
        record[playlist.title][video.title] = playlist.video_urls[i]
    except:
        print(f'ERROR: Unable to download {video.title}')

# save the record dict to json
with open(json_dir, 'w') as json_file:
    json.dump(record, json_file)

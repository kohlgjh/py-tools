from moviepy.editor import AudioFileClip
from numpy import nbytes

def mp4_to_mp3(mp4_path, mp3_path, nbytes=4):
    '''
    Simple function that converts an mp4 file to an mp3 file.

    Parameters:
        mp4_path: the path to the mp4 file to be converted
        mp3_path: the path to where the resultant mp3 file will be saved
        nbytes: 2 for 16-bit and 4 for 32-bit sound
    '''
    mp4 = AudioFileClip(mp4_path)
    mp4.write_audiofile(mp3_path, nbytes=nbytes)
    mp4.close()


import eyed3
from eyed3.id3.frames import ImageFrame

def edit_mp3_data(mp3_path, art_path, name, artist=None, album=None):
    '''
    This function edits the mp3 metadata adding the art specified in 
    art_path as the mp3 album cover.
    
    Parameters:
        mp3_path: the path to the mp3 file
        art_path: the path to the album art file
        name: the title of the song/mp3
    '''
    # load the audio file
    audiofile = eyed3.load(mp3_path)

    # initialize the tag if there isn't one
    if (audiofile.tag == None):
        audiofile.initTag()

    # change the title of the file
    audiofile.tag.title = name

    # change the album name
    if album is not None: audiofile.tag.album = album
    else: audiofile.tag.album = name

    # change the artist
    if artist is not None: audiofile.tag.artist = artist
    else: audiofile.tag.artist = name

    # change the album art
    audiofile.tag.images.set(3, open(art_path, 'rb').read(), 'image/jpeg')

    # save the audiofile
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
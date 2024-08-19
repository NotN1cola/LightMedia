import os
import time
import threading
from pygame import mixer
from mutagen.mp3 import MP3
import yt_dlp as youtube_dl
from pysondb import PysonDB

sdb = PysonDB("songinfos_db.json")
cfg = PysonDB("config.json")

isPlaying = None
current_song_id = 0 

def getSongDuration(song_path):
    try:
        audio = MP3(song_path)
        return audio.info.length
    except FileNotFoundError:
        print(f"Error: File '{song_path}' not found.")
        return 0

def isSongPlaying():
    global isPlaying
    while True:
        isPlaying = mixer.music.get_busy()
        time.sleep(1)

def playSong(song_id):
    try:
        song_path = f"playlist_audios/{song_id}.mp3"
        mixer.music.load(song_path)
        mixer.music.play()
    except FileNotFoundError:
        print(f"Error: No file 'playlist_audios/{song_id}.mp3' found.")

def playSongGUI():
    global current_song_id
    mixer.init()

    while True:
        getSongInfo = sdb.get_by_query(lambda song: song["id"] == str(current_song_id))
        
        if getSongInfo:
            first_key = next(iter(getSongInfo))
            getSongTitle = getSongInfo[first_key]["title"]
        else:
            getSongTitle = "Unknown Title"

        threading.Thread(target=playSong, args=(current_song_id,)).start()
        threading.Thread(target=isSongPlaying).start()

        print("██╗     ██╗ ██████╗ ██╗  ██╗████████╗███╗   ███╗███████╗██████╗ ██╗ █████╗ ")
        print("██║     ██║██╔════╝ ██║  ██║╚══██╔══╝████╗ ████║██╔════╝██╔══██╗██║██╔══██╗")
        print("██║     ██║██║  ███╗███████║   ██║   ██╔████╔██║█████╗  ██║  ██║██║███████║")
        print("██║     ██║██║   ██║██╔══██║   ██║   ██║╚██╔╝██║██╔══╝  ██║  ██║██║██╔══██║")
        print("███████╗██║╚██████╔╝██║  ██║   ██║   ██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║")
        print("╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝ Created by notn1cola with 🩷")
        print(" ")
        print("Playing some music...")
        print(f"Title: {getSongTitle}")

        playedSeconds = 0

        while mixer.music.get_busy():
            current_seconds = mixer.music.get_pos() // 1000
            if playedSeconds != current_seconds:
                print("██╗     ██╗ ██████╗ ██╗  ██╗████████╗███╗   ███╗███████╗██████╗ ██╗ █████╗ ")
                print("██║     ██║██╔════╝ ██║  ██║╚══██╔══╝████╗ ████║██╔════╝██╔══██╗██║██╔══██╗")
                print("██║     ██║██║  ███╗███████║   ██║   ██╔████╔██║█████╗  ██║  ██║██║███████║")
                print("██║     ██║██║   ██║██╔══██║   ██║   ██║╚██╔╝██║██╔══╝  ██║  ██║██║██╔══██║")
                print("███████╗██║╚██████╔╝██║  ██║   ██║   ██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║")
                print("╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝ Created by notn1cola with 🩷")
                print(" ")
                print("Playing some music...")
                print(f"Title: {getSongTitle}")
                print(f"Played seconds: {current_seconds}")
                playedSeconds = current_seconds
            time.sleep(1)
            os.system("cls")

        print("Music stopped...")
        current_song_id += 1 
        if not os.path.exists(f"playlist_audios/{current_song_id}.mp3"):
            print("End of playlist.")
            exit()
        os.system("cls")

def getYoutubeSong():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    download_directory = os.path.join(script_directory, 'playlist_audios')

    downloadedSongNumber = len(os.listdir(download_directory))
    downloadedSong = f"{downloadedSongNumber}.mp3"

    print("Enter the URL of the song to download...")
    songUrl = input("∽ ")
    print("Downloading song...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_directory, downloadedSong),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(songUrl, download=True)
        getTitle = info_dict.get('title', None)

    os.rename(f"{os.path.join(download_directory, downloadedSong)}.mp3", f"playlist_audios/{downloadedSong}")

    # Include the 'id' key in your data
    infoAdd = sdb.add({
        'id': f'{downloadedSongNumber}',
        'title': f'{getTitle}'
    })

    print(f"Downloaded and saved: {getTitle} as {downloadedSong}")

    Main()

def Main():
    os.system("cls")
    print("██╗     ██╗ ██████╗ ██╗  ██╗████████╗███╗   ███╗███████╗██████╗ ██╗ █████╗ ")
    time.sleep(0.1)
    print("██║     ██║██╔════╝ ██║  ██║╚══██╔══╝████╗ ████║██╔════╝██╔══██╗██║██╔══██╗")
    time.sleep(0.1)
    print("██║     ██║██║  ███╗███████║   ██║   ██╔████╔██║█████╗  ██║  ██║██║███████║")
    time.sleep(0.1)
    print("██║     ██║██║   ██║██╔══██║   ██║   ██║╚██╔╝██║██╔══╝  ██║  ██║██║██╔══██║")
    time.sleep(0.1)
    print("███████╗██║╚██████╔╝██║  ██║   ██║   ██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║")
    time.sleep(0.1)
    print("╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝ Created by notn1cola with 🩷")
    time.sleep(0.1)
    print(" ")
    time.sleep(0.1)
    print(" [1] ▶ Play the playlist")
    time.sleep(0.1)
    print(" [2] ▶ Add a song from Youtube")
    time.sleep(0.1)
    print(" [3] ▶ Add a song from Spotify")
    time.sleep(0.1)
    print(" [4] ▶ Remove a song")
    time.sleep(0.1)
    print(" [5] ▶ Credits")
    time.sleep(0.1)
    print(" [6] ▶ Exit")
    time.sleep(0.1)
    print(" ")

    todo = input("∽ ")
    if todo == "1":
        playSongGUI()
    elif todo == "2":
        getYoutubeSong()
    elif todo == "3":
        print("Not implemented yet...")
    elif todo == "4":
        print("Not implemented yet...")
    elif todo == "5":
        print("Not implemented yet...")
    elif todo == "6":
        print("Exiting the program...")
        exit()

if __name__ == "__main__":
    Main()

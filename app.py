from flask import Flask, render_template, request
from pytube import YouTube, Playlist
import threading

app = Flask(__name__)

def download_video(video_url, quality):
    video = YouTube(video_url)
    video.streams.filter(res=quality).first().download()

def download_playlist(playlist_url, quality):
    p = Playlist(playlist_url) 
    for video in p.videos:
        video.streams.filter(res=quality).first().download()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        playlist_url = request.form.get('playlist_url')
        video_url = request.form.get('video_url')
        quality = request.form.get('quality')

        if playlist_url:  # If playlist URL is provided
            threading.Thread(target=download_playlist, args=(playlist_url, quality)).start()
            return "Download started for playlist: " + playlist_url

        elif video_url:  # If video URL is provided
            threading.Thread(target=download_video, args=(video_url, quality)).start()
            return "Download started for video: " + video_url

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

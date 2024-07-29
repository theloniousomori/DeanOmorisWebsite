from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os


app = Flask(__name__)
application = app


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', current_page='contact')

def load_albums():
    with open('data/albums.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html', current_page='home')

@app.route('/album/<int:album_id>')
def album(album_id):
    albums = load_albums()
    album = next((a for a in albums if a['id'] == album_id), None)
    
    lyrics_file_path = os.path.join("data/lyrics", album.get('lyrics_file', ''))
    if os.path.exists(lyrics_file_path):
        with open(lyrics_file_path, 'r') as f:
            lyrics_data = json.load(f)
    else:
        lyrics_data = {"tracks": []}

    return render_template('album.html', album=album, lyrics_data=lyrics_data)

@app.route('/discography')
def discography():
    albums = load_albums()
    return render_template('discography.html', albums=albums, current_page='discography')

@app.route('/about')
def about():
    return render_template('about.html', current_page='about')

@app.route('/film')
def film():
    return render_template('film.html', current_page='film')

@app.route('/causes')
def causes():
    return render_template('causes.html', current_page='causes')


if __name__ == '__main__':
    app.run(debug=True)
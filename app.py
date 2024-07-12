from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_albums():
    with open('data/albums.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    albums = load_albums()
    return render_template('index.html', albums=albums)

@app.route('/album/<int:album_id>')
def album(album_id):
    albums = load_albums()
    album = next((a for a in albums if a['id'] == album_id), None)
    return render_template('album.html', album=album)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/film')
def film():
    return render_template('film.html')

@app.route('/causes')
def causes():
    return render_template('causes.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
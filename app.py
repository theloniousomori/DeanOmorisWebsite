from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)
application = app

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Secret key for session management
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        msg = Message(subject, 
                      sender=email, 
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"From: {name} <{email}>\n\n{message}"

        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message: {e}', 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')

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
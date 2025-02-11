"""This module contains the web application for the Dumpert video downloader."""
from flask import Flask, render_template, request, flash, send_file
import download_dumpert_video
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders the index page."""
    if request.method == 'POST' and request.form.get('url'):
        url = request.form['url']
        if not url:
            flash('URL is required!')
        else:
            return send_file(download_dumpert_video.download_video(url), as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)

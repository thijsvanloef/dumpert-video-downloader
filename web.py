"""This module contains the web application for the Dumpert video downloader."""
from flask import Flask, render_template, request, flash, send_file
from download_dumpert_video import verify_input, download_video
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders the index page."""
    if request.method == 'POST' and request.form.get('url'):
        url = request.form['url']
        try:
            return send_file(download_video(url), as_attachment=True)
        except Exception as e:
            flash(f'Error downloading video: {str(e)}')
    return render_template('index.html')
    
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080, threads=4)

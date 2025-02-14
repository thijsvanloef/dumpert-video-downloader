from flask import Flask, render_template, request, flash, send_file, Response, jsonify
from download_dumpert_video import download_video
import secrets
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders the index page."""
    if request.method == 'POST' and request.form.get('url'):
        url = request.form['url']
        try:
            file_path = download_video(url)
            if not os.path.exists(file_path):
                raise FileNotFoundError("Bestand niet gevonden.")

            return jsonify({"success": True, "message": "Download gelukt!", "file": file_path})

        except Exception as e:
            return jsonify({"success": False, "message": "Error bij downloaden", "error": str(e)})

    return render_template('index.html')

@app.route('/download')
def download():
    """Serve the downloaded file."""
    file_path = request.args.get('file')
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Bestand niet gevonden", 404

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080, threads=4)

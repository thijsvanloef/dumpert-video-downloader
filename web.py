# filepath: app.py
from flask import Flask, render_template, request, url_for, flash, redirect, send_file
import download_dumpert_video


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing123'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not url:
            flash('URL is required!')
        if url:
            return send_file(download_dumpert_video.download_video(url), as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080) 
    # app.run(debug=True)
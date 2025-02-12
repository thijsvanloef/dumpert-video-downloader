"""This module contains the web application for the Dumpert video downloader."""
from flask import Flask, render_template, request, flash, send_file, Response
from download_dumpert_video import download_video
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


@app.route('/robots.txt')
def robots_txt():
    """Serves the robots.txt file."""
    content = "User-agent: *\nAllow: /\n\nSitemap: https://dumpert.loef.dev/sitemap.xml"
    return Response(content, mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap_xml():
    """Serves the sitemap.xml file."""
    content = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://dumpert.loef.dev/</loc>
            <changefreq>weekly</changefreq>
        </url>
    </urlset>"""
    return Response(content, mimetype='application/xml')


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080, threads=4)

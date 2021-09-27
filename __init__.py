from flask import Flask
from flask import render_template, redirect

import subprocess
from os.path import exists

app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect("https://lafabricationnumerique.fr/")

@app.route('/<uuid:cert_id>')
def show_cert(cert_id):
    certificate = get_cert(cert_id)
    return render_template('index.html', certificate=certificate)

def get_cert(cert_id):
    cert_id = str(cert_id)
    if exists('./static/' + cert_id + '.sig') and exists('./static/' + cert_id + '.pdf') and exists('./static/' + cert_id + '.png'):
        subprocess_msg = subprocess.run(['gpg', '--verify', 'static/' + cert_id + '.sig', 'static/' + cert_id + '.pdf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return {
            "id": cert_id,
            "gpg_msg": str(subprocess_msg.stderr)
        }
    else:
        return None

if __name__ == "__main__":
  app.run(debug=False)


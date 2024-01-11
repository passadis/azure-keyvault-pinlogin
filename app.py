from flask import Flask, render_template, request, redirect, url_for, flash
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)
app.secret_key = 'edF32ert44rfgSAv2'  # Change to a strong secret key

# Azure Key Vault setup
key_vault_name = os.environ["KEY_VAULT_NAME"]
kv_uri = f"https://{key_vault_name}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=kv_uri, credential=credential)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pin = request.form['pin']
        secret_name = f"secret-{pin}"
        try:
            retrieved_secret = client.get_secret(secret_name)
            # Assuming the secret value is in 'username:password' format
            username, password = retrieved_secret.value.split(':')
            # Redirect to success page or pass username/password to the template
            return render_template('success.html', username=username, password=password)
        except Exception as e:
            # Handle error (e.g., secret not found)
            flash('Invalid PIN or secret not found.')
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)

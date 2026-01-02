#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "flask",
#     "PyYAML",
#     "requests",
#     "xero-python",
# ]
# ///
"""
Xero API Connector

This script handles the OAuth2 authentication flow with Xero to generate a .token.json file.
It starts a local web server to receive the callback from Xero.

Usage:
    ./xero_connect.py

Requirements:
    - xero_config.yaml (with CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
"""
import yaml
import os
import sys
import base64
import requests
import webbrowser
from flask import Flask, request
from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token

def load_config(config_file='xero_config.yaml'):
    if not os.path.exists(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        return None
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def save_token(token_data, token_file='.token.json'):
    import json
    with open(token_file, 'w') as f:
        json.dump(token_data, f, indent=4)
    print(f"Token saved to {token_file}")

def get_xero_client(config):
    api_client = ApiClient(
        Configuration(
            debug=True,
            oauth2_token=OAuth2Token(
                client_id=config['CLIENT_ID'],
                client_secret=config['CLIENT_SECRET']
            ),
        ),
        pool_threads=1,
    )
    return api_client

def start_auth_server(config):
    app = Flask(__name__)

    # Disable flask banner
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.route("/callback")
    def callback():
        code = request.args.get("code")
        if not code:
            return "Error: No code provided", 400

        # Exchange code for token
        token_url = "https://identity.xero.com/connect/token"

        # Basic Auth header
        auth_str = f"{config['CLIENT_ID']}:{config['CLIENT_SECRET']}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config['REDIRECT_URI']
        }

        try:
            response = requests.post(token_url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()

            save_token(token_data)

            return "Authentication successful! You can close this window and return to the terminal."

        except Exception as e:
            return f"Error exchanging token: {str(e)}", 500

    return app

def generate_auth_url(config):
    scope_str = config.get('SCOPE', 'offline_access accounting.transactions accounting.settings')

    base_url = "https://login.xero.com/identity/connect/authorize"
    params = {
        "response_type": "code",
        "client_id": config['CLIENT_ID'],
        "redirect_uri": config['REDIRECT_URI'],
        "scope": scope_str,
        "state": "123"
    }

    import urllib.parse
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return url

if __name__ == "__main__":
    config = load_config()
    if config:
        if config['CLIENT_ID'] == "YOUR_CLIENT_ID_HERE":
            print("Please update xero_config.yaml with your actual CLIENT_ID and CLIENT_SECRET.")
        else:
            auth_url = generate_auth_url(config)
            print(f"\nOpening browser to: {auth_url}")
            print("Waiting for callback on http://localhost:8888/callback ...")

            # Open browser automatically
            webbrowser.open(auth_url)

            # Start server
            app = start_auth_server(config)
            app.run(port=8888)

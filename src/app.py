"""Demo Python microservice using vulnerable dependencies for CVE Fixer testing."""

import os
import yaml
import urllib3
import jinja2
from PIL import Image
from flask import Flask, jsonify, request

app = Flask(__name__)
http = urllib3.PoolManager()


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration using PyYAML (demonstrates vulnerable PyYAML usage)."""
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            # Note: PyYAML 5.3 yaml.load without Loader or with FullLoader has known vulnerabilities
            return yaml.load(f, Loader=yaml.FullLoader) or {}
    return {"app": "cve-dummy-app", "env": "demo", "version": "1.0.0"}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "cve-dummy-python-api"})


@app.route("/fetch", methods=["GET"])
def fetch_data():
    """Fetch external data using urllib3."""
    url = request.args.get("url", "https://httpbin.org/get")
    response = http.request("GET", url, timeout=5.0)
    return jsonify({
        "status": response.status,
        "data": response.data.decode("utf-8", errors="replace"),
    })


@app.route("/render", methods=["POST"])
def render_template():
    """Render template using Jinja2."""
    template_str = request.json.get("template", "Hello {{ name }}!")
    context = request.json.get("context", {"name": "World"})
    template = jinja2.Template(template_str)
    rendered = template.render(**context)
    return jsonify({"rendered": rendered})


if __name__ == "__main__":
    config = load_config()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="127.0.0.1", port=port)

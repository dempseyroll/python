from flask import Flask, jsonify, abort, render_template_string
import random

app = Flask(__name__)

systems_dict = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

current_damaged_system_name = None

def systems():
    systems = {
        "navigation": "NAV-01",
        "communications": "COM-02",
        "life_support": "LIFE-03",
        "engines": "ENG-04",
        "deflector_shield": "SHLD-05"
    }
    systems_list = systems.keys()
    system_damaged = random.choices(list(systems_list))
    return system_damaged

@app.route('/status')
def get_status():
    global current_damaged_system_name
    system = systems()[0]
    current_damaged_system_name = system
    return jsonify({"damaged_system": system})

@app.route('/repair-bay')
def get_repair():
    if not current_damaged_system_name:
        return "No damaged system reported yet. Please call /status first.", 400

    system_code = systems_dict.get(current_damaged_system_name, "UNKNOWN")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{system_code}</div>
    </body>
    </html>
    """
    return html

@app.route('/teapot', methods=['POST'])
def post_teapot():
    abort(418)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# URL usada:
# {
# }

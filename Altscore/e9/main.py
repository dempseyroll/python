from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/phase-change-diagram')
def hidraulic_fluid():
	const = 0.00035
	pressure = float(request.args.get('pressure'))
	results = pressure * const
	return jsonify({"specific_volume_liquid": results, "specific_volume_vapor": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


# LOGS:

# 127.0.0.1 - - [25/Apr/2025 01:48:38] "GET /phase-change-diagram?pressure=1.4395621256014344 HTTP/1.1" 200 -
# 127.0.0.1 - - [25/Apr/2025 01:48:39] "GET /phase-change-diagram?pressure=9.746216852463457 HTTP/1.1" 200 -
# 127.0.0.1 - - [25/Apr/2025 01:48:39] "GET /phase-change-diagram?pressure=5.825686592318929 HTTP/1.1" 200 -
# 127.0.0.1 - - [25/Apr/2025 01:48:40] "GET /phase-change-diagram?pressure=8.979489013375838 HTTP/1.1" 200 -
# 127.0.0.1 - - [25/Apr/2025 01:48:40] "GET /phase-change-diagram?pressure=9.110857737688912 HTTP/1.1" 200 -
# 127.0.0.1 - - [25/Apr/2025 01:48:41] "GET /phase-change-diagram?pressure=3.4079028872751143 HTTP/1.1" 200 -
# 127.0.0.1 - - [25/Apr/2025 01:48:41] "GET /phase-change-diagram?pressure=1.2351564025832287 HTTP/1.1" 200 -
# 127.0.0.1 - - [25/Apr/2025 01:48:42] "GET /phase-change-diagram?pressure=8.53092530315315 HTTP/1.1" 200 -
# 127.0.0.1 - - [25/Apr/2025 01:48:42] "GET /phase-change-diagram?pressure=6.440377855431648 HTTP/1.1" 200 -
# 127.0.0.1 - - [25/Apr/2025 01:48:43] "GET /phase-change-diagram?pressure=10.0 HTTP/1.1" 200 -

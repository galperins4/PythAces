from flask import Flask, request
import json
app = Flask(__name__)

@app.route("/prices")
def prices():
    return "Return Employee JSON data"

@app.route('/contracts', methods=['POST']) 
def contracts():
    print(request.json)
    return json.dumps(request.json)

if __name__ == "__main__":
    app.run(host = "192.168.1.116")
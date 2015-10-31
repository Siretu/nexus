import os
import socket
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/nexus/api/lifx/status', methods=["GET"])
def get_light_status():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5432))
    status = sock.recv(1024)

    return jsonify({'status':status})

@app.route('/nexus/api/lifx/status', methods=["POST"])
def set_light_status():
    if not request.json or not "status" in request.json:
        abort(400)
    
    status = request.json["status"]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5432))
    sock.recv(1024)
    if status == "True":
        sock.send("on")
        status = True
    else:
        sock.send("off")
        status = False
    return jsonify({"status":status}), 201




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

#!/usr/bin/python

import os
import socket
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/nexus/api/lifx/status', methods=["GET"])
def get_light_status():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5432))
    status = sock.recv(1024) == "True"

    return jsonify({'status': status})

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
    return jsonify({"status": status}), 201

def jasper_status():
    cmd = os.popen("ps aux | grep jasper")
    status = "jasper.py" in cmd.read()
    return status

def restart_jasper():
    os.system("restart ../jasper/jasper.py")

@app.route('/nexus/api/jasper/status', methods=["GET"])
def get_jasper_status():
    return jsonify({"status": jasper_status()})

@app.route('/nexus/api/jasper/status', methods=["POST"])
def set_jasper_status():
    print "Foo: " + str(request.json)
    print "Bar: " + request.data
    if not request.json or not "status" in request.json:
        pass
        abort(400)
    if request.json["status"]:
        force = False # Should we force restart?
        if "force" in request.json and request.json["force"] == True:
            force = True
            
        currently_on = jasper_status()

        if not currently_on or force:
            restart_jasper()
            
            
        return jsonify({"status": True})
    else:
        os.system("pkill -f jasper.py")
        return jsonify({"status": False})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

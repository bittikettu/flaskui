# app.py
import datetime
from flask import Flask, render_template, request, jsonify
import platform
import socket
import psutil
import subprocess
import json

class SystemInfo:
    def __init__(self):
        self.machine_name = platform.node()
        self.processor_name = platform.processor()
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.disk_usage = self.get_disk_usage()
        self.root_disk_usage = self.filter_disk_usage('/')
        self.root_disk_percent = self.root_disk_usage[0]['percent']

    def get_disk_usage(self):
        partitions = psutil.disk_partitions()
        disk_usage_info = []
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage_info.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
        return disk_usage_info
    
    def filter_disk_usage(self, mountpoint):
        filtered_disk_info = [disk for disk in self.disk_usage if disk['mountpoint'] == mountpoint]
        return filtered_disk_info

    def __str__(self):
        return f"Machine Name: {self.machine_name}\nProcessor Name: {self.processor_name}\nHostname: {self.hostname}\nIP Address: {self.ip_address}"

system_info = SystemInfo()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',system_info=system_info, utc_dt=datetime.datetime.utcnow())

@app.route('/about/')
def about():
    return render_template('about.html', system_info=system_info)

@app.route('/log/')
def log():
    return render_template('syslog.html', system_info=system_info)

@app.route('/run', methods=['GET'])
def run_command():
    command = request.args.get('command')
    print(command)
    if command is None:
        return jsonify({"error": "Missing 'command' parameter"}), 400

    try:
        result = run_system_command(command)
        try:
            json_result = json.loads(result)
            return json_result
        except json.JSONDecodeError:
            return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_system_command(command):
    result = subprocess.check_output(command, shell=True, text=True)
    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


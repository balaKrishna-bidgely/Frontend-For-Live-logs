import os
import time
import threading
import paramiko
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

active_connections = {}

# Map jumphost aliases to hostnames/IPs
JUMP_HOSTS = {
                'jhnonprodqa': 'jumphost-nonprodqa.bidgely.com',
                'jhuat': 'jumphost-uat.bidgely.com',
                'jhproductqa': 'jumphost-productqa.bidgely.com',
                'jhmeuat': 'jumphost-meuat.bidgely.com'
}

class SSHLogStreamer:
    def __init__(self, jumphost, service_ip, ssh_password, service_password, log_path, room_id):
        self.jumphost = jumphost
        self.service_ip = service_ip
        self.ssh_password = ssh_password
        self.service_password = service_password
        self.log_path = log_path
        self.room_id = room_id
        self.client = None
        self.channel = None
        self.is_running = False

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            socketio.emit('status', {'message': f'Connecting to {self.jumphost}...'}, room=self.room_id)
            self.client.connect(hostname=self.jumphost, username=os.getenv('SSH_USERNAME'), password=self.ssh_password, timeout=20)
            socketio.emit('status', {'message': f'SSH connection established to {self.jumphost}'}, room=self.room_id)
            return True
        except Exception as e:
            socketio.emit('error', {'message': f'SSH connection failed: {str(e)}'}, room=self.room_id)
            return False

    def stream_logs(self):
        try:
            if not self.connect():
                return

            self.channel = self.client.invoke_shell()
            time.sleep(10)
            socketio.emit('status', {'message': f'Logging into service {self.service_ip}...'}, room=self.room_id)

            # Run login-bops
            self.channel.send(f'./login-bops {self.service_ip}\n')
            time.sleep(2)
            self.channel.send(self.service_password + '\n')
            time.sleep(2)
            self.channel.send('yes\n')
            time.sleep(2)

            socketio.emit('status', {'message': 'Login successful. Navigating to log directory...'}, room=self.room_id)

            file_path = self.log_path
            self.channel.send(f'tail -f {file_path}\n')

            self.is_running = True
            socketio.emit('connected', {'message': f'Streaming logs from {self.service_ip}'}, room=self.room_id)

            buffer = ""
            while self.is_running:
                if self.channel.recv_ready():
                    data = self.channel.recv(4096).decode('utf-8', errors='ignore')
                    if data:
                        buffer += data
                        lines = buffer.split('\n')
                        buffer = lines[-1]
                        for line in lines[:-1]:
                            socketio.emit('log_data', {'data': line}, room=self.room_id)
                time.sleep(0.1)
        except Exception as e:
            socketio.emit('error', {'message': f'Error streaming logs: {str(e)}'}, room=self.room_id)
        finally:
            self.disconnect()

    def disconnect(self):
        self.is_running = False
        try:
            if self.channel and not self.channel.closed:
                self.channel.close()
            if self.client:
                self.client.close()
        except Exception:
            pass


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    print(f'Client connected: {request.sid}')
    emit('response', {'data': 'Connected to server'})


@socketio.on('disconnect')
def on_disconnect():
    print(f'Client disconnected: {request.sid}')
    if request.sid in active_connections:
        active_connections[request.sid].disconnect()
        del active_connections[request.sid]


@socketio.on('start_streaming')
def start_streaming(data):
    try:
        jumphost_alias = data.get('jumphost')  # frontend value
        service_ip = data.get('host')
        log_path = data.get('log_path')

        if not jumphost_alias or not service_ip or not log_path:
            emit('error', {'message': 'Please provide jumphost, host, and log_path'})
            return

        jumphost = JUMP_HOSTS.get(jumphost_alias)  # resolve alias
        if not jumphost:
            emit('error', {'message': f'Unknown jumphost alias: {jumphost_alias}'})
            return

        ssh_password = os.getenv('SSH_PASSWORD')
        service_password = os.getenv('SERVICE_PASSWORD')

        room_id = request.sid
        join_room(room_id)

        streamer = SSHLogStreamer(jumphost, service_ip, ssh_password, service_password, log_path, room_id)
        active_connections[room_id] = streamer

        thread = threading.Thread(target=streamer.stream_logs)
        thread.daemon = True
        thread.start()

    except Exception as e:
        emit('error', {'message': f'Internal error: {str(e)}'})



@socketio.on('stop_streaming')
def stop_streaming():
    room_id = request.sid
    if room_id in active_connections:
        active_connections[room_id].disconnect()
        del active_connections[room_id]
        emit('disconnected', {'message': 'Stopped streaming logs'})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5500, debug=False)
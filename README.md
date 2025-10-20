# Live Log Viewer Dashboard

A web-based dashboard to view live logs from remote services via SSH in real-time.

## Features

- 🔐 Secure SSH connection to remote services
- 📊 Real-time log streaming using WebSockets
- 🎨 Beautiful, responsive UI
- 🔄 Auto-scrolling log display
- 🛑 Easy start/stop controls
- 🗑️ Clear logs functionality

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd ~/Desktop/DashBoardForLogs
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
- Create a `.env` file in the project root
- Add the following variables:
   ```
   SSH_USERNAME=your_ssh_username
   SSH_PASSWORD=your_ssh_password
   SERVICE_PASSWORD=your_service_password
   SSH_KEY_PATH=~/.ssh/your_key.pem (optional)
   ```

## Usage

1. **Start the backend server:**
   ```bash
   python backend.py
   ```
   
   The server will start on `http://localhost:5000`

2. **Open your browser:**
   - Navigate to `http://localhost:5000`

3. **Fill in the connection details:**
   - **Service IP Address**: The IP of the remote service (e.g., 10.0.0.1)
   - **Username**: Your SSH username (default: jhnonprodqa)
   - **Password**: Your SSH password
   - **Log File Path**: Full path to the log file (e.g., /var/log/bidgely/ingesterJobs/gbUserDataIngester/gbUserDataIngester.log)

4. **Click "Start Streaming"** to begin viewing live logs

5. **Click "Stop Streaming"** to disconnect

## How It Works

1. **Frontend (HTML/CSS/JS)**:
   - Provides a user-friendly interface to input connection details
   - Uses WebSockets to maintain a real-time connection with the backend
   - Displays incoming log data in a scrollable terminal-like container

2. **Backend (Python)**:
   - Uses Flask for the web server
   - Uses Flask-SocketIO for WebSocket communication
   - Uses Paramiko for SSH connections
   - Executes `tail -f` command on the remote server
   - Streams log output back to the frontend in real-time

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  HTML/CSS/JS Frontend (index.html)                   │   │
│  │  - Connection form                                   │   │
│  │  - Real-time log display                             │   │
│  │  - WebSocket client                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↕ WebSocket
┌─────────────────────────────────────────────────────────────┐
│                  Python Backend (backend.py)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Flask + Flask-SocketIO Server                       │   │
│  │  - Handles WebSocket connections                     │   │
│  │  - Manages SSH connections (Paramiko)                │   │
│  │  - Streams log data in real-time                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↕ SSH
┌─────────────────────────────────────────────────────────────┐
│              Remote Service (via SSH)                        │
│  - Executes: tail -f /path/to/log/file                      │
│  - Streams log output                                        │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting

### Connection Failed
- Verify the IP address is correct
- Check username and password
- Ensure SSH access is enabled on the remote service
- Verify the log file path exists on the remote server

### No Logs Appearing
- Check that the log file path is correct
- Verify the log file has write permissions
- Ensure the log file is being actively written to

### Port Already in Use
- Change the port in `backend.py` (default: 5000)
- Or kill the process using port 5000:
  ```bash
  lsof -ti:5000 | xargs kill -9
  ```

## Security Notes

⚠️ **Important**: This application stores passwords in memory during the session. For production use:
- Use SSH key-based authentication instead of passwords
- Deploy behind HTTPS
- Implement proper authentication and authorization
- Use environment variables for sensitive configuration

## File Structure

```
DashBoardForLogs/
├── backend.py              # Python Flask backend with SSH streaming
├── templates/
│   └── index.html          # Frontend HTML/CSS/JS
├── requirements.txt        # Python dependencies
└── README.md              # This file
```


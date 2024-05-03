#!/bin/bash

# Stop script on any error
set -e

# Optional: Update and upgrade the system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install Python and necessary system utilities
sudo apt-get install -y python3 python3-pip python3-venv git

# Clone your repository (replace URL with your repository URL)
git clone https://github.com/AuspicesAI/ScytheEx.git /opt/ScytheEx
cd /opt/ScytheEx

# Optional: Setup Python virtual environment
# python3 -m venv venv
# source venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Create a systemd service file
echo "
[Unit]
Description=My Network Traffic Capture Service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/ScytheEx/backend
ExecStart=/usr/bin/python3 /opt/ScytheEx/backend/main.py
Restart=always

[Install]
WantedBy=multi-user.target
" | sudo tee /etc/systemd/system/Scytheex.service

# Enable and start the service
sudo systemctl enable Scytheex.service
sudo systemctl start Scytheex.service

echo "Installation complete. The service is now running."

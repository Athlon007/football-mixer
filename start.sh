#!/bin/sh

killer() {
    # IF variables are not setup, then exit
    if [ -z "$api_pid" ] || [ -z "$client_pid" ]; then
        exit
    fi
    
    kill $api_pid
    kill $client_pid
    exit
}

trap killer SIGINT SIGTERM EXIT

# Initializes the app's back-end and front-end.
# Check if 'python3', 'yarn' and 'node' are installed

if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found"
    exit
fi

if ! command -v yarn &> /dev/null
then
    echo "yarn could not be found"
    exit
fi

if ! command -v node &> /dev/null
then
    echo "node could not be found"
    exit
fi

# Node version must be either 18, 19, or 20
node_version=$(node -v)
if [[ $node_version != v18.* ]] && [[ $node_version != v19.* ]] && [[ $node_version != v20.* ]]; then
    echo "Node version must be either 18, 19, or 20"
    exit
fi

# check if virtualenv is installed
if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found"
    exit
fi

# Setup virtualenv (if not already setup)
echo "Setting up virtualenv..."
cd app
if [ ! -d ".venv" ]; then
    echo "Virtualenv not found. Creating..."
    virtualenv .venv
fi

# Activate virtualenv
echo "Activating virtualenv..."
source .venv/bin/activate
echo "Virtualenv activated!"

# Install back-end dependencies
echo "Installing back-end dependencies..."
python -m pip install -r requirements.txt
export FLASK_APP=app.py
echo "Back-end dependencies installed!"

# Start the back-end and continue in the background. save PID to a variable
api_pid=$(flask run)
echo "Back-end started on PID: $api_pid"

# Install front-end dependencies
echo "Installing front-end dependencies..."
cd ../client
yarn install
echo "Front-end dependencies installed!"

# Start the front-end and continue in the background. save PID to a variable
echo "Starting front-end..."
client_pid=$(yarn start)
echo "Front-end started on PID: $client_pid"

# Wait for the back-end and front-end to finish
wait $api_pid
wait $client_pid

# Deactivate virtualenv
deactivate

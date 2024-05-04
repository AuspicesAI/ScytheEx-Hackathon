#!/bin/bash

echo "Starting setup for ScytheEx-ai..."
echo "--------------------------------"
sleep 2

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python 3.10 or later."
    echo "Python installation instructions: https://www.python.org/downloads/"
    exit 1
fi
sleep 2

# Check if Poetry is installed
if ! command -v poetry &> /dev/null
then
    echo "Poetry not found, installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "Poetry installation complete."
    echo "--------------------------------"
    sleep 2
fi

# Navigate to the ScytheEx-ai directory
cd "$(dirname "$0")"

# Delete current poetry.lock file if it exists
if [ -f "poetry.lock" ]; then
    echo "Deleting existing poetry.lock file..."
    rm poetry.lock
    echo "poetry.lock file deleted."
    echo "--------------------------------"
    sleep 2
fi

# Recreate the poetry.lock file
echo "Creating new poetry.lock file..."
poetry lock
echo "poetry.lock file created."
echo "--------------------------------"
sleep 2

# Install dependencies
echo "Installing dependencies..."
poetry install
echo "Dependencies installed."
echo "--------------------------------"
sleep 2

# Create an IPython kernel for the project
echo "Creating an IPython kernel for ScytheEx-ai..."
poetry run python -m ipykernel install --user --name=ScytheEx-ai --display-name "Python (ScytheEx-ai)"
echo "IPython kernel for ScytheEx-ai created."
echo "--------------------------------"
sleep 2

# Check if the ScytheEx-ai has been created
echo "Verifying the creation of the ScytheEx-ai..."
if poetry run jupyter kernelspec list | grep -iq 'ScytheEx-ai'; then
    echo "ScytheEx-ai has been successfully created."
else
    echo "Error: ScytheEx-ai was not created successfully. Please check the installation logs for errors."
fi
echo "--------------------------------"
sleep 2

# Check if Poetry environment is set
poetryEnv=$(poetry env info -p)
if [ -z "$poetryEnv" ]; then
    echo "Poetry environment is not set. Please set up the environment manually."
else
    echo "Poetry environment is set up. Path: $poetryEnv"
    echo "If using VSCode, press Ctrl+Shift+P, type 'Python: Select Interpreter', and add the path:"
    echo "$poetryEnv"
fi

## Final message before dotenv setup
echo "Primary setup complete. Proceeding to dotenv-vault setup."
echo "--------------------------------"
sleep 2

# Check if Node.js and npm are installed
if ! command -v node &> /dev/null || ! command -v npm &> /dev/null
then
    echo "Node.js and npm are not installed. Please install them to proceed."
    echo "Node.js installation instructions: https://linuxtldr.com/npx-package-runner/"
    exit 1
fi
sleep 2

# Dotenv-vault setup
echo "Setting up dotenv-vault for environment variables..."
if [ ! -f ".env.vault" ]; then
    echo "No .env.vault file found. Attempting to connect to dotenv-vault..."
    # Attempt to connect to dotenv-vault
    npx dotenv-vault@latest new vlt_79a4218fb64985c6e5cdbcae5ee0cf074f4f5827a7911d2dea595e7b92ffbe9b
fi

# Final message with instructions to enter Poetry shell manually
echo "Primary setup complete."
echo "Please enter the Poetry shell manually by running 'poetry shell'."
echo "In the Poetry shell, you can run 'exit' to deactivate the environment."
echo "--------------------------------"

# Exit script
exit 0
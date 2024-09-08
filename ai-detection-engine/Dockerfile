# Use an official Python 3.10 runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Upgrade pip and install wheel
RUN pip install --progress-bar off --upgrade pip wheel

# Set environment variable to limit pip's concurrency
ENV MAX_CONCURRENCY=1

# Create a virtual environment and activate it
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Poetry with reduced resource usage
RUN pip install --progress-bar off poetry

# Copy pyproject.toml and poetry.lock files
COPY poetry.lock pyproject.toml ./

# Use Poetry to export dependencies to requirements.txt
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes

# Install dependencies from requirements.txt
RUN pip install --progress-bar off -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Command to run the application
CMD ["python", "./main.py"]

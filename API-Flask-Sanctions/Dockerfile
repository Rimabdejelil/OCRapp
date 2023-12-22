# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY api.py /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org Flask azure-cosmos

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "-m", "api", "run", "--host=0.0.0.0"]
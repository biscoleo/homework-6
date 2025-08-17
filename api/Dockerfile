
# lightweight Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . /app

RUN mkdir /logs

# Make port 8000 available for fastapi (this is the default fastapi/uvicorn port)
EXPOSE 8000

# Define the command to run your app when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000"]
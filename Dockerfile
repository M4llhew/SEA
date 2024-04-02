# Use the latest development version of Python (3.x) for now
FROM python:3.10.13

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

# Set the working directory in the container
WORKDIR SEA/djangoProject

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Collect static files
RUN python djangoProject/manage.py collectstatic --noinput

# Run the Django application
CMD ["python", "djangoProject/manage.py", "runserver", "0.0.0.0:8000"]
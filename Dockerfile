# Use a lightweight Python image as a base
FROM python:3.9-alpine  

# Set the working directory
WORKDIR /app

# Define environment variables if needed
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the project requirements
COPY requirements.txt ./

# Install dependencies 
RUN pip install -r requirements.txt
RUN apk add --no-cache bash

# Copy the project code
COPY . ./ 

# Expose the port Django will run on 
EXPOSE 8000

# Command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

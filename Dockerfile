# Use the official Python image from Docker Hub
FROM python:3.9-slim-buster

# Switch to root user to perform installation tasks
USER root

# Create a directory for your application
RUN mkdir /app

# Copy all files from your current directory to /app in the container
COPY . /app/

# Set the working directory to /app/
WORKDIR /app/

# Install dependencies from requirements_dev.txt
RUN pip install -r requirements_dev.txt

RUN pip install --upgrade pendulum

# Set environment variables for Airflow
ENV AIRFLOW_HOME='/app/airflow'
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING=True

# Initialize the Airflow database
RUN airflow db init

# Create an Airflow admin user (replace with your actual user details)
RUN airflow users create -e www.ayazkhan.com.21@gmail.com -f ayazulhaq -l yousafzi -p admin -r admin -u

# Make start.sh executable
RUN chmod 777 start.sh

# Update packages in the base image
RUN apt-get update -y

# Set the default entrypoint and command for the container
ENTRYPOINT [ "/bin/sh" ]
CMD ["start.sh"]

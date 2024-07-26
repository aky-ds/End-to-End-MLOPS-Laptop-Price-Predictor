# Use a more specific base image if possible
FROM python:3.9-slim-buster-slim

# Create a non-root user
RUN adduser --disabled-password airflow

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements_dev.txt requirements_dev.txt
RUN pip install --no-cache-dir -r requirements_dir.txt


# Set environment variables
ENV AIRFLOW_HOME /app/airflow
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT 1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING True

# Create Airflow directory and initialize database
RUN airflow init
RUN airflow db init

# Create an Airflow admin user (replace with your actual user details)
RUN airflow users create -e www.ayazkhan.com.21@gmail.com -f ayazulhaq -l yousafzi -p admin -r admin -u

# Make start.sh executable (if needed)
RUN chmod +x start.sh

# Switch to the airflow user
USER airflow

# Command to start your application
CMD ["start.sh"]

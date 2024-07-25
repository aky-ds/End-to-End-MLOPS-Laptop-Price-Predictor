#!/bin/bash

# Initialize Airflow metadata database
airflow db init

# Create an admin user if not exists
airflow users create -e www.ayazkhan.com.21@gmail.com -f ayazulhaq -l yousafzi -p admin -r admin -u

# Start Airflow webserver by default
exec airflow webserver

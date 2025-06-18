#!/bin/bash

# Add AWS credentials connection (replace with your own AWS access key and secret key)
airflow connections add aws_credentials \
  --conn-type aws \
  --conn-login YOUR_AWS_ACCESS_KEY_ID \
  --conn-password 'YOUR_AWS_SECRET_ACCESS_KEY'

# Add Redshift connection (replace with your own Redshift connection URI)
airflow connections add redshift \
  --conn-uri 'redshift://USERNAME:PASSWORD@HOST:PORT/DATABASE'

# Set Airflow variables for S3 pathing (replace with your own bucket and prefix)
airflow variables set s3_bucket YOUR_S3_BUCKET_NAME
airflow variables set s3_prefix YOUR_S3_PREFIX

# Optionally set AWS keys as Airflow variables if your pipeline retrieves them this way
airflow variables set AWS_ACCESS_KEY_ID YOUR_AWS_ACCESS_KEY_ID
airflow variables set AWS_SECRET_ACCESS_KEY YOUR_AWS_SECRET_ACCESS_KEY
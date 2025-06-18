# Data Pipelines Project — Airflow ETL with Redshift & S3

This repository contains my implementation of a scalable ETL data pipeline built with **Apache Airflow**, **Amazon Redshift**, and **Amazon S3**. It was created as part of my **[WGU] D608 Data Processing** coursework in collaboration with **Udacity**.

---

## Project Overview

The pipeline:
- Extracts JSON data (event logs and song metadata) from **S3**.
- Stages the data into **Redshift** staging tables.
- Loads a star schema with one fact table (`songplays`) and four dimension tables (`users`, `songs`, `artists`, `time`).
- Runs automated data quality checks to ensure data integrity.

The workflow is managed by an **Airflow DAG** (`final_project.py`), which is scheduled to run hourly.


## 💻 Repository Structure

```
├── final_project.py # Airflow DAG definition
├── plugins/
│ └── final_project_operators/
│ ├── data_quality.py # Custom operator for data quality checks
│ ├── load_dimension.py # Custom operator for loading dimension tables
│ ├── load_fact.py # Custom operator for loading fact table
│ └── stage_redshift.py # Custom operator for staging data from S3 to Redshift
├── set_connections_and_variables.sh # Script to set Airflow connections and variables
└── README.md # Project documentation
```

## How to Run

This project was developed and tested in the **Udacity Airflow workspace**.

If you'd like to adapt it to your own Airflow environment:
- Place `final_project.py` in your Airflow `dags/` directory.
- Place the `plugins/final_project_operators/` directory inside your Airflow `plugins/` directory.
- Be sure to replace placeholder values in `set_connections_and_variables.sh` with your actual AWS and Redshift credentials before use. This template is provided for educational purposes only — do not commit real credentials to version control.

---

## Notes

- The project builds upon starter code provided by **Udacity**. This repository includes only my custom code and configurations — no proprietary Udacity infrastructure files.

---

## Contact

Feel free to reach out if you'd like to collaborate or have questions about the implementation!

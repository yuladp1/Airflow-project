# 🛠️ Airflow ETL Pipeline: Product Sales Data

This project is an example of an **ETL pipeline using Apache Airflow**, running in a **Docker environment**.  
It fetches data from a public API, transforms it using Pandas, and saves the output to a CSV file.

---

## 📦 Features

- ⏬ **Extract**: Fetches product data from `https://fakestoreapi.com/products`
- 🔄 **Transform**: Aggregates data (e.g. sales by date or other transformation)
- 💾 **Load**: Saves the result as a CSV inside the Airflow container
- 🐳 **Runs via Docker** using the official [Airflow Docker image](https://airflow.apache.org/docs/docker-stack/)
- 🗂️ Task communication via **XCom**

---

## 🧱 Project Structure

AirflowDocker/
│
├── dags/
│ └── products_sales_report.py # The Airflow DAG definition
│
├── files/
│ └── sales_summary.csv # Final CSV output (after DAG run)
│
├── docker-compose.yml # Docker setup for Airflow
└── README.md # This file

---

## ▶️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/yuladp1/airflow-etl-pipeline.git
cd airflow-etl-pipeline

### 2. Start Airflow with Docker

bash
docker-compose up

3. Open Airflow UI
Go to http://localhost:8080
Log in with:

Username: airflow
Password: airflow

4. Trigger the DAG
Find the DAG named my_first_dag in the Airflow UI.

Turn it on and trigger it manually or let it run on schedule.

📄 Output
After the DAG completes, the resulting CSV will be saved in:

bash
files/sales_summary.csv
If you don't see the file on your host machine, it might be inside the Docker container. You can copy it like this:

bash
docker cp airflowdocker-airflow-webserver-1:/opt/airflow/files/sales_summary.csv ./files/

🔧 Notes
Python packages used:

pandas
requests
Airflow features:
PythonOperator
XCom
Custom DAGs with dependencies
Compatible with Airflow 2.x

📈 Future Improvements
Add unit tests for data transformation
Store CSV output to S3 or Google Cloud Storage
Add email alert on failure
Add data validation step

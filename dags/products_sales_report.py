import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import requests

# Task 1: Fetch data from a public API
def fetch_data(**context):
    url = "https://fakestoreapi.com/products"  # Replace with real API URL
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)

    # Push raw data to XCom for downstream tasks
    context['ti'].xcom_push(key='raw_sales', value=df.to_json())

# Task 2: Transform the fetched data
def transform_data(**context):
    raw_json = context['ti'].xcom_pull(key='raw_sales')
    df = pd.read_json(raw_json)

    # Compute revenue per product
    df['count'] = df['rating'].apply(lambda x: x['count'])
    df['revenue'] = df['price'] * df['count']

    # Group by category: total items sold and revenue
    summary = df.groupby('category').agg(
        total_items_sold=('count', 'sum'),
        total_revenue=('revenue', 'sum')
    ).reset_index()

    # Push transformed summary to XCom
    context['ti'].xcom_push(key='sales_summary', value=summary.to_json())

# Task 3: Save the result as a CSV file
def save_to_file(**context):
    # Pull transformed summary data from XCom
    summary_json = context['ti'].xcom_pull(key='sales_summary')
    summary_df = pd.read_json(summary_json)

    # Define the output directory inside the Docker container
    output_dir = '/opt/airflow/files'

    # Make sure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the DataFrame to CSV
    summary_df.to_csv(f'{output_dir}/sales_summary.csv', index=False)
    print("Saved to CSV")

# Define the DAG
with DAG(
    dag_id="products_sales_report",
    start_date=days_ago(1),
    schedule_interval=None,  # Manual trigger
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_data",
        python_callable=fetch_data,
        provide_context=True,
        dag=dag
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        provide_context=True,
        dag=dag
    )

    save_task = PythonOperator(
        task_id="save_to_file",
        python_callable=save_to_file,
        provide_context=True,
        dag=dag
    )

    # Set task dependencies: fetch → transform → save
    fetch_task >> transform_task >> save_task

from __future__ import annotations
import json
from textwrap import dedent
import pendulum
import numpy as np
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.Pipeline.training_pipeline import Training_Pipeline

training_pipeline = Training_Pipeline()

default_args = {
    'retries': 2,
}

with DAG(
    'Laptop-price-predictor',
    description='A training pipeline for laptop price prediction model',
    default_args=default_args,
    schedule_interval="@weekly",
    start_date=pendulum.parse('2024-07-25T00:00:00Z'),
    catchup=False,
    tags=['machine learning', 'regression', 'laptop']
) as dag:
    dag.doc_md = __doc__

    def data_ingestion(**kwargs):
        ti = kwargs['ti']
        train_path, test_path = training_pipeline.start_data_ingestion()
        ti.xcom_push(key='data_ingestion_artifacts', value={'train_path': train_path, 'test_path': test_path})

    data_ingestion_task = PythonOperator(
        task_id='data_ingestion',
        python_callable=data_ingestion,
        provide_context=True,  # This is needed to access context variables like kwargs
    )

    data_ingestion_task.doc_md = dedent(
        """\
        #### Data Ingestion
        This task performs data ingestion to create train and test datasets.
        """
    )

    def data_transform(**kwargs):
        ti = kwargs['ti']
        data_ingest_artfict = ti.xcom_pull(task_ids='data_ingestion', key='data_ingestion_artifacts')
        train_arr, test_arr = training_pipeline.start_data_transform(data_ingest_artfict)
        ti.xcom_push(key='data_transform_artifacts', value={'train_arr': train_arr.tolist(), 'test_arr': test_arr.tolist()})

    data_transform_task = PythonOperator(
        task_id='data_transform',
        python_callable=data_transform,
        provide_context=True,
    )

    data_transform_task.doc_md = dedent(
        """\
        #### Data Transform
        This task transforms the data into train and test arrays.
        """
    )

    def model_trainer(**kwargs):
        ti = kwargs['ti']
        data_transform_artfict = ti.xcom_pull(task_ids='data_transform', key='data_transform_artifacts')
        train_arr = np.array(data_transform_artfict['train_arr'])
        test_arr = np.array(data_transform_artfict['test_arr'])
        training_pipeline.start_model_trainer(train_arr, test_arr)

    model_train_task = PythonOperator(
        task_id='model_trainer',
        python_callable=model_trainer,
        provide_context=True,
    )

    model_train_task.doc_md = dedent(
        """\
        #### Model Trainer
        This task trains the machine learning model using the transformed data.
        """
    )

    # Define task dependencies
    data_ingestion_task >> data_transform_task >> model_train_task


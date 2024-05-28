# import json
from textwrap import dedent
# import datetime
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
import random


dag = DAG("my_dag", # Dag id
        start_date=pendulum.datetime(2023, 1 ,1), # start date, the 1st of January 2021 
        schedule_interval='@daily',  # Cron expression, here it is a preset of Airflow, @daily means once every day.
        description='A simple ML flow with DAG',
)

def _training_model():
    return random.randint(0, 10)


def _choosing_best_model(ti):
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    return 'accurate' if max(accuracies) > 8 else 'inaccurate'
    
training_model_tasks = [
    PythonOperator(
        task_id=f"training_model_{model_id}",
        python_callable=_training_model,
        op_kwargs={
            "model": model_id
        },
        dag=dag
    ) for model_id in ['A', 'B', 'C']
]

choosing_best_model = BranchPythonOperator(
    task_id="choosing_best_model",
    python_callable=_choosing_best_model,
    dag=dag
)


accurate = BashOperator(
    task_id="accurate",
    bash_command="echo 'Prediction'",
    dag=dag
)
inaccurate = BashOperator(
    task_id="inaccurate",
    bash_command=" echo 'Retraining'",
    dag=dag
)


training_model_tasks >> choosing_best_model >> [accurate, inaccurate]


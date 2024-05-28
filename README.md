# Testing Airflow


## Notes

Download default `docker-compose.yaml` file for Airlfow

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.3/docker-compose.yaml'
```

You need to prepare the environment a bit: create necessary files and folders, initialize the database



```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env

```

You can also delete the container and image after testing to avoid stress on your computer

```bash
docker-compose down --volumes --rmi all

```

The `webserver` will run on https://localhost:8080


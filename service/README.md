# CS446 Fraud Detection


## Setup


### One-time BigQuery setup
```bash
bq --project_id=cs446-fraud-detection mk --dataset fraud_dataset
bq mk --table cs446-fraud-detection:fraud_dataset.predictions transaction_id:INTEGER,tx_amount:FLOAT,tx_fraud:INTEGER,fraud_probability:FLOAT,processed_at:TIMESTAMP
```


### To delete BigQuery dataset
```bash
bq rm -r cs446-fraud-detection:fraud_dataset
```


### Deploy
```bash
./deploy.sh
```

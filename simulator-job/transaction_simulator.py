import pandas as pd
import json, time, glob, argparse
from google.cloud import pubsub_v1

PROJECT_ID = "cs446-fraud-detection"
TOPIC_ID = "transaction-events"

parser = argparse.ArgumentParser()
parser.add_argument("--days", nargs="+", default=["2018-04-01"], help="Which day files to load (e.g. 2018-04-01 2018-04-02)")
parser.add_argument("--all", action="store_true", help="Load all 183 days")
parser.add_argument("--limit", type=int, default=100, help="Max transactions to send")
parser.add_argument("--delay", type=float, default=0.05, help="Seconds between each transaction")
args = parser.parse_args()

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

if args.all:
    df = pd.concat([pd.read_pickle(f) for f in sorted(glob.glob("simulated-data-raw/data/*.pkl"))])
else:
    df = pd.concat([pd.read_pickle(f"simulated-data-raw/data/{day}.pkl") for day in args.days])

df = df.head(args.limit)

for _, row in df.iterrows():
    msg = {
        "TRANSACTION_ID": int(row["TRANSACTION_ID"]),
        "TX_DATETIME": str(row["TX_DATETIME"]),
        "CUSTOMER_ID": int(row["CUSTOMER_ID"]),
        "TERMINAL_ID": int(row["TERMINAL_ID"]),
        "TX_AMOUNT": float(row["TX_AMOUNT"]),
        "TX_FRAUD": int(row["TX_FRAUD"])
    }
    publisher.publish(topic_path, json.dumps(msg).encode("utf-8"))
    print(f"Published: {msg}")
    time.sleep(args.delay)
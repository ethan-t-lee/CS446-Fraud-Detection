import pandas as pd
import json, time, glob
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("cs446-fraud-detection", "transaction-events")    

##################################################
# Uncomment which option you want               
# Each day has ~10000 transactions              
##################################################

# --- OPTION 1: Single day ---
df = pd.read_pickle("simulated-data-raw/2018-04-01.pkl")
df = df.head(100)

# --- OPTION 2: Multiple specific days ---
# df = pd.concat([
#     pd.read_pickle("simulated-data-raw/2018-04-01.pkl"),
#     pd.read_pickle("simulated-data-raw/2018-04-02.pkl"),
#     pd.read_pickle("simulated-data-raw/2018-04-03.pkl"),
# ])

# If you run this option, thats 1.75 million transactions, so it will take a long time
# --- OPTION 3: All 183 days ---
# df = pd.concat([pd.read_pickle(f) for f in sorted(glob.glob("simulated-data-raw/*.pkl"))])

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
    time.sleep(0.01)     #Will delay each transaction posting, can change
import pandas as pd
import random
from faker import Faker
from datetime import datetime
import mlflow
import os

# --- Config ---
NUM_RECORDS = 10000
LABEL_NOISE_PCT = 0.1
SAVE_PATH = "../data/logs/noisy_simulated_audit_logs.csv"
EXPERIMENT_NAME = "AutoRiskAI_Experiment"

# --- Faker setup ---
fake = Faker()
Faker.seed(42)
random.seed(42)

# --- Event types and users ---
event_types = ["login_success", "login_failure", "file_access", "privilege_escalation", "config_change"]
users = [f"user_{i}" for i in range(1, 31)]
malicious_users = [f"bad_actor_{i}" for i in range(1, 6)]
all_users = users + malicious_users

# --- Generate records ---
records = []
for _ in range(NUM_RECORDS):
    is_malicious = random.random() < 0.1
    user = random.choice(malicious_users) if is_malicious else random.choice(users)
    ip_address = fake.ipv4_public()
    
    if is_malicious and random.random() < 0.5:
        event_type = "login_failure"
    else:
        event_type = random.choices(
            event_types, weights=[0.45, 0.3, 0.15, 0.05, 0.05], k=1
        )[0]

    timestamp = fake.date_time_between(start_date='-15d', end_date='now')
    
    record = {
        "timestamp": timestamp.isoformat(),
        "user": user,
        "ip_address": ip_address,
        "event_type": event_type,
        "resource": fake.uri_path(),
        "random_token": fake.sha1(),  # junk
        "label": int(is_malicious)
    }
    records.append(record)

# --- Create DataFrame ---
df = pd.DataFrame(records)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["event_hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek

# --- Inject label noise ---
flip_indices = df.sample(frac=LABEL_NOISE_PCT, random_state=42).index
df.loc[flip_indices, "label"] = 1 - df.loc[flip_indices, "label"]

# --- Save CSV ---
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
df.to_csv(SAVE_PATH, index=False)
print(f"Saved noisy audit logs to {SAVE_PATH}")

# --- Log to MLflow ---
mlflow.set_experiment(EXPERIMENT_NAME)
with mlflow.start_run(run_name="noisy_audit_dataset"):
    mlflow.log_param("num_records", NUM_RECORDS)
    mlflow.log_param("label_noise_pct", LABEL_NOISE_PCT)
    mlflow.log_artifact(SAVE_PATH, artifact_path="datasets")

    print("Logged dataset to MLflow")

import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

NUM_RECORDS = 5000 # 5000 rows of auit logs

event_types = ["login_success", "login_failure", "file_access", "privilege_escalation", "config_change"] #Action types in logs
users = [f"user_{i}" for i in range(1, 21)] #20 users

records = []

for _ in range(NUM_RECORDS):
    event_time = fake.date_time_between(start_date='-15d', end_date='now')
    record = {
        "timestamp": event_time.isoformat(),
        "user": random.choice(users),
        "ip_address": fake.ipv4_public(),
        "event_type": random.choices(
            event_types,
            weights=[0.5, 0.3, 0.1, 0.05, 0.05],  # simulate frequent logins and rare anomalies
            k=1 #Pick one
        )[0],
        "resource": fake.uri_path()
    }
    records.append(record)

df = pd.DataFrame(records)
df.to_csv("data/logs/simulated_audit_logs.csv", index=False)
print("Simulated audit logs saved.")

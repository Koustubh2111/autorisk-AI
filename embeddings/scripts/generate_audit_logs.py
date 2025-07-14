import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import numpy as np

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

NUM_RECORDS = 5000  # 5000 rows of audit logs

# Event types: added explicit anomaly event type, with higher anomaly frequency
event_types = ["login_success", "login_failure", "file_access", "privilege_escalation", "config_change", "anomaly_event"]
users = [f"user_{i}" for i in range(1, 21)]  # 20 users

records = []

for _ in range(NUM_RECORDS):
    event_time = fake.date_time_between(start_date='-15d', end_date='now')
    
    # Increase anomaly event frequency to ~10%
    event_type = random.choices(
        event_types,
        weights=[0.45, 0.25, 0.1, 0.05, 0.05, 0.10],  # anomaly_event weight 0.10
        k=1
    )[0]
    
    # Inject correlated anomaly feature values
    if event_type == "anomaly_event":
        # Randomly select failed login count higher for anomalies
        failed_logins = np.random.poisson(5) + 1
        # Randomly assign suspicious IP addresses (e.g., some private or rare ranges)
        ip_address = random.choice([
            fake.ipv4_private(),
            fake.ipv4_public(),
            "10.0.0." + str(random.randint(1, 255)),  # simulated suspicious private subnet
            "172.16.0." + str(random.randint(1, 255)),
        ])
    else:
        failed_logins = np.random.poisson(1)
        ip_address = fake.ipv4_public()
    
    record = {
        "timestamp": event_time.isoformat(),
        "user": random.choice(users),
        "ip_address": ip_address,
        "event_type": event_type,
        "resource": fake.uri_path(),
        "failed_logins_last_1h": failed_logins,
        "event_hour": event_time.hour
    }
    records.append(record)

df = pd.DataFrame(records)

# Add label for anomaly: 1 if anomaly_event, else 0
df['label'] = (df['event_type'] == 'anomaly_event').astype(int)

# Save to CSV
df.to_csv("../../data/logs/simulated_audit_logs_hard.csv", index=False)
print("Harder simulated audit logs saved.")

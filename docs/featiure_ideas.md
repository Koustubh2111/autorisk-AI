# Feature Ideas for Anomaly Detection

| Feature            | Type               | Description                                 | Why It Helps                                     |
|--------------------|--------------------|---------------------------------------------|-------------------------------------------------|
| `event_hour`       | Numeric            | Hour of event (0–23)                        | Unusual times (e.g., 3am) may indicate anomalies |
| `event_type_code`  | Categorical (int)  | Encoded event type                          | Helps model distinguish risky vs normal actions  |
| `resource_depth`   | Numeric            | URL depth (e.g., `/admin/settings`)        | Accessing deep/internal paths might signal risk  |
| `is_privileged_event` | Binary           | If event is escalation or config change    | Rare events often tied to breaches                 |
| `is_weekend`       | Binary             | Whether event happened on weekend           | Off-hour events often suspicious                   |
| `failed_logins_last_1h` | Numeric        | Count of failures in past 1 hour            | Brute-force or compromised account                 |
| `ip_event_count`   | Numeric            | Activity level from same IP                  | Unusual spike from IP may be bot                    |
| `user_event_rate`  | Numeric            | How active the user is                       | Dormant → Active could signal impersonation        |

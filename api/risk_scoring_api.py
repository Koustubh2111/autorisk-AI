from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import xgboost as xgb
from datetime import datetime
import shap
#uvicorn risk-scoring-api:app --reload  

app = FastAPI(title="Audit Log Risk Scoring API")


# Define the expected input format using Pydantic
class AuditLog(BaseModel):
    timestamp: str
    user: str
    ip_address: str
    event_type: str
    resource: str

# Feature extraction logic (basic inline for now)
def extract_features(log: dict):
    df = pd.DataFrame([log])
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    if df['timestamp'].isnull().any():
        raise ValueError("Invalid timestamp format. Make sure ISO 8601 format is used (e.g. '2025-07-14T10:22:00').")

    df["event_hour"] = df["timestamp"].dt.hour #Hour of the event (0–23)
    event_type_map = {event: i for i, event in enumerate(df["event_type"].unique())}
    df["event_type_code"] = df["event_type"].map(event_type_map) #Numeric encoding of event type
    df["resource_depth"] = df["resource"].str.count("/") #Resource depth - Depth of the accessed URL path
    df["is_privileged_event"] = df["event_type"].isin(["privilege_escalation", "config_change"]).astype(int) #priviledged event ? like escalation or config change
    df["is_weekend"] = df["timestamp"].dt.weekday >= 5 #weekend?

    #failed logins in one hour
    df = df.sort_values(by="timestamp")

    # Filter to just login failures
    failures = df[df["event_type"] == "login_failure"].copy()

    # Initialize the new column
    failures["failed_logins_last_1h"] = 0

    # Group by user and compute rolling counts manually
    for user, group in failures.groupby("user"):
        times = group["timestamp"]
        counts = []

        for i in range(len(times)):
            current_time = times.iloc[i]
            window_start = current_time - pd.Timedelta(hours=1)
            count = times[(times >= window_start) & (times < current_time)].count()
            counts.append(count)

        failures.loc[group.index, "failed_logins_last_1h"] = counts

    # Merge back into original df
    df = df.merge(
        failures[["timestamp", "user", "failed_logins_last_1h"]],
        on=["timestamp", "user"],
        how="left"
    )
    df["failed_logins_last_1h"] = df["failed_logins_last_1h"].fillna(0).astype(int)

    ip_counts = df["ip_address"].value_counts()
    df["ip_event_count"] = df["ip_address"].map(ip_counts)

    # User activity rate
    df["user_event_rate"] = (
        df.groupby("user")["timestamp"]
        .transform("count") / 15  # avg per day over 15 days
        )
    
    features = [
    "event_hour", "event_type_code", "resource_depth",
    "is_privileged_event", "is_weekend",
    "failed_logins_last_1h", "ip_event_count", "user_event_rate"
    ]
    

    return df[features]

@app.post("/score-log")
def score_log(log: AuditLog):
    try:
        features = extract_features(log.model_dump())

        dmatrix = xgb.DMatrix(features)
        # Load XGBoost model from local file
        model = xgb.Booster()
        model.load_model("../models/xgb_model.model") 
        risk_score = model.predict(dmatrix)[0]

        return {
            "risk_score": float(risk_score),
            "classification": "Anomaly" if risk_score > 0.5 else "Normal"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/explain-risk")
def explain_risk(log: AuditLog):
    try:
        features_df = extract_features(log.model_dump())
        model = xgb.XGBClassifier()
        model.load_model("../models/xgb_model.model") 

        explainer = shap.Explainer(model)
        shap_values = explainer(features_df)

        # Turn into human-readable output
        output = {
            "risk_score": float(model.predict_proba(features_df)[0][1]),
            "explanations": {
                feature: float(value)
                for feature, value in zip(features_df.columns, shap_values.values[0])
            }
        }
        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

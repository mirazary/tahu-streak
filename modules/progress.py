import pandas as pd
import os
from datetime import date

DATA_PATH = "data/progress.csv"

def ensure_file():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=["email", "date", "progress", "duration", "mood"])
        df.to_csv(DATA_PATH, index=False)

def save_progress(email, progress, duration, mood):
    ensure_file()
    today = str(date.today())
    
    df = pd.read_csv(DATA_PATH)

    # sudah isi progress hari ini
    if ((df["email"] == email) & (df["date"] == today)).any():
        return False

    new_entry = pd.DataFrame([[email, today, progress, duration, mood]],
                             columns=["email", "date", "progress", "duration", "mood"])
    
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return True

def get_progress(email, limit=10):
    ensure_file()
    df = pd.read_csv(DATA_PATH)
    return df[df["email"] == email].sort_values("date", ascending=False).head(limit)

def has_logged_today(email):
    ensure_file()
    df = pd.read_csv(DATA_PATH)
    today = str(date.today())
    return ((df["email"] == email) & (df["date"] == today)).any()

import pandas as pd
import os
from datetime import date

DATA_PATH = "data/friends.csv"

def ensure_file():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=["user", "friend", "streak", "last_day"])
        df.to_csv(DATA_PATH, index=False)

def get_friends(email):
    ensure_file()
    df = pd.read_csv(DATA_PATH)
    return df[df["user"] == email]

def add_friend(user, friend):
    ensure_file()
    df = pd.read_csv(DATA_PATH)
    if ((df["user"] == user) & (df["friend"] == friend)).any():
        return False
    df.loc[len(df)] = [user, friend, 0, ""]
    df.to_csv(DATA_PATH, index=False)
    return True

def update_fire_streak(user, friend):
    ensure_file()
    df = pd.read_csv(DATA_PATH)
    today = str(date.today())

    mask = (df["user"] == user) & (df["friend"] == friend)
    if mask.any():
        row = df.loc[mask].iloc[0]
        last_day = row["last_day"]
        streak = int(row["streak"])

        # kalau nyala bareng lagi hari ini
        if last_day != today:
            streak += 1
            df.loc[mask, "streak"] = streak
            df.loc[mask, "last_day"] = today
            df.to_csv(DATA_PATH, index=False)
        return streak
    return 0

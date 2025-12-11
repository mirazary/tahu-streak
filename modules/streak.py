import pandas as pd
import os
from datetime import datetime, timedelta


DATA_PATH = "data/streak.csv"


def load_streak(email):
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=["email", "streak", "last_checkin"])
        df.to_csv(DATA_PATH, index=False)

    df = pd.read_csv(DATA_PATH)

    if email not in df["email"].values:
        new_row = pd.DataFrame({"email": [email], "streak": [0], "last_checkin": [""]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)

    row = df[df["email"] == email].iloc[0]
    return int(row["streak"]), str(row["last_checkin"])


def save_streak(email, streak, last_checkin):
    df = pd.read_csv(DATA_PATH)
    df.loc[df["email"] == email, ["streak", "last_checkin"]] = [streak, last_checkin]
    df.to_csv(DATA_PATH, index=False)


def checkin_today(email):
    streak, last_checkin = load_streak(email)
    today = datetime.now().date()

    # Jika belum pernah check-in
    if last_checkin == "" or last_checkin == "nan":
        save_streak(email, 1, str(today))
        return 1, True

    last_date = datetime.strptime(last_checkin, "%Y-%m-%d").date()

    # Jika check-in hari yang sama → tidak boleh dua kali
    if last_date == today:
        return streak, False

    # Hitung jarak hari terakhir
    gap = (today - last_date).days

    # Kalau bolos < 3 hari → streak tetap lanjut
    if 1 <= gap <= 3:
        streak += 1
        save_streak(email, streak, str(today))
        return streak, True

    # Kalau bolos 3 hari atau lebih → reset
    if gap > 3:
        streak = 1
        save_streak(email, streak, str(today))
        return streak, True

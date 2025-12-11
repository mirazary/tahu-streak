import os
import pandas as pd
from datetime import date

DATA_PATH = "data/progress.csv"

# Membuat file progress.csv jika belum ada
def ensure_file():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=["email", "date", "progress"])
        df.to_csv(DATA_PATH, index=False)

# Menyimpan progress harian user
def log_progress(email, progress_text):
    ensure_file()
    today = str(date.today())

    df = pd.read_csv(DATA_PATH)

    # jika user sudah log hari ini → update teksnya
    if ((df["email"] == email) & (df["date"] == today)).any():
        df.loc[(df["email"] == email) & (df["date"] == today), "progress"] = progress_text
    else:
        new_row = pd.DataFrame([[email, today, progress_text]],
                               columns=["email", "date", "progress"])
        df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(DATA_PATH, index=False)
    return True

# Mengecek apakah user sudah log hari ini
def has_logged_today(email):
    ensure_file()
    df = pd.read_csv(DATA_PATH)
    today = str(date.today())

    return ((df["email"] == email) & (df["date"] == today)).any()

# Mengambil semua progress user
def get_progress_history(email, limit=20):
    ensure_file()
    df = pd.read_csv(DATA_PATH)

    return df[df["email"] == email].sort_values("date", ascending=False).head(limit)

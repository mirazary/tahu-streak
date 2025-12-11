import os
import pandas as pd
from datetime import datetime

DATA_PATH = "data/pet.csv"

def ensure_file():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=["email", "level", "exp", "last_updated"])
        df.to_csv(DATA_PATH, index=False)

def load_pet(email):
    ensure_file()
    df = pd.read_csv(DATA_PATH)
    row = df[df["email"] == email]
    if row.empty:
        return 1, 0  # default level 1, exp 0
    return int(row.level.values[0]), int(row.exp.values[0])

def update_pet(email, new_level, new_exp):
    ensure_file()
    df = pd.read_csv(DATA_PATH)
    df = df[df["email"] != email]
    df.loc[len(df)] = [email, new_level, new_exp, datetime.now()]
    df.to_csv(DATA_PATH, index=False)

def get_pet_stage(streak):
    if streak < 5:
        return 1, "Tahu Polos", "Bahagia 🌸"
    elif streak < 10:
        return 2, "Tahu Hebat", "Semangat 🔥"
    else:
        return 3, "Tahu Legendaris", "Tak Terhentikan 💪"

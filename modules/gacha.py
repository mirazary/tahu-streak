import random
import pandas as pd
import os
from datetime import date

# lokasi penyimpanan data hasil gacha
DATA_PATH = "data/gacha.csv"

# tingkat rarity dan peluang drop-nya
RARITY = {
    "Common": 0.7,
    "Rare": 0.2,
    "Epic": 0.09,
    "Legendary": 0.01
}

# daftar hadiah berdasarkan rarity
REWARDS = {
    "Common": [
        "Sticker Semangat",
        "Kopi Instan",
        "Doa Dosen Lolos Bab 3",
        "Notifikasi Reviewer yang Lembut"
    ],
    "Rare": [
        "Motivasi Premium",
        "Kucing Good Luck",
        "Es Krim Anti Stress",
        "Playlist Fokus TA"
    ],
    "Epic": [
        "Tahu Emas",
        "Pet TAHU Level Boost",
        "Plakat Juara TA",
        "Extra Power of Revision"
    ],
    "Legendary": [
        "Super TAHU Mode",
        "Golden Thesis",
        "Dosen Jadi Baik Hari Ini",
        "Skip Sidang Sementara 😎"
    ]
}

# pastikan file gacha.csv ada
def ensure_file():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=["email", "date", "rarity", "reward"])
        df.to_csv(DATA_PATH, index=False)

# fungsi utama untuk melakukan gacha
def roll_gacha(email):
    ensure_file()
    today = date.today()

    df = pd.read_csv(DATA_PATH)

    # cek apakah user sudah gacha hari ini
    if ((df["email"] == email) & (df["date"] == str(today))).any():
        return None, None, False  # sudah gacha hari ini

    # tentukan rarity berdasarkan peluang
    r = random.random()
    cumulative = 0
    rarity = "Common"
    for name, chance in RARITY.items():
        cumulative += chance
        if r <= cumulative:
            rarity = name
            break

    # pilih hadiah berdasarkan rarity
    reward = random.choice(REWARDS[rarity])

    # simpan hasil gacha ke CSV
    new_entry = pd.DataFrame([[email, today, rarity, reward]], columns=["email", "date", "rarity", "reward"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

    return rarity, reward, True  # True artinya sukses gacha

# ambil riwayat gacha user
def get_history(email, limit=5):
    ensure_file()
    df = pd.read_csv(DATA_PATH)
    user_data = df[df["email"] == email].sort_values("date", ascending=False).head(limit)
    return user_data

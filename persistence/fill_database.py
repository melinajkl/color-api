from __future__ import annotations

import csv
from pathlib import Path

from persistence.connection import get_connection


CSV_PATH = Path(__file__).resolve().parent.parent / "ressources" / "themes.csv"


with get_connection() as conn:
    cur = conn.cursor()
    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        data = []
        for row in reader:
            key = f"{row['time_of_day']}:{row['day_type']}:{row['weather']}"
            data.append((
                key,
                row["time_of_day"],
                row["day_type"],
                row["weather"],
                row["background"],
                row["surface"],
                row["primary"],
                row["secondary"],
            ))

    sql = """
    INSERT INTO color_palette (
        palette_key,
        time_of_day,
        day_type,
        weather,
        background,
        surface,
        primary_color,
        secondary_color
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    cur.executemany(sql, data)
    conn.commit()
    cur.close()
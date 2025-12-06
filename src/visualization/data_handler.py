import sqlite3
from typing import List, Dict


class DataEconomyHandler:
    def __init__(self):
        self._conn = sqlite3.connect("economy.sqlite")
        self._cursor = self._conn.cursor()

    def initialize_data_base(self) -> "DataEconomyHandler":
        self._cursor.execute("DROP TABLE IF EXISTS years")
        self._conn.commit()
        self._cursor.execute("""
                             CREATE TABLE IF NOT EXISTS years
                             (
                                 year INTEGER PRIMARY KEY AUTOINCREMENT,
                                 output REAL,
                                 inflation REAL,
                                 unemployment REAL,
                                 rate REAL,
                                 wage REAL
                             )
                             """)
        self._conn.commit()
        return self
        
    def append(self, output: float, inflation: float, unemployment: float, rate: float, wage: float):
        self._cursor.execute("""
                             INSERT INTO years (output, inflation, unemployment, rate, wage)
                             VALUES (?, ?, ?, ?, ?)
                             """, (output, inflation, unemployment, rate, wage))
        self._conn.commit()

    def get_data_us_history(self) -> List[Dict[str, float]]:
        self._cursor.execute("SELECT year, output, inflation, unemployment, rate, wage FROM years")
        rows = self._cursor.fetchall()
        return [
            {
                "period": row[0],
                "output": row[1],
                "inflation": row[2],
                "unemployment": row[3],
                "rate": row[4],
                "wage": row[5]
            }
            for row in rows
        ]
        
        
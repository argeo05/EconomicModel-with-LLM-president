import sqlite3
from typing import List, Dict


class DataEconomyHandler:
    """Handler for storing simulation data.

    Attributes:
        _conn: SQLite database connection
        _cursor: Database cursor
    """
    
    def __init__(self):
        self._conn = sqlite3.connect("economy.sqlite")
        self._cursor = self._conn.cursor()

    def initialize_data_base(self) -> "DataEconomyHandler":
        """Initialize database schema.

        Returns:
            Self for method chaining
        """
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
                                 wage REAL,
                                 presidentAdvice TEXT
                             )
                             """)
        self._conn.commit()
        return self
        
    def append(self, output: float, inflation: float, unemployment: float, rate: float, wage: float, presidentAdvice: str):
        """Append single record to database.

        Args:
            output: Output value
            inflation: Inflation rate
            unemployment: Unemployment rate
            rate: Interest rate
            wage: Wage rate
            presidentAdvice: President advice message
        """
        self._cursor.execute("""
                             INSERT INTO years (output, inflation, unemployment, rate, wage, presidentAdvice)
                             VALUES (?, ?, ?, ?, ?, ?)
                             """, (output, inflation, unemployment, rate, wage, presidentAdvice))
        self._conn.commit()

    def append_all(self, records: List[tuple]):
        """Append multiple records to database.

        Args:
            records: List of tuples containing (output, inflation, unemployment, rate, wage, presidentAdvice)
        """
        self._cursor.executemany("""
                                 INSERT INTO years (output, inflation, unemployment, rate, wage, presidentAdvice)
                                 VALUES (?, ?, ?, ?, ?, ?)
                                 """, records)
        self._conn.commit()

    def get_data_us_history(self) -> List[Dict[str, float]]:
        """Get all historical data from database.

        Returns:
            List of dictionaries with period, output, inflation, unemployment, rate, wage
        """
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
        
        